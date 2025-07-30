"""
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT-0
"""
import json
import logging
import re
import time
import uuid

from cfn_policy_validator.canonical_user_id import client, get_canonical_user
from cfn_policy_validator.validation.findings import Findings, create_custom_error_finding
from cfn_policy_validator.validation import InvalidPolicyException
from cfn_policy_validator.validation.reporter import Reporter
from cfn_policy_validator.application_error import ApplicationError


LOGGER = logging.getLogger("cfn-policy-validator")


def validate(parser_output, findings_to_ignore, finding_types_that_are_errors, allowed_external_principals):
	"""
	Run the output from the parsers through IAM Access Analyzer, filter, and report the findings.
	"""

	findings = validate_parser_output(parser_output)

	reporter = Reporter(findings_to_ignore, finding_types_that_are_errors, allowed_external_principals)
	return reporter.build_report_from(findings)


def validate_parser_output(parser_output):
	"""
	Run the parser output through IAM Access Analyzer validation
	"""
	validator = Validator(parser_output.Account, parser_output.Region, parser_output.Partition)

	validator.validate_policies(parser_output.OrphanedPolicies)
	validator.validate_roles(parser_output.Roles)
	validator.validate_users(parser_output.Users)
	validator.validate_groups(parser_output.Groups)
	validator.validate_permission_sets(parser_output.PermissionSets)
	validator.validate_resources(parser_output.Resources)

	return validator.findings


