# Stone_Addons

[English](README.md) | 中文

这是一个 Home Assistant add-on 仓库，用于收口一些原本需要单独通过 Docker 或 docker-compose 部署的服务。

仓库中的 add-on 采用薄封装思路：尽量直接复用上游镜像和启动逻辑，只补 Home Assistant 所需的目录映射、配置注入、启动包装、文档、图标和版本同步。

这里维护的是 add-on wrapper。各项目的核心实现、商标、版权和发布产物仍归原始上游仓库或镜像维护者所有。

## 安装

1. 打开 Home Assistant。
2. 进入 **设置** -> **加载项** -> **加载项商店**。
3. 打开右上角菜单，选择 **仓库**。
4. 添加以下仓库地址：

```text
https://github.com/Tabstone/Stone_Addons
```

## Add-ons

| Add-on | 目录 | 说明 | 上游项目地址 | 上游镜像地址 |
| --- | --- | --- | --- | --- |
| TrendRadar | `trendradar/` | 趋势分析服务，提供 Web UI 与通知能力 | [sansan0/TrendRadar](https://github.com/sansan0/TrendRadar) | [wantcat/trendradar](https://hub.docker.com/r/wantcat/trendradar) |
| TrendRadar MCP | `trendradar-mcp/` | TrendRadar 的 MCP 服务，复用主 add-on 数据 | [sansan0/TrendRadar](https://github.com/sansan0/TrendRadar) | [wantcat/trendradar-mcp](https://hub.docker.com/r/wantcat/trendradar-mcp) |
| CLI Proxy API | `cli-proxy-api/` | CLI Proxy API 服务，保留配置与鉴权目录 | [router-for-me/CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI) | [eceasy/cli-proxy-api](https://hub.docker.com/r/eceasy/cli-proxy-api) |
| CPA Manager Plus Full | `cpa-manager-plus-full/` | CPA Manager Plus 完整 Docker/Manager Server 模式，提供 SQLite 请求统计、模型价格和内置面板 | [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus) | [seakee/cpa-manager-plus](https://hub.docker.com/r/seakee/cpa-manager-plus) |
| CPA Manager Plus Panel | `cpa-manager-plus-panel/` | CPA Manager Plus 的 CPA panel 模式辅助 add-on，用于区分纯 CPA 自托管面板，不运行 Manager Server | [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus) | [seakee/cpa-manager-plus](https://hub.docker.com/r/seakee/cpa-manager-plus) |
| AxonHub | `axonhub/` | AI 网关与模型代理平台，默认 SQLite 单容器封装 | [looplj/axonhub](https://github.com/looplj/axonhub) | [looplj/axonhub](https://hub.docker.com/r/looplj/axonhub) |
| atvloadly | `atvloadly/` | Apple TV IPA 侧载与自动刷新服务，保留配对和签名数据 | [bitxeno/atvloadly](https://github.com/bitxeno/atvloadly) | [ghcr.io/bitxeno/atvloadly](https://github.com/bitxeno/atvloadly/pkgs/container/atvloadly) |
| drpy-node | `drpy-node/` | drpyS Node.js 服务，保留配置、订阅、源文件和缓存目录 | [hjdhnx/drpy-node](https://github.com/hjdhnx/drpy-node) | [ghcr.io/hjdhnx/drpy-node](https://github.com/users/hjdhnx/packages/container/package/drpy-node) |
| Microsoft Rewards Script | `microsoft-rewards-script/` | Microsoft Rewards 自动任务脚本，后台 cron 运行并保留配置与浏览器会话 | [TheNetsky/Microsoft-Rewards-Script](https://github.com/TheNetsky/Microsoft-Rewards-Script) | [ghcr.io/thenetsky/microsoft-rewards-script](https://github.com/TheNetsky/Microsoft-Rewards-Script/pkgs/container/microsoft-rewards-script) |
| Mihomo | `mihomo/` | Mihomo 核心，保留配置目录并映射宿主网络能力 | [MetaCubeX/mihomo](https://github.com/MetaCubeX/mihomo) | [metacubex/mihomo](https://hub.docker.com/r/metacubex/mihomo) |
| MetaCubeXD | `metacubexd/` | Mihomo 的 Web UI | [MetaCubeX/metacubexd](https://github.com/MetaCubeX/metacubexd) | [ghcr.io/metacubex/metacubexd](https://github.com/MetaCubeX/metacubexd/pkgs/container/metacubexd) |
| Metapi | `metapi/` | Metapi AI API 聚合管理与统一代理，默认持久化 SQLite 数据目录 | [cita-777/metapi](https://github.com/cita-777/metapi) | [1467078763/metapi](https://hub.docker.com/r/1467078763/metapi) |
| Sub2API | `sub2api/` | Sub2API 独立网关封装，依赖外部 PostgreSQL 与 Redis | [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api) | [weishaw/sub2api](https://hub.docker.com/r/weishaw/sub2api) |

## 维护方式

- 每个 add-on 都尽量跟随上游镜像版本，不重写上游业务逻辑。
- 仓库级 GitHub Actions 会检查上游镜像版本，并自动同步 `build.yaml`、`config.yaml.version` 与 `CHANGELOG.md`。
- 同步 workflow 生成 changelog 时会优先补充上游 release 或 tag 链接；如果上游没有发布说明，则降级写入上游项目地址和镜像地址。
- 具体的使用方式、持久化目录、端口和配置项说明，请查看各 add-on 目录下的 `DOCS.md`。
