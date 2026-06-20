#!/bin/sh
set -eu

mkdir -p /config/reports
chown -R node:node /config/reports
chmod 0777 /config/reports

if [ -e /app/reports ] && [ ! -L /app/reports ]; then
  rm -rf /app/reports
fi

ln -sfn /config/reports /app/reports
chown -h node:node /app/reports
