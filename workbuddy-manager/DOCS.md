# WorkBuddy Manager

WorkBuddy Manager 的 Home Assistant add-on 薄封装，直接复用上游官方镜像
`ghcr.io/ithtelab/workbuddy-manager`。

## 与原始 Docker 命令的对应关系

上游 README 中的单容器命令只运行管理端：

```bash
docker run -d --name workbuddy-manager \
  -p 127.0.0.1:7864:7864 \
  -v /opt/workbuddy-manager/data:/app/data \
  ghcr.io/ithtelab/workbuddy-manager:latest
```

等价的 Docker Compose 配置如下，在配置所在目录执行 `docker compose up -d`：

```yaml
services:
  workbuddy-manager:
    image: ghcr.io/ithtelab/workbuddy-manager:latest
    container_name: workbuddy-manager
    ports:
      - "127.0.0.1:7864:7864"
    volumes:
      - /opt/workbuddy-manager/data:/app/data
```

这份 Compose 严格对应原命令，只持久化管理端数据。管理端还会在
`/opt/workbuddy2api` 写入账号凭据和网关配置；普通 Docker 部署如需保留它们，
应另加 `- /opt/workbuddy-manager/workbuddy2api:/opt/workbuddy2api` 卷映射。

本 add-on 保持单容器封装，同时持久化这两类数据：

```text
原始 Docker                  Home Assistant add-on
/opt/workbuddy-manager/data  /addon_configs/<完整加载项标识>/data
/app/data                    /app/data（软链接到 /config/data）
/opt/workbuddy2api            /config/workbuddy2api（账号凭据、网关配置和状态）
127.0.0.1:7864               7864/tcp
```

`<完整加载项标识>` 通常为 `<仓库ID>_workbuddy-manager`，仓库来源不同会使前缀不同。
不要仅按未带前缀的 `workbuddy-manager` 创建目录；应以 HA 实际提供的配置目录为准。

迁移已有数据时，先停止 add-on，再把原 `data` 目录内容复制到 Home Assistant
的 `/addon_configs/<完整加载项标识>/data/`。已有上游的 `config.json`、`auths/`
和 `data/` 则复制到同一级的 `workbuddy2api/` 目录，然后启动 add-on。

## 上游网关

上游镜像本身**不包含** `workbuddy2api` 网关。网关是独立服务，本 add-on 不会把它
塞进同一容器，也不会挂载宿主机的 `docker.sock`。

请先把上游网关运行起来，再在 add-on 配置中设置：

```text
WB2API_BASE=http://<网关地址>:7863
WB2API_KEY=<网关配置中的 api_key>
```

`WB2API_KEY` 留空时，管理端仍会尝试从本地上游配置文件读取密钥。若网关与管理端
不在同一个容器网络，请填写管理端实际可访问的地址，不要使用容器内的
`127.0.0.1`。

账号导入和网关设置会保存在 `/config/workbuddy2api`，但这些本地文件不会仅凭
`WB2API_BASE` 自动同步到远程网关。远程网关需要另行共享或同步 `config.json`
及 `auths/`；只设置 URL 和密钥不等于完成账号文件共享。

受此部署边界影响，面板里依赖 Docker 的操作（重建上游容器、读取上游容器日志、
在容器内一键更新上游）会降级为“请到宿主机操作”，这是预期行为。

## 配置项

| 选项 | 默认值 | 说明 |
| --- | --- | --- |
| `TZ` | `Asia/Shanghai` | 容器时区；影响按日统计与每日限额重置 |
| `WB_ADMIN_PASSWORD` | 空 | 首次启动创建管理员时使用的密码；留空则随机生成并打印到 add-on 日志 |
| `WB2API_BASE` | `http://127.0.0.1:7863` | 上游 `workbuddy2api` 网关地址 |
| `WB2API_KEY` | 空 | 上游网关密钥；留空则尝试读取本地上游配置 |
| `WB_SECURE_COOKIE` | `auto` | 会话 Cookie 的 Secure 策略：`auto`、`true`、`false` |
| `WB_CORS_ORIGINS` | 空 | 管理面 CORS 白名单，逗号分隔；同源访问时留空 |
| `WB_TRUST_PROXY` | `true` | 是否信任反向代理传入的真实 IP 头 |
| `WB_KEY_CUSTOM_ENABLED` | `false` | 是否允许创建自定义形态的网关密钥 |
| `env_vars` | 空 | 透传其他上游环境变量，例如 `WB_GITHUB_MIRROR`、`WB_HTTP_PROXY` |

管理员密码只在创建首个管理员时使用。已有 `users.json` 时修改该选项不会重置密码，
请在面板内修改。

## 首次启动

1. 启动 add-on。
2. 打开 add-on 日志。如果未设置 `WB_ADMIN_PASSWORD`，查找随机生成的初始密码。
3. 点击“打开 Web UI”，使用管理员账号登录。
4. 在面板中配置上游网关并添加账号。

本 add-on 未启用 Home Assistant Ingress：上游前端按根路径构建，并设置了
`frame-ancestors 'none'`，不适合通过 Ingress 子路径和 iframe 访问。请使用
`7864` 端口直连。

## 持久化与升级

管理端数据库、用户文件、日志和更新状态保存在 `/config/data`；上游账号凭据、
网关配置与状态保存在 `/config/workbuddy2api`。对应 HA 配置目录：

```text
/addon_configs/<完整加载项标识>/data/
/addon_configs/<完整加载项标识>/workbuddy2api/
```

`2.11.23-1` 只持久化了前者。如果旧容器中已有账号凭据或网关配置，应在更新前
先导出 `/opt/workbuddy2api/`，再按前述路径导入；旧容器已被删除的数据无法自动恢复。

add-on 版本跟随上游镜像，格式为 `上游版本-包装序号`，例如 `2.11.23-1`。仓库的
`sync-upstream.yml` 会检查 GHCR 标签，自动更新 `build.yaml`、`config.yaml` 的
版本和 `CHANGELOG.md`。

升级请通过 Home Assistant 的加载项更新流程。不要使用面板内的“系统更新”来更新
本 add-on：它更新的是容器可写层，重新创建加载项后会被上游镜像覆盖。升级前建议
备份整个 `/addon_configs/<完整加载项标识>/`。

## 安全提示

管理端持有账号凭据和网关密钥。Home Assistant add-on 的端口映射默认对整个局域网
开放，因此建议：

- 设置强管理员密码；
- 用防火墙限制 `7864` 的访问来源，或放在带 HTTPS 和访问控制的反向代理之后；
- 不要把管理端直接暴露到公网；
- 定期备份 `/addon_configs/<完整加载项标识>/`。
