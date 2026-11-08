#!/bin/sh
set -eu

OPTIONS_FILE="/data/options.json"
ENV_FILE="/tmp/addon_env.sh"

umask 077
if [ ! -f "$OPTIONS_FILE" ]; then
  cat > "$ENV_FILE" <<'EOF'
export TZ='Asia/Shanghai'
EOF
  exit 0
fi

jq -r '
  {
    TZ: (.TZ // "Asia/Shanghai" | tostring),
    MAGPIE_PUBLIC_URL: (.MAGPIE_PUBLIC_URL // "" | tostring),
    MAGPIE_WEB_KEY: (.MAGPIE_WEB_KEY // "" | tostring),
    MAGPIE_ALLOW_IPS: (.MAGPIE_ALLOW_IPS // "" | tostring)
  }
  | to_entries[]
  | select(.value != "")
  | "export \(.key)=\(.value | @sh)"
' "$OPTIONS_FILE" > "$ENV_FILE"

jq -r '
  (.env_vars // [])[]
  | select(.name != null and .name != "")
  | select(.name | test("^[A-Za-z_][A-Za-z0-9_]*$"))
  | .name as $name
  | select(([
      "TZ",
      "MAGPIE_PUBLIC_URL",
      "MAGPIE_WEB_KEY",
      "MAGPIE_ALLOW_IPS"
    ] | index($name)) | not)
  | "export \($name)=\((.value // "") | tostring | @sh)"
' "$OPTIONS_FILE" >> "$ENV_FILE"
