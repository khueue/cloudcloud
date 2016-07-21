#!/usr/bin/env bash

set -o errexit
set -o xtrace

aws s3 cp \
	--recursive \
	./app/dist \
	s3://cloudcloud-site-app/