class Validator:
	RESOURCE_POLICY_TYPE = 'RESOURCE_POLICY'
	IDENTITY_POLICY_TYPE = 'IDENTITY_POLICY'

	def __init__(self, account_id, region, partition):
		self.findings = Findings()
		self.access_analyzer_name = 'AnalyzerCreatedByCfnIAMPolicyValidator'
		self.analyzer_arn = None

		self.client = client.build('accessanalyzer', region)

		# preview builders are used to build the access preview configuration for an individual resource type
		# a preview builder must be added to add support for access previews for a given resource
		self.preview_builders = {
			'AWS::SQS::Queue': SqsQueuePreviewBuilder(account_id, region, partition),
			'AWS::KMS::Key': KmsKeyPreviewBuilder(account_id, region, partition),
			'AWS::S3::AccessPoint': S3SingleRegionAccessPointPreviewBuilder(account_id, region, partition),
			'AWS::S3::MultiRegionAccessPoint': S3MultiRegionAccessPointPreviewBuilder(account_id, partition),
			'AWS::S3::Bucket': S3BucketPreviewBuilder(region, partition),
			'AWS::IAM::Role::TrustPolicy': RoleTrustPolicyPreviewBuilder(account_id, partition),
			'AWS::SecretsManager::Secret': SecretsManagerSecretPreviewBuilder(account_id, region, partition)
		}

		# maps the resource type to the parameter for validate_policy that enables service specific policy validation
		# not all services have service specific policy validation.  The names may be identical for now, but we don't
		# want to rely on that
		self.service_specific_policy_validation = {
			'AWS::S3::Bucket': 'AWS::S3::Bucket',
			'AWS::S3::AccessPoint': 'AWS::S3::AccessPoint',
			'AWS::S3::MultiRegionAccessPoint': 'AWS::S3::MultiRegionAccessPoint'
		}

		self.maximum_number_of_access_preview_attempts = 150
		self._try_create_analyzer()

	def validate_roles(self, roles):
		"""
		Validate policies attached to roles
		"""
		previews_to_await = []
		for role in roles:
			LOGGER.info(f'Validating trust policy for role {role.RoleName}..')
			validation_findings = self._validate_policy(role.TrustPolicy, self.RESOURCE_POLICY_TYPE, False, 'AWS::IAM::AssumeRolePolicyDocument')
			self.findings.add_validation_finding(validation_findings, role.RoleName, 'TrustPolicy')

			# use access previews to validate a role's trust policy
			preview = self.__validate_role_trust_policy(role, validation_findings)
			previews_to_await.append(preview)

			# validate identity policies attached to the role
			for policy in role.Policies:
				LOGGER.info(f'Validating identity policy for {role.RoleName} with name {policy.Name}')
				validation_findings = self._validate_policy(policy.Policy, self.IDENTITY_POLICY_TYPE, policy.IsAWSManagedPolicy)
				self.findings.add_validation_finding(validation_findings, role.RoleName, policy.Name)

		access_preview_findings = self._wait_for_findings(previews_to_await)
		for access_preview_finding in access_preview_findings:
			self.findings.add_trust_policy_finding(access_preview_finding.findings, access_preview_finding.resource.RoleName)

	def __validate_role_trust_policy(self, role, validation_findings):
		preview_builder = self.preview_builders['AWS::IAM::Role::TrustPolicy']
		configuration = preview_builder.build_configuration(role)

		LOGGER.info(f'Creating access preview with configuration {configuration}')
		response = self.client.create_access_preview(
			analyzerArn=self.analyzer_arn,
			configurations=configuration
		)
		LOGGER.info(f'CreateAccessPreview response: {response}')
		return PreviewAwaitingResponse(response['id'], role, role.RoleName, 'TrustPolicy', validation_findings)

	def validate_policies(self, policies):
		"""
		Validate orphaned policies
		"""
		resource_name = 'No resource attached'
		for policy in policies:
			LOGGER.info(f'Validating identity policy for {policy.Name}')
			validation_findings = self._validate_policy(policy.Policy, self.IDENTITY_POLICY_TYPE, policy.IsAWSManagedPolicy)
			self.findings.add_validation_finding(validation_findings, resource_name, policy.Name)

	def validate_users(self, users):
		"""
		Validate policies attached to users
		"""
		for user in users:
			for policy in user.Policies:
				LOGGER.info(f'Validating identity policy for user {user.UserName} with policy name {policy.Name}')
				validation_findings = self._validate_policy(policy.Policy, self.IDENTITY_POLICY_TYPE, policy.IsAWSManagedPolicy)
				self.findings.add_validation_finding(validation_findings, user.UserName, policy.Name)

	def validate_groups(self, groups):
		"""
		Validate policies attached to groups
		"""
		for group in groups:
			for policy in group.Policies:
				LOGGER.info(f'Validating identity policy for group {group.GroupName} with policy name {policy.Name}')
				validation_findings = self._validate_policy(policy.Policy, self.IDENTITY_POLICY_TYPE, policy.IsAWSManagedPolicy)
				self.findings.add_validation_finding(validation_findings, group.GroupName, policy.Name)

	def validate_permission_sets(self, permission_sets):
		"""
		Validate policies attached to permission sets
		"""
		for permission_set in permission_sets:
			for policy in permission_set.Policies:
				LOGGER.info(f'Validating identity policy for permission set {permission_set.Name} with policy name {policy.Name}')
				validation_findings = self._validate_policy(policy.Policy, self.IDENTITY_POLICY_TYPE, policy.IsAWSManagedPolicy)
				self.findings.add_validation_finding(validation_findings, permission_set.Name, policy.Name)

	def validate_resources(self, resources):
		"""
		Validate resource policies
		"""
		previews_to_await = []
		for resource in resources:
			validation_findings = []
			if resource.Policy.Policy is None:
				LOGGER.info(f'Resource {resource.ResourceName} has no resource-based policy.  Skipping call to ValidatePolicy.')
			else:
				# we want to run validate_policy on all resource policies regardless of if they are supported policies
				# for access previews
				LOGGER.info(f'Validating resource policy for resource {resource.ResourceName} of type {resource.ResourceType}')

				validate_policy_resource_type = self.service_specific_policy_validation.get(resource.ResourceType)
				validation_findings = self._validate_policy(resource.Policy.Policy, self.RESOURCE_POLICY_TYPE, False, validate_policy_resource_type)
				self.findings.add_validation_finding(validation_findings, resource.ResourceName, resource.Policy.Name)

			# only supported policies for access previews will have config builders
			preview_builder = self.preview_builders.get(resource.ResourceType)
			if preview_builder is not None:
				try:
					configuration = preview_builder.build_configuration(resource)
				except InvalidPolicyException as e:
					validation_finding = create_custom_error_finding(
						f'Failed to create access preview for {resource.ResourceName}. Reason: {e.to_string()}',
						'FAILED_ACCESS_PREVIEW_CREATION'
					)
					self.findings.add_validation_finding([validation_finding], resource.ResourceName,resource.Policy.Name)
					continue

				LOGGER.info(f'Creating access preview for resource {resource.ResourceName} of type {resource.ResourceType}')
				LOGGER.info(f'Using access preview configuration: {configuration}')

				try:
					response = self.client.create_access_preview(
						analyzerArn=self.analyzer_arn,
						configurations=configuration
					)
				except Exception as e:
					validation_finding = create_custom_error_finding(
						f'Failed to create access preview for {resource.ResourceName}. Reason: {e}',
						'FAILED_ACCESS_PREVIEW_CREATION'
					)
					self.findings.add_validation_finding(
						[validation_finding],
						resource.ResourceName,
						resource.Policy.Name
					)
					continue

				LOGGER.info(f'CreateAccessPreview response: {response}')
				preview = PreviewAwaitingResponse(response['id'], resource, resource.ResourceName, resource.Policy.Name, validation_findings)
				previews_to_await.append(preview)

		# batch and wait for all access previews to complete
		access_preview_findings = self._wait_for_findings(previews_to_await)

		for access_preview_finding in access_preview_findings:
			self.findings.add_external_principal_finding(access_preview_finding.findings,
														 access_preview_finding.resource.ResourceName,
														 access_preview_finding.resource.Policy.Name)

	def _validate_policy(self, policy_as_json, policy_type, is_aws_managed_policy, resource_type=None):
		policy_as_string = json.dumps(policy_as_json)
		policy_without_whitespace = policy_as_string.replace(" ", "")
		length_of_policy_without_whitespace = len(policy_without_whitespace)
		if length_of_policy_without_whitespace >= 32768:
			if is_aws_managed_policy:
				LOGGER.info(f'AWS managed policy has length {length_of_policy_without_whitespace} which exceeds the max size (32768 bytes) for ValidatePolicy call.  Ignoring..')
				return []
			else:
				# if this is a customer policy, we return an error finding
				return [self._build_policy_size_finding(length_of_policy_without_whitespace)]

		LOGGER.info(policy_as_string)
		paginator = self.client.get_paginator('validate_policy')
		args = {
			'policyDocument': policy_as_string,
			'policyType': policy_type
		}

		if resource_type is not None:
			LOGGER.info(f'Running service specific policy validation for {resource_type}')
			args['policyType'] = self.RESOURCE_POLICY_TYPE
			args['validatePolicyResourceType'] = resource_type

		response_iterator = paginator.paginate(**args)
		findings = []
		for page in response_iterator:
			LOGGER.info(f'ValidatePolicy response: {page}')
			findings.extend(page['findings'])

		return findings

	@staticmethod
	def _build_policy_size_finding(policy_size):
		return {
			'findingType': 'ERROR',
			'findingDetails': f'The {policy_size} characters in the policy, excluding whitespace, exceed the character maximum for the ValidatePolicy API. We recommend that you use multiple granular policies.',
			'issueCode': 'POLICY_SIZE_EXCEEDS_VALIDATE_POLICY_MAXIMUM'
		}

	def _wait_for_findings(self, previews_to_await):
		findings = []
		for preview in previews_to_await:
			number_of_attempts = 0
			while True:
				LOGGER.info(f'Waiting on access preview {preview.id} to finish creating attempt {number_of_attempts+1}..')
				response = self.client.get_access_preview(
					accessPreviewId=preview.id,
					analyzerArn=self.analyzer_arn
				)
				LOGGER.info(f'GetAccessPreview response: {response}')
				status = response['accessPreview']['status']

				if status == 'CREATING':
					number_of_attempts = number_of_attempts + 1
					if number_of_attempts >= self.maximum_number_of_access_preview_attempts:
						raise ApplicationError(f'Timed out after 5 minutes waiting for access analyzer preview to create.')

					time.sleep(2)
				else:
					break

			LOGGER.info(f'Access preview creation completed for {preview.resource_name} with status {status}')

			if status == 'FAILED':
				reason = response["accessPreview"]["statusReason"]["code"]
				if reason == 'INVALID_CONFIGURATION':
					# if we have a validation finding of type error, return that instead of throwing an exception so
					# that users can implement rules to ignore the finding and/or resource.  This is useful when policies
					# use functions that are not yet supported
					if self._has_validation_finding_of_type_error(preview.validation_findings):
						# do nothing, there is already an error finding being reported
						continue
					else:
						# if there's no error finding, create our own
						validation_finding = create_custom_error_finding(
							f'Failed to create access preview for {preview.resource_name}. Reason: {reason}',
							'FAILED_ACCESS_PREVIEW_CREATION'
						)
						self.findings.add_validation_finding(
							[validation_finding],
							preview.resource_name,
							preview.policy_name
						)

					continue
				else:
					raise ApplicationError(f'Failed to create access preview for {preview.resource_name}.  Reason: {reason}')

			paginator = self.client.get_paginator('list_access_preview_findings')
			for page in paginator.paginate(accessPreviewId=preview.id, analyzerArn=self.analyzer_arn):
				active_findings = []
				for finding in page['findings']:
					LOGGER.info(f'Access preview finding: {finding}')
					if finding['status'] == 'ACTIVE':
						active_findings.append(finding)

				if len(active_findings) > 0:
					findings.append(AccessPreviewFindings(preview.resource, active_findings))

		return findings

	@staticmethod
	def _filter_findings_for_source_type(raw_findings, desired_source_type):
		filtered_findings = []
		for raw_finding in raw_findings:
			sources = raw_finding.get('sources')
			if sources is None:
				continue

			if any([source for source in sources if source.get('type') == desired_source_type]):
				filtered_findings.append(raw_finding)

		return filtered_findings

	def _try_create_analyzer(self):
		if self.analyzer_arn is not None:
			return

		response = self.client.list_analyzers(
			type='ACCOUNT'
		)

		first_active_analyzer = next((analyzer for analyzer in response['analyzers'] if analyzer['status'] == 'ACTIVE'), None)
		if first_active_analyzer is not None:
			self.analyzer_arn = first_active_analyzer['arn']
			return

		LOGGER.info('No active analyzers found in account.  Creating analyzer.')
		response = self.client.create_analyzer(
			analyzerName=self.access_analyzer_name,
			type='ACCOUNT'
		)
		self.analyzer_arn = response['arn']

	@staticmethod
	def _has_validation_finding_of_type_error(validation_findings):
		return any(validation_finding for validation_finding in validation_findings if validation_finding['findingType'] == 'ERROR')


