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

export PYTHONPATH="/opt${PYTHONPATH:+:$PYTHONPATH}"
exec python3 -m tabs_cleaner.server
