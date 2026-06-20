# Claude Code Hub

Claude Code Hub 的 Home Assistant add-on 薄封装，直接复用上游官方镜像 `ghcr.io/ding113/claude-code-hub`。

## 部署形态

这个 add-on 只运行上游 `app` 服务：

- PostgreSQL 需要外部提供
- Redis 需要外部提供
- add-on 会持久化 Node 诊断报告目录 `/app/reports`

这样保持了上游 `docker-compose.yaml` 中的服务边界，不把数据库和 Redis 强行塞进应用镜像。

## 首次启动前必须配置

请在 add-on 配置页至少修改：

- `ADMIN_TOKEN`
- `DSN`
- `REDIS_URL`

示例：

```text
DSN=postgres://postgres:your-password@postgres-host:5432/claude_code_hub
REDIS_URL=redis://redis-host:6379
```

如果你通过 HTTP 访问 Home Assistant 内网地址，建议保持默认：

```text
ENABLE_SECURE_COOKIES=false
```

如果你通过 HTTPS 反代访问，可以改为 `true`。

## 持久化目录

首次启动后会在 `/addon_configs/<实际 add-on slug>/` 下创建：

```text
/addon_configs/<实际 add-on slug>/
  reports/
```

上游容器中的 `/app/reports` 会软链接到 `/config/reports`，用于保存 Node 诊断报告。

业务数据不在这个目录中；Claude Code Hub 的业务数据保存在你配置的 PostgreSQL 和 Redis 中。

## 访问方式

- Ingress：启用
- 容器端口：`3000`
- 默认宿主端口：`23000`
- Web UI：`http://homeassistant.local:23000/`

API 文档路径沿用上游：

- `/api/actions/scalar`
- `/api/actions/docs`

## 可选扩展环境变量

配置页里的 `env_vars` 可继续传递上游支持但本 add-on 未显式建模的环境变量，例如：

- `CSRF_SECRET`
- `FETCH_CONNECT_TIMEOUT`
- `FETCH_HEADERS_TIMEOUT`
- `FETCH_BODY_TIMEOUT`
- `ENABLE_ENDPOINT_CIRCUIT_BREAKER`
- `ENDPOINT_PROBE_INTERVAL_MS`
- 其他上游新增配置项

## 升级说明

- 该 add-on 直接使用上游官方 GHCR 镜像
- 仓库级同步 workflow 会检查官方 GHCR 标签
- 检测到新的上游版本后，会自动更新 add-on 的 `build.yaml`、`config.yaml.version` 和 `CHANGELOG.md`