class AccessPreviewFindings:
	def __init__(self, resource, findings):
		self.resource = resource
		self.findings = findings


class PreviewAwaitingResponse:
	def __init__(self, preview_id, resource, resource_name, policy_name, validation_findings):
		self.id = preview_id
		self.resource = resource
		self.resource_name = resource_name
		self.policy_name = policy_name
		self.validation_findings = validation_findings


class SqsQueuePreviewBuilder:
	def __init__(self, account_id, region, partition):
		self.region = region
		self.account_id = account_id
		self.partition = partition

	def build_configuration(self, resource):
		policy = json.dumps(resource.Policy.Policy)

		return {
			f'arn:{self.partition}:sqs:{self.region}:{self.account_id}:{resource.ResourceName}': {
				'sqsQueue': {
					'queuePolicy': policy
				}
			}
		}


class KmsKeyPreviewBuilder:
	def __init__(self, account_id, region, partition):
		self.account_id = account_id
		self.region = region
		self.partition = partition

	def build_configuration(self, resource):
		policy = json.dumps(resource.Policy.Policy)

		return {
			f'arn:{self.partition}:kms:{self.region}:{self.account_id}:key/{resource.ResourceName}': {
				'kmsKey': {
					'keyPolicies': {
						'default': policy
					}
				}
			}
		}


