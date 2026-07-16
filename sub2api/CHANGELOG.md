# Changelog

## 0.1.156-1

- Sync upstream image [weishaw/sub2api:0.1.156](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.156](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.156).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - OpenAI 账号支持 Codex Agent Identity 认证，前端标明认证模式
  - 账号管理新增安全的一键复制功能
  - /keys 与 /admin/groups 列表新增可选 ID 列
  - Server-Timing 指标扩展至已认证用户 Web API
  - OpenAI WebSocket 首消息超时支持配置


## 0.1.155-1

- Sync upstream image [weishaw/sub2api:0.1.155](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.155](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.155).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - Grok 渠道健康监控：监控中心支持 Grok 平台健康检查，新导入的 OAuth 账号自动探活，账号列表显示 Free 计划徽标
  - Grok Web SSO 批量导入：批量粘贴 SSO key 自动转换为 Build OAuth 账号，失败自动跳过并汇总结果（原账号类型页的 SSO 卡片入口已移除）
  - 系统日志支持按主机名过滤
  - 管理后台新增可选开启的服务端耗时指标采集（server timing）
  - Grok 免费账号配额改用滚动 24 小时估算，并改进免费配额探测与用量展示


## 0.1.153-1

- Sync upstream image [weishaw/sub2api:0.1.153](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.153](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.153).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - Grok 视频编辑与延长：网关新增视频 edit/extension 端点支持
  - Apple 容器部署：新增 apple-container.sh 部署脚本及配套文档
  - 账号编辑弹窗支持手动覆盖 OpenAI 订阅档位 plan_type（仅 OAuth 账号）
  - API Key 列表最近使用 IP 查询性能优化，并新增数据库索引
  - 内嵌静态资源设置长效 Cache-Control，直接部署时浏览器不再重复下载控制台资源


## 0.1.152-1

- Sync upstream image [weishaw/sub2api:0.1.152](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.152](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.152).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - Grok 平台能力大幅增强：新增 xAI API Key 账号支持与免费 OAuth 提示词缓存；Codex alpha/search 网页搜索接入转发并支持按次计费。
  - Grok 支持 xAI API Key 账号：可在管理后台创建/编辑，支持 Responses 转发与连接测试
  - Grok 免费 OAuth 账号启用提示词缓存，可缓存对话请求自动经 Responses 链路转发
  - Codex alpha/search 网页搜索端点转发与按次计费：默认 $0.01/次，分组可设覆盖价（0 为免费），实际扣费叠加分组倍率，前端表单实时预览单次价格
  - Chat 兼容桥支持 tool_search 服务端工具与 custom 工具，Codex exec 与 MCP 工具在 chat-only 上游可正常使用


## 0.1.151-1

- Sync upstream image [weishaw/sub2api:0.1.151](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.151](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.151).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - OpenAI Fast/Flex 策略支持用户级规则：规则可指定生效用户，用户专属规则优先于全局规则，便于为特定用户配置例外
  - 修复 Codex 上游 originator 与 User-Agent 错配导致请求 404 的问题，覆盖普通转发、透传、WebSocket、用量探针与账号测试等路径
  - 修复 GPT-5.6 计费与用量统计问题：补齐价格识别与模型别名匹配，完善用量统计口径
  - 修复 Grok Responses 接口丢失 reasoning effort 参数的问题，兼容的参数将被保留
  - 修复 Codex 图像生成时 image_gen 命名空间声明未正确剥离的问题


## 0.1.150-1

- Sync upstream image [weishaw/sub2api:0.1.150](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.150](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.150).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - GPT-5.6 缓存写入计费：支持 cache write token 独立计价与用量统计
  - parallel_tool_calls 兼容映射：Chat Completions 与 Responses API 互转时保留该字段（含显式 false）
  - GPT-5.6 计费与官方定价对齐，显式配置的缓存写入价格优先生效
  - 升级 Codex 客户端版本至 0.144.1，修复 gpt-5.6-luna 模型请求 404
  - 加固计费并发与支付恢复流程，防止并发场景下的余额与订阅状态异常


## 0.1.146-1

- Sync upstream image [weishaw/sub2api:0.1.146](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.146](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.146).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - API Key 并发统计：密钥列表实时展示并发使用情况
  - 账号请求头覆写：API Key 类型账号支持自定义 Anthropic/OpenAI 请求头（含敏感头禁止覆写防护）
  - 账号数据导入：支持拖拽上传和批量导入账号数据
  - 适配 OpenAI 新模型 gpt-5.6-sol/terra/luna，开放 Grok 图像生成计价配置
  - 订阅套餐编辑器支持预览人民币扣费金额


## 0.1.144-1

- Sync upstream image [weishaw/sub2api:0.1.144](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.144](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.144).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - 修复高并发下用量日志静默丢失导致的对账缺口问题；新增 Anthropic Fable 专属 7d_oi 窗口的模型级限流支持，触发限流不再误伤整个账号。
  - Anthropic 账号支持 Fable 专属 7d_oi 限流窗口：仅该窗口触发 429 时按模型级限流处理（其他模型正常调度），账号列表新增 "7d F" 用量进度条
  - 错误请求列表全面对齐用量明细：支持排序、筛选、列设置，新增分类过滤（管理端与用户端）
  - Codex 图像工具策略：账号级四态控制（跟随渠道/强制注入/不注入/全部拦截），支持剥离图像生成工具
  - 数据库迁移超时时间支持配置


## 0.1.143-1

- Sync upstream image [weishaw/sub2api:0.1.143](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.143](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.143).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - 订阅分组新增高峰时段倍率能力；OpenAI WebSocket 新增 http_bridge ingress 模式。
  - 订阅分组高峰时段倍率：支持为分组配置高峰时段与倍率，倍率信息全链路透传至可用渠道、支付计划与结算信息
  - OpenAI WebSocket 新增 http_bridge ingress 模式及账号级 WS 选择器
  - 支持恢复已撤销的订阅
  - 用量记录新增 IP 地理位置查询与展示


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
