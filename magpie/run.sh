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

if [ "$#" -gt 0 ]; then
  exec gosu nonroot "$@"
fi

exec gosu nonroot /magpie web --addr 0.0.0.0:3430 --no-open