class S3BucketPreviewBuilder:
	def __init__(self, region, partition):
		self.partition = partition
		self.region = region

	def build_configuration(self, resource):
		s3_bucket_json = {}

		# either policy or access control must be present, there exists no resource where they are both null
		if resource.Policy.Policy is not None:
			policy = json.dumps(resource.Policy.Policy)
			s3_bucket_json['bucketPolicy'] = policy

		access_control = resource.Configuration.get('AccessControl')
		if access_control is not None:
			bucket_acl_grants = self.__build_bucket_acl_grants(resource.ResourceName, access_control)
			s3_bucket_json['bucketAclGrants'] = bucket_acl_grants

		return {
			f'arn:{self.partition}:s3:::{resource.ResourceName}': {
				's3Bucket': s3_bucket_json
			}
		}

	def __build_bucket_acl_grants(self, bucket_name, access_control_value):
		if access_control_value == 'Private':
			return [self.__build_owner_full_control_grant()]
		elif access_control_value == 'PublicRead':
			return [
				self.__build_owner_full_control_grant(),
				self.__build_grant_uri(self.all_users_group_uri, 'READ')
			]
		elif access_control_value == 'PublicReadWrite':
			return [
				self.__build_owner_full_control_grant(),
				self.__build_grant_uri(self.all_users_group_uri, 'READ'),
				self.__build_grant_uri(self.all_users_group_uri, 'WRITE')
			]
		elif access_control_value == 'AuthenticatedRead':
			return [
				self.__build_owner_full_control_grant(),
				self.__build_grant_uri(self.authenticated_users_group_uri, 'READ')
			]
		elif access_control_value == 'LogDeliveryWrite':
			return [
				self.__build_grant_uri(self.log_delivery_group_uri, 'WRITE'),
				self.__build_grant_uri(self.log_delivery_group_uri, 'READ_ACP')
			]
		elif access_control_value == 'BucketOwnerRead':
			return [self.__build_owner_full_control_grant()]
		elif access_control_value == 'BucketOwnerFullControl':
			return [self.__build_owner_full_control_grant()]
		elif access_control_value == 'AwsExecRead':
			return [
				self.__build_owner_full_control_grant(),
				self.__build_grant_id(self.ec2_canonical_id, 'READ')
			]
		else:
			raise ApplicationError(f'Invalid AccessControl value "{access_control_value}" for {bucket_name}.\n'
								f'See https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-accesscontrol '
								f'for valid AccessControl values.')

	all_users_group_uri = 'http://acs.amazonaws.com/groups/global/AllUsers'
	authenticated_users_group_uri = 'http://acs.amazonaws.com/groups/global/AuthenticatedUsers'
	log_delivery_group_uri = 'http://acs.amazonaws.com/groups/s3/LogDelivery'
	ec2_canonical_id = '6aa5a366c34c1cbe25dc49211496e913e0351eb0e8c37aa3477e40942ec6b97c'

	@staticmethod
	def __build_grant_uri(uri, permission):
		return {
			'grantee': {
				'uri': uri
			},
			'permission': permission
		}

	@staticmethod
	def __build_grant_id(grant_id, permission):
		return {
			'grantee': {
				'id': grant_id
			},
			'permission': permission
		}

	def __build_owner_full_control_grant(self):
		return self.__build_grant_id(get_canonical_user(self.region), 'FULL_CONTROL')


