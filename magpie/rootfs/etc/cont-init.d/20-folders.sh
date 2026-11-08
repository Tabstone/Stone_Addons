#!/bin/sh
set -eu

for dir in /config /config/magpie /config/home /config/cache /config/data /config/state; do
  mkdir -p "$dir"
done

chown 65532:65532 /config
chown -R 65532:65532 \
  /config/magpie \
  /config/home \
  /config/cache \
  /config/data \
  /config/state
