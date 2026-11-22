# Changelog

## 2.11.23-2

- Persist upstream account credentials, gateway configuration, and state under `/config/workbuddy2api` so recreating or updating the add-on does not discard them.
- Translate the `WB_TRUST_PROXY` option to the upstream-required `1`/`0` values.
- Document the equivalent Docker Compose configuration and repository-prefixed Home Assistant data paths.

## 2.11.23-1

- Sync upstream image [ghcr.io/ithtelab/workbuddy-manager:2.11.23](https://github.com/ithtelab/workbuddy-manager/pkgs/container/workbuddy-manager).
- Upstream project: [ithtelab/workbuddy-manager](https://github.com/ithtelab/workbuddy-manager).
- Upstream release: [v2.11.23](https://github.com/ithtelab/workbuddy-manager/releases/tag/v2.11.23).
- Upstream changelog summary:
  - **Docker 部署起不来：容器反复重启，日志里只有一行 `su-exec: not found`**。
  - 2.11.22 的镜像漏装了两个启动时必需的工具，容器启动几毫秒后即以状态码 127
  - 退出，`restart: unless-stopped` 下无限重启、面板打不开。拉取新镜像并重建
  - 容器即可：
  - > 临时绕过：如果挂载目录属主已经是 `10001:10001`，可以在 `.env` 里设
  - > `WB_FIX_OWNERSHIP=0`，面板能先起来。
