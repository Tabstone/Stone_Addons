# Changelog

## 2.12.0-1

- Sync upstream image [ghcr.io/ithtelab/workbuddy-manager:2.12.0](https://github.com/ithtelab/workbuddy-manager/pkgs/container/workbuddy-manager).
- Upstream project: [ithtelab/workbuddy-manager](https://github.com/ithtelab/workbuddy-manager).
- Upstream release: [v2.12.0](https://github.com/ithtelab/workbuddy-manager/releases/tag/v2.12.0).
- Upstream changelog summary:
  - **请求日志区分「首帧」与「首字」**：新增首帧延迟（上游开始回话的时刻），
  - 与原有的首字延迟（第一个正文 token）并列显示。两者相差很大时，说明时间花在
  - 上游排队或模型思考上，而不是生成慢。
  - **账号页每页条数可选**：20 / 25 / 50 / 100，选择记在浏览器本地，刷新后保留。
  - **账号预警补齐详情**：每条预警现在带账号备注、触发的具体任务、HTTP 状态码与
  - 翻译后的错误说明；主页与账号页只在有「当前暂停」或未确认的新预警时显示顶栏。


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
