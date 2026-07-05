#!/bin/sh
set -eu

OPTIONS_FILE="/data/options.json"
ENV_FILE="/tmp/addon_env.sh"

write_defaults() {
  cat > "$ENV_FILE" <<'EOF'
export PORT='5678'
export DATA_DIR='/config/data'
export TZ='Asia/Shanghai'
export ADMIN_TOKEN='change-me'
export SPEED_TIMEOUT_MS='5000'
export SITE_TIMEOUT_MS='3000'
export FETCH_TIMEOUT_MS='30000'
export VERBOSE='false'
EOF
}

if [ ! -f "$OPTIONS_FILE" ]; then
  write_defaults
  exit 0
fi

jq -r '
  {
    PORT: "5678",
    DATA_DIR: "/config/data",
    TZ: (.TZ // "Asia/Shanghai" | tostring),
    ADMIN_TOKEN: (.ADMIN_TOKEN // "change-me" | tostring),
    BASE_URL: (.BASE_URL // "" | tostring),
    CRON_SCHEDULE: (.CRON_SCHEDULE // "" | tostring),
    REFRESH_TOKEN: (.REFRESH_TOKEN // "" | tostring),
    VERBOSE: ((if has("VERBOSE") then .VERBOSE else false end) | tostring),
    SPEED_TIMEOUT_MS: (.SPEED_TIMEOUT_MS // 5000 | tostring),
    SITE_TIMEOUT_MS: (.SITE_TIMEOUT_MS // 3000 | tostring),
    FETCH_TIMEOUT_MS: (.FETCH_TIMEOUT_MS // 30000 | tostring),
    SCRAPE_SOURCE_URL: (.SCRAPE_SOURCE_URL // "" | tostring),
    SCRAPE_SOURCE_REFERER: (.SCRAPE_SOURCE_REFERER // "" | tostring),
    MACCMS_API_URL: (.MACCMS_API_URL // "" | tostring),
    MACCMS_AES_KEY: (.MACCMS_AES_KEY // "" | tostring),
    MACCMS_AES_IV: (.MACCMS_AES_IV // "" | tostring),
    ZBAPE_API_KEY: (.ZBAPE_API_KEY // "" | tostring)
  }
  | to_entries[]
  | select(.value != "")
  | "export \(.key)=\(.value | @sh)"
' "$OPTIONS_FILE" > "$ENV_FILE"

jq -r '
  (.env_vars // [])[]
  | select(.name != null and .name != "")
  | .name as $name
  | select(([
      "PORT",
      "DATA_DIR",
      "TZ",
      "ADMIN_TOKEN",
      "BASE_URL",
      "CRON_SCHEDULE",
      "REFRESH_TOKEN",
      "VERBOSE",
      "SPEED_TIMEOUT_MS",
      "SITE_TIMEOUT_MS",
      "FETCH_TIMEOUT_MS",
      "SCRAPE_SOURCE_URL",
      "SCRAPE_SOURCE_REFERER",
      "MACCMS_API_URL",
      "MACCMS_AES_KEY",
      "MACCMS_AES_IV",
      "ZBAPE_API_KEY"
    ] | index($name)) | not)
  | "export \($name)=\((.value // "") | tostring | @sh)"
' "$OPTIONS_FILE" >> "$ENV_FILE"
