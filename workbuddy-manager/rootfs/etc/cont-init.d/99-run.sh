#!/bin/sh
set -eu

OPTIONS_FILE="/data/options.json"
ENV_FILE="/tmp/addon_env.sh"

write_defaults() {
  cat > "$ENV_FILE" <<'EOF'
export TZ='Asia/Shanghai'
export WB_ADMIN_PASSWORD=''
export WB2API_BASE='http://127.0.0.1:7863'
export WB2API_KEY=''
export WB_SECURE_COOKIE='auto'
export WB_CORS_ORIGINS=''
export WB_TRUST_PROXY='1'
export WB_KEY_CUSTOM_ENABLED='false'
EOF
}

if [ ! -f "$OPTIONS_FILE" ]; then
  write_defaults
  exit 0
fi

jq -r '
  {
    TZ: (.TZ // "Asia/Shanghai" | tostring),
    WB_ADMIN_PASSWORD: (.WB_ADMIN_PASSWORD // "" | tostring),
    WB2API_BASE: (.WB2API_BASE // "http://127.0.0.1:7863" | tostring),
    WB2API_KEY: (.WB2API_KEY // "" | tostring),
    WB_SECURE_COOKIE: (.WB_SECURE_COOKIE // "auto" | tostring),
    WB_CORS_ORIGINS: (.WB_CORS_ORIGINS // "" | tostring),
    WB_TRUST_PROXY: (if .WB_TRUST_PROXY == false then "0" else "1" end),
    WB_KEY_CUSTOM_ENABLED: ((if has("WB_KEY_CUSTOM_ENABLED") then .WB_KEY_CUSTOM_ENABLED else false end) | tostring)
  }
  | to_entries[]
  | "export \(.key)=\(.value | @sh)"
' "$OPTIONS_FILE" > "$ENV_FILE"

jq -r '
  (.env_vars // [])[]
  | select(.name != null and .name != "")
  | .name as $name
  | select(([
      "TZ",
      "WB_ADMIN_PASSWORD",
      "WB2API_BASE",
      "WB2API_KEY",
      "WB_SECURE_COOKIE",
      "WB_CORS_ORIGINS",
      "WB_TRUST_PROXY",
      "WB_KEY_CUSTOM_ENABLED"
    ] | index($name)) | not)
  | "export \($name)=\((.value // "") | tostring | @sh)"
' "$OPTIONS_FILE" >> "$ENV_FILE"
