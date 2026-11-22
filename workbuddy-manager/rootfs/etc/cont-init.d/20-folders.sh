#!/bin/sh
set -eu

ROOT_DIR="/config"
DATA_DIR="${ROOT_DIR}/data"

mkdir -p "$DATA_DIR"
chown -R 10001:10001 "$DATA_DIR"
chmod 0770 "$DATA_DIR"

if [ -e /app/data ] && [ ! -L /app/data ]; then
  rm -rf /app/data
fi

ln -sfn "$DATA_DIR" /app/data