class S3AccessPointPreviewBuilder:
	def __init__(self, account_id, partition, region=None):
		self.partition = partition
		self.account_id = account_id
		self.region = region

	# this bucket policy enforces that access must come through an access point so that we can evaluate the access point
	# policy independent of the bucket policy
	def build_bucket_policy(self, bucket_name):
		return {
			"Version": "2012-10-17",
			"Statement": [
				{
					"Effect": "Allow",
					"Principal": {
						"AWS": "*"
					},
					"Action": "*",
					"Resource": [
						f"arn:aws:s3:::{bucket_name}",
						f"arn:aws:s3:::{bucket_name}/*"
					],
					"Condition": {
						"StringEquals": {
							"s3:DataAccessPointAccount": self.account_id
						}
					}
				}
			]
		}


class S3MultiRegionAccessPointPreviewBuilder(S3AccessPointPreviewBuilder):
	def __init__(self, account_id, partition):
		super(S3MultiRegionAccessPointPreviewBuilder, self).__init__(account_id, partition)

	def build_configuration(self, resource):
		policy_json = resource.Policy.Policy
		policy = json.dumps(resource.Policy.Policy)

		# since we're evaluating the access point independently, the name of the bucket does not matter
		bucket_name = str(uuid.uuid4())

		bucket_policy_json = self.build_bucket_policy(bucket_name)
		bucket_policy = json.dumps(bucket_policy_json)

		access_point_arn = self.build_access_point_arn(resource.ResourceName, policy_json)

		return {
			f'arn:{self.partition}:s3:::{bucket_name}': {
				's3Bucket': {
					'accessPoints': {
						access_point_arn: {
							'accessPointPolicy': policy
						}
					},
					'bucketPolicy': bucket_policy
				}
			}
		}

	# match the alias of the multi region access point in an access point's ARN:
	# "arn:aws:s3::111111111111:accesspoint/MyAccessPoint.mrap/object/abc/*" would find "MyAccessPoint.mrap"
	access_point_alias_regex = re.compile(r'arn:[^:]*:s3::[^:]*:accesspoint/([^/]*)')

	# find the access point ARN from the first resource in the access point policy
	def build_access_point_arn(self, access_point_name, access_point_policy):
		error_message_prefix = f"Access point policy for {access_point_name}"
		statements = access_point_policy.get('Statement')
		if not isinstance(statements, list):
			statements = [statements]

		# we only need to look at the first resource in the first statement.  All statements must have resources
		# and all resources must include the multi region access point ARN.
		first_statement = next(iter(statements), None)
		if not isinstance(first_statement, dict):
			raise InvalidPolicyException(f"{error_message_prefix} has 'Statement' that is missing or is of invalid type.", access_point_policy)

		resource = first_statement.get('Resource')
		if not isinstance(resource, list):
			resource = [resource]

		resource = next(iter(resource), None)
		if not isinstance(resource, str):
			raise InvalidPolicyException(f"{error_message_prefix} has 'Resource' element that is missing or is of invalid type.", access_point_policy)

		match = self.access_point_alias_regex.search(resource)
		if match is None:
			raise InvalidPolicyException(f"{error_message_prefix} has entry for 'Resource' with invalid multi-region access point ARN.", access_point_policy)
		else:
			return f'arn:{self.partition}:s3::{self.account_id}:accesspoint/{match.group(1)}'


