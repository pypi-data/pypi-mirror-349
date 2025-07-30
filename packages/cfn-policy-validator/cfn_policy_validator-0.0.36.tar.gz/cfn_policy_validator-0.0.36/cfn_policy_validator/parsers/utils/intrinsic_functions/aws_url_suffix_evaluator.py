"""
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT-0
"""

url_suffixes = {
	'cn-north-1': 'amazonaws.com.cn',
	'cn-northwest-1': 'amazonaws.com.cn'
}

default_url_suffix = 'amazonaws.com'


def evaluate(region):
	return url_suffixes.get(region, default_url_suffix)
