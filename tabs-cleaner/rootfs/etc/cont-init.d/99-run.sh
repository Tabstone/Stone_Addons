#!/bin/sh
set -eu

OPTIONS_FILE="/data/options.json"
ENV_FILE="/tmp/addon_env.sh"

write_defaults() {
  cat > "$ENV_FILE" <<'EOF'
export PORT='8099'
export TABS_CLEANER_CONFIG_DIR='/config'
export TZ='Asia/Shanghai'
export JOURNAL_VACUUM_SIZE='300M'
export ENABLE_DEEP_CLEAN='true'
EOF
}

if [ ! -f "$OPTIONS_FILE" ]; then
  write_defaults
  exit 0
fi

jq -r '
  {
    PORT: "8099",
    TABS_CLEANER_CONFIG_DIR: "/config",
    TZ: (.TZ // "Asia/Shanghai" | tostring),
    JOURNAL_VACUUM_SIZE: (.JOURNAL_VACUUM_SIZE // "300M" | tostring),
    ENABLE_DEEP_CLEAN: ((if has("ENABLE_DEEP_CLEAN") then .ENABLE_DEEP_CLEAN else true end) | tostring)
  }
  | to_entries[]
  | "export \(.key)=\(.value | @sh)"
' "$OPTIONS_FILE" > "$ENV_FILE"
