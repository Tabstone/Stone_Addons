#!/bin/sh
set -eu

ROOT_DIR="/config"
DATA_DIR="${ROOT_DIR}/data"
UPSTREAM_DIR="${ROOT_DIR}/workbuddy2api"

mkdir -p "$DATA_DIR" "$UPSTREAM_DIR"

if [ -d /opt/workbuddy2api ] && [ ! -L /opt/workbuddy2api ]; then
  python - "$UPSTREAM_DIR" <<'PY'
from pathlib import Path
import shutil
import sys

def copy_missing(source, destination):
    target = Path(destination)
    if not target.exists() and not target.is_symlink():
        shutil.copy2(source, destination)

shutil.copytree("/opt/workbuddy2api", sys.argv[1], dirs_exist_ok=True, copy_function=copy_missing)
PY
  rm -rf /opt/workbuddy2api
fi

chown -R 10001:10001 "$DATA_DIR" "$UPSTREAM_DIR"
chmod 0770 "$DATA_DIR" "$UPSTREAM_DIR"

if [ -e /app/data ] && [ ! -L /app/data ]; then
  rm -rf /app/data
fi

ln -sfn "$DATA_DIR" /app/data
ln -sfn "$UPSTREAM_DIR" /opt/workbuddy2api