class S3SingleRegionAccessPointPreviewBuilder(S3AccessPointPreviewBuilder):
	def __init__(self, account_id, region, partition):
		super(S3SingleRegionAccessPointPreviewBuilder, self).__init__(account_id, partition, region)

	def build_configuration(self, resource):
		policy = json.dumps(resource.Policy.Policy)

		# since we're evaluating the access point independently, the name of the bucket does not matter
		bucket_name = str(uuid.uuid4())

		bucket_policy_json = self.build_bucket_policy(bucket_name)
		bucket_policy = json.dumps(bucket_policy_json)

		network_origin = {
			'internetConfiguration': {}
		}

		if resource.Configuration is not None and 'VpcId' in resource.Configuration:
			network_origin = {
				'vpcConfiguration': {
					'vpcId': resource.Configuration['VpcId']
				}
			}

		return {
			f'arn:{self.partition}:s3:::{bucket_name}': {
				's3Bucket': {
					'accessPoints': {
						f'arn:{self.partition}:s3:{self.region}:{self.account_id}:accesspoint/{resource.ResourceName}': {
							'accessPointPolicy': policy,
							'networkOrigin': network_origin
						}
					},
					'bucketPolicy': bucket_policy
				}
			}
		}


class RoleTrustPolicyPreviewBuilder:
	def __init__(self, account_id, partition):
		self.account_id = account_id
		self.partition = partition

	def build_configuration(self, resource):
		policy = json.dumps(resource.TrustPolicy)

		role_name = resource.RoleName[:64]

		return {
			f'arn:{self.partition}:iam::{self.account_id}:role/{role_name}': {
				'iamRole': {
					'trustPolicy': policy
				}
			}
		}


class SecretsManagerSecretPreviewBuilder:
	def __init__(self, account_id, region, partition):
		self.account_id = account_id
		self.region = region
		self.partition = partition

	def build_configuration(self, resource):
		policy = json.dumps(resource.Policy.Policy)

		return {
			# secrets manager arns have a random 6 characters appended to the end
			f'arn:{self.partition}:secretsmanager:{self.region}:{self.account_id}:secret:{resource.ResourceName}-3xyxqI': {
				'secretsManagerSecret': {
					'secretPolicy': policy
				}
			}
		}
