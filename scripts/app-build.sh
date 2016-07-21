#!/usr/bin/env bash

set -o errexit
set -o xtrace

rm -rf ./app/dist

mkdir -p ./app/dist
mkdir -p ./app/dist/js

# Copy HTML index.
cp ./app/src/html/index.html ./app/dist/

# Create JS bundle.
browserify \
	./app/src/js/app.js \
	--debug \
	--transform [babelify] \
	--plugin [minifyify --map app-bundle.js.map --output ./app/dist/js/app-bundle.js.map] \
	--outfile ./app/dist/js/app-bundle.js
