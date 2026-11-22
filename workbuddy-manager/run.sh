#!/bin/sh
set -eu

if [ -d /etc/cont-init.d ]; then
  for script in /etc/cont-init.d/*; do
    [ -f "$script" ] || continue
    if [ -x "$script" ]; then
      "$script"
    else
      /bin/sh "$script"
    fi
  done
fi

if [ -f /tmp/addon_env.sh ]; then
  . /tmp/addon_env.sh
fi

if [ "$#" -eq 0 ]; then
  set -- python -m uvicorn server.main:app --host 0.0.0.0 --port 7864 --timeout-graceful-shutdown 20
fi

exec /app/deploy/docker-entrypoint.sh "$@"
