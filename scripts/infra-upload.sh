#!/usr/bin/env bash

set -o errexit
set -o xtrace

aws s3 cp \
	--recursive \
	./cloudformation/generated \
	s3://cloudcloud-site-cloudformation/
