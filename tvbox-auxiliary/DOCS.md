# TVBox Auxiliary

TVBox Auxiliary 的 Home Assistant add-on 薄封装，直接复用上游官方镜像 `ghcr.io/nuu987/tvbox-auxiliary`。

## 部署形态

这个 add-on 对应上游 Docker Compose 中的单服务部署：

- 容器端口：`5678`
- Home Assistant 持久化目录：`/config/data`

上游镜像声明了 `VOLUME /app/data`，wrapper 不会删除或替换这个 Docker 挂载点；它会通过 `DATA_DIR=/config/data` 让应用直接把 Json 数据写入 Home Assistant 的持久化目录，然后继续执行上游命令 `node dist/server.js`。

## 首次启动前必须配置

请至少修改：

- `ADMIN_TOKEN`

建议同时配置：

- `BASE_URL`

`BASE_URL` 是服务对外可达地址。Docker/HA 部署建议填写，例如：

```text
http://homeassistant.local:5678
```

如果留空，上游会尝试自动识别局域网地址；在容器环境下可能提示 Docker 未配置 `BASE_URL`。

## 持久化目录

首次启动后会在 `/addon_configs/<实际 add-on slug>/` 下创建：

```text
/addon_configs/<实际 add-on slug>/
  data/
```

wrapper 会设置 `DATA_DIR=/config/data`。上游的 `config.json`、缓存资源、导出配置等 Json 文件都会保存在这里。

## 访问方式

- Ingress：启用，入口为 `/status`
- 容器端口：`5678`
- 默认宿主端口：`5678`
- Web UI：`http://homeassistant.local:5678/status`

常用路径：

- `/status`：状态页
- `/admin`：接口管理
- `/config`：TVBox 输出配置接口
- `/refresh`：手动刷新接口

## 选项说明

- `ADMIN_TOKEN`：管理后台 Bearer token，必须改成强密码。
- `BASE_URL`：服务对外可达地址，用于生成静态资源和代理地址。
- `CRON_SCHEDULE`：自动聚合 cron 表达式，例如 `0 5 * * *`。
- `REFRESH_TOKEN`：独立刷新接口访问令牌，通常可留空。
- `VERBOSE`：开启 debug 日志。
- `SPEED_TIMEOUT_MS`、`SITE_TIMEOUT_MS`、`FETCH_TIMEOUT_MS`：上游超时调优。
- `SCRAPE_SOURCE_URL`、`SCRAPE_SOURCE_REFERER`、`MACCMS_*`、`ZBAPE_API_KEY`：上游保留的高级抓取/资源站配置。
- `env_vars`：传递上游新增但本 add-on 未显式建模的环境变量。

## 升级说明

- `build.yaml` 固定上游 GHCR 镜像 tag，不使用 `latest`
- `config.yaml.version` 使用 Home Assistant add-on 版本，例如 `1.0.0-1`
- 仓库级同步 workflow 会检查上游 GHCR 标签，并更新 `build.yaml`、`config.yaml.version` 和 `CHANGELOG.md`
