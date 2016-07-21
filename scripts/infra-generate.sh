#!/usr/bin/env bash

set -o errexit

# Python with:
# -Wall Warnings.
# -3 Compatibility warnings for Python 3.
# -B Skip generating .pyc files.
PYTHON="python -Wall -3 -B"

declare -a STACKS=(
	dns.py
	main.py
	storage.py
)

rm -rf ./cloudformation/generated/*.template
mkdir -p ./cloudformation/generated

for stack in "${STACKS[@]}"; do
	# Generate.
	echo "--- Generating template for ./cloudformation/troposphere/${stack} ..."
	${PYTHON} "./cloudformation/troposphere/${stack}" > "./cloudformation/generated/${stack}.template"
done

echo
