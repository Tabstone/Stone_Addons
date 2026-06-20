#!/bin/sh
set -eu

OPTIONS_FILE="/data/options.json"
ENV_FILE="/tmp/addon_env.sh"

write_defaults() {
  cat > "$ENV_FILE" <<'EOF'
export NODE_ENV='production'
export PORT='3000'
export TZ='Asia/Shanghai'
export ADMIN_TOKEN='change-me'
export DSN=''
export REDIS_URL=''
export AUTO_MIGRATE='true'
export ENABLE_RATE_LIMIT='true'
export ENABLE_SECURE_COOKIES='false'
export AUTH_SESSION_TTL_SECONDS='604800'
export SESSION_TTL='300'
export DB_POOL_MAX='20'
export DB_POOL_IDLE_TIMEOUT='20'
export DB_POOL_CONNECT_TIMEOUT='10'
export MESSAGE_REQUEST_WRITE_MODE='async'
export MESSAGE_REQUEST_ASYNC_FLUSH_INTERVAL_MS='250'
export MESSAGE_REQUEST_ASYNC_BATCH_SIZE='200'
export MESSAGE_REQUEST_ASYNC_MAX_PENDING='5000'
export ENABLE_API_KEY_VACUUM_FILTER='true'
export ENABLE_API_KEY_REDIS_CACHE='true'
export API_KEY_AUTH_CACHE_TTL_SECONDS='60'
export API_TEST_TIMEOUT_MS='15000'
export MAX_RETRY_ATTEMPTS_DEFAULT='2'
export LANGFUSE_BASE_URL='https://cloud.langfuse.com'
export LANGFUSE_SAMPLE_RATE='1'
export LANGFUSE_DEBUG='false'
EOF
}

if [ ! -f "$OPTIONS_FILE" ]; then
  write_defaults
  exit 0
fi

jq -r '
  {
    NODE_ENV: "production",
    PORT: "3000",
    TZ: (.TZ // "Asia/Shanghai" | tostring),
    ADMIN_TOKEN: (.ADMIN_TOKEN // "change-me" | tostring),
    DSN: (.DSN // "" | tostring),
    REDIS_URL: (.REDIS_URL // "" | tostring),
    APP_URL: (.APP_URL // "" | tostring),
    AUTO_MIGRATE: ((if has("AUTO_MIGRATE") then .AUTO_MIGRATE else true end) | tostring),
    ENABLE_RATE_LIMIT: ((if has("ENABLE_RATE_LIMIT") then .ENABLE_RATE_LIMIT else true end) | tostring),
    ENABLE_SECURE_COOKIES: ((if has("ENABLE_SECURE_COOKIES") then .ENABLE_SECURE_COOKIES else false end) | tostring),
    AUTH_SESSION_TTL_SECONDS: (.AUTH_SESSION_TTL_SECONDS // 604800 | tostring),
    SESSION_TTL: (.SESSION_TTL // 300 | tostring),
    DB_POOL_MAX: (.DB_POOL_MAX // 20 | tostring),
    DB_POOL_IDLE_TIMEOUT: (.DB_POOL_IDLE_TIMEOUT // 20 | tostring),
    DB_POOL_CONNECT_TIMEOUT: (.DB_POOL_CONNECT_TIMEOUT // 10 | tostring),
    MESSAGE_REQUEST_WRITE_MODE: (.MESSAGE_REQUEST_WRITE_MODE // "async" | tostring),
    MESSAGE_REQUEST_ASYNC_FLUSH_INTERVAL_MS: (.MESSAGE_REQUEST_ASYNC_FLUSH_INTERVAL_MS // 250 | tostring),
    MESSAGE_REQUEST_ASYNC_BATCH_SIZE: (.MESSAGE_REQUEST_ASYNC_BATCH_SIZE // 200 | tostring),
    MESSAGE_REQUEST_ASYNC_MAX_PENDING: (.MESSAGE_REQUEST_ASYNC_MAX_PENDING // 5000 | tostring),
    ENABLE_API_KEY_VACUUM_FILTER: ((if has("ENABLE_API_KEY_VACUUM_FILTER") then .ENABLE_API_KEY_VACUUM_FILTER else true end) | tostring),
    ENABLE_API_KEY_REDIS_CACHE: ((if has("ENABLE_API_KEY_REDIS_CACHE") then .ENABLE_API_KEY_REDIS_CACHE else true end) | tostring),
    API_KEY_AUTH_CACHE_TTL_SECONDS: (.API_KEY_AUTH_CACHE_TTL_SECONDS // 60 | tostring),
    API_TEST_TIMEOUT_MS: (.API_TEST_TIMEOUT_MS // 15000 | tostring),
    MAX_RETRY_ATTEMPTS_DEFAULT: (.MAX_RETRY_ATTEMPTS_DEFAULT // 2 | tostring),
    LANGFUSE_PUBLIC_KEY: (.LANGFUSE_PUBLIC_KEY // "" | tostring),
    LANGFUSE_SECRET_KEY: (.LANGFUSE_SECRET_KEY // "" | tostring),
    LANGFUSE_BASE_URL: (.LANGFUSE_BASE_URL // "https://cloud.langfuse.com" | tostring),
    LANGFUSE_SAMPLE_RATE: (.LANGFUSE_SAMPLE_RATE // 1.0 | tostring),
    LANGFUSE_DEBUG: ((if has("LANGFUSE_DEBUG") then .LANGFUSE_DEBUG else false end) | tostring)
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
      "NODE_ENV",
      "PORT",
      "TZ",
      "ADMIN_TOKEN",
      "DSN",
      "REDIS_URL",
      "APP_URL",
      "AUTO_MIGRATE",
      "ENABLE_RATE_LIMIT",
      "ENABLE_SECURE_COOKIES",
      "AUTH_SESSION_TTL_SECONDS",
      "SESSION_TTL",
      "DB_POOL_MAX",
      "DB_POOL_IDLE_TIMEOUT",
      "DB_POOL_CONNECT_TIMEOUT",
      "MESSAGE_REQUEST_WRITE_MODE",
      "MESSAGE_REQUEST_ASYNC_FLUSH_INTERVAL_MS",
      "MESSAGE_REQUEST_ASYNC_BATCH_SIZE",
      "MESSAGE_REQUEST_ASYNC_MAX_PENDING",
      "ENABLE_API_KEY_VACUUM_FILTER",
      "ENABLE_API_KEY_REDIS_CACHE",
      "API_KEY_AUTH_CACHE_TTL_SECONDS",
      "API_TEST_TIMEOUT_MS",
      "MAX_RETRY_ATTEMPTS_DEFAULT",
      "LANGFUSE_PUBLIC_KEY",
      "LANGFUSE_SECRET_KEY",
      "LANGFUSE_BASE_URL",
      "LANGFUSE_SAMPLE_RATE",
      "LANGFUSE_DEBUG"
    ] | index($name)) | not)
  | "export \($name)=\((.value // "") | tostring | @sh)"
' "$OPTIONS_FILE" >> "$ENV_FILE"
