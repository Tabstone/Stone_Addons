# Changelog

## 0.1.142-1

- Sync upstream image [weishaw/sub2api:0.1.142](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.142](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.142).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - OpenAI Spark 影子账号：链接型影子账号（parent_account_id）复用母账号凭据/代理，独立走 spark 配额维度与用量窗口，一母一影强约束、母账号 429 与影子互不连坐
  - 适配 Claude Sonnet 5：模型白名单与 dateline 归一化路径打通
  - 抹除 Anthropic OAuth 请求中客户端 dateline 隐写指纹：对 /v1/messages 的 OAuth/setup-token 账号请求做 dateline 归一化，抹除撇号 / 日期分隔符隐写位；默认开启，可在系统设置切换
  - Grok 媒体（图像）路由：识别官方 grok 媒体模型 ID、路由 grok media 端点，并支持图像编辑上传转换
  - 用户使用记录列表默认显示“推理强度”列


## 0.1.141-1

- Sync upstream image [weishaw/sub2api:0.1.141](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.141](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.141).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - 用户用量分析对齐管理员：用户端 UsageView 重构为与管理员视角一致的统计指标、分组维度（端点/分组/模型分布）和图表展示
  - 修复订阅支付金额显示错误
  - **Docker:**
  - ```bash
  - docker pull weishaw/sub2api:0.1.141


## 0.1.140-1

- Sync upstream image [weishaw/sub2api:0.1.140](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.140](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.140).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - 新增 Grok CLI 兼容路由、API 密钥列表列设置与 OpenAI quota headroom 调度权重，
  - 并修复退款 pending、订阅金额显示、OpenAI 计费等多处问题。
  - Grok CLI 兼容：新增 Grok CLI 路由及 messages 兼容性支持
  - OAuth 邮箱补全：完善 OAuth 注册时的邮箱补全流程
  - API 密钥列表列设置：支持自定义显示列


## 0.1.139-1

- Sync upstream image [weishaw/sub2api:0.1.139](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.139](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.139).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - 新增 Grok 订阅、Codex 个人访问令牌（PAT）认证、GPT-5.5 Codex 指令支持，并加固 codex_cli_only 引擎指纹检测；同时修复多项支付、计费与网关稳定性问题。
  - Grok 订阅支持：完整的 OAuth、调度、配额探测与公开路由能力
  - Codex 个人访问令牌（PAT）上游认证
  - codex_cli_only 检测加固：统一引擎指纹信号列表，支持账号级 app-server
  - GPT-5.5 Codex 指令支持，作为最新版本回退


## 0.1.138-1

- Sync upstream image [weishaw/sub2api:0.1.138](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.138](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.138).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - 新增订阅推广返利与"优先最快重置账号"调度策略；适配新版 Claude Code CLI，并修复多家上游（Vertex / Gemini / OpenAI / GLM / 图像生成）的兼容性问题。
  - 订阅支付应用推广返利（affiliate rebate）
  - 账号调度支持「优先最快重置」可选策略
  - 更新 CC Switch 的 OpenAI 默认模型
  - 用量页显示缓存 Token 明细


## 0.1.137-1

- Sync upstream image [weishaw/sub2api:0.1.137](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.137](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.137).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - 新增 OpenAI 账号重置次数查询/触发重置、cyber_policy 硬阻断全链路透传。
  - OpenAI 账号重置次数：admin 端查询剩余重置次数、触发 rate-limit credit 消费
  - OpenAI cyber_policy：硬阻断响应全链路原样透传，异步审计/计费/会话拦截
  - Claude OAuth：可配置 system prompt blocks 注入
  - 国产 LLM 兜底定价：GLM 13 款、Kimi K 系列 4 款、MiniMax M 系列 6 款、DeepSeek V4 Pro/Flash


## 0.1.136-1

- Sync upstream image [weishaw/sub2api:0.1.136](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.136](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.136).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - Admin compliance acknowledgement: administrators must read and confirm the compliance statement before using admin features
  - Support for the claude-fable-5 model (including Bedrock and Antigravity platform adaptation, and frontend model selection)
  - Admin user list now supports filtering by API Key group (dedicated / public / subscription / disabled groups)
  - Optimized account group scheduling indexes for better scheduling performance
  - Reduced scheduler debug logging loop overhead


## 0.1.135-1

- Sync upstream image to 0.1.135.


## 0.1.134-1

- Sync upstream image to 0.1.134.


## 0.1.133-1

- Sync upstream image to 0.1.133.


## 0.1.132-1

- Sync upstream image to 0.1.132.


## 0.1.131-1

- Sync upstream image to 0.1.131.


## 0.1.130-1

- Sync upstream image to 0.1.130.


## 0.1.129-1

- Sync upstream image to 0.1.129.


## 0.1.127-1

- Sync upstream image to 0.1.127.


## 0.1.126-1

- Sync upstream image to 0.1.126.


## 0.1.125-1

- Sync upstream image to 0.1.125.


## 0.1.124-1

- Sync upstream image to 0.1.124.


## 0.1.123-1

- Sync upstream image to 0.1.123.


## 0.1.122-1

- Sync upstream image to 0.1.122.


## 0.1.121-1

- Sync upstream image to 0.1.121.


## 0.1.119-1

- Sync upstream image to 0.1.119.


## 0.1.117-1

- Sync upstream image to 0.1.117.


## 0.1.115-1

- Sync upstream image to 0.1.115.


## 0.1.114-1

- Sync upstream image to 0.1.114.


## 0.1.113-1

- Sync upstream image to 0.1.113.


## 0.1.112-1

- Sync upstream image to 0.1.112.


## 0.1.111-1

- Sync upstream image to 0.1.111.


## 0.1.110-1

- Sync upstream image to 0.1.110.


## 0.1.109-3

- Fix `jq` quoting in `env_vars` export generation so the add-on can start correctly.

## 0.1.109-2

- Switch upstream image source to `weishaw/sub2api:0.1.109`.

## 0.1.109-1

- Initial release wrapping `ghcr.io/tabstone/sub2api:0.1.109`.
