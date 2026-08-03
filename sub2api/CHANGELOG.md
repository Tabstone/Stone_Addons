# Changelog

## 0.1.170-1

- Sync upstream image [weishaw/sub2api:0.1.170](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.170](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.170).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - 新增分组级利润控制，可按账号成本倍率过滤调度候选，避免请求被分给成本高于分组定价的账号；上游计费倍率探测扩展到全部 API Key 平台账号并支持自动写回账号倍率；修复 Anthropic 流式响应中断时部分用量丢失导致漏计费的问题。
  - 分组级利润控制（默认关闭）：为 OpenAI / Anthropic / Gemini / Grok / Antigravity 分组开启后，按「最低利润率 + 安全缓冲」过滤调度候选，成本倍率过高的账号不参与调度；排序、评分、粘性会话与熔断在合格账号之间行为不变
  - 利润控制：槽位获取后二次复核账号倍率，超阈值账号释放槽位并重新选号；粘性会话仅在终检通过后绑定，超阈值的粘性账号跳过而非解绑，倍率恢复后自动回归
  - 利润控制：请求级定价时刻，同一请求在等待、重试、切换账号过程中不会因跨越高峰窗口而改变判定基准
  - 利润控制范围：组合分组不支持直接开启；图片、视频、模型列表、用量、count_tokens 等非 Token 计费路径不纳入门控


## 0.1.169-1

- Sync upstream image [weishaw/sub2api:0.1.169](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.169](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.169).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - 修复网关上游 URL 路径片段校验缺陷（GHSA-vrxq-qm4h-6hgg），v0.1.135 ~ v0.1.168 用户建议尽快升级；同时修复 release 产物缺少定价兜底资源、以及代理断流熔断可能导致「无可用账号」的问题。
  - 收紧上游 URL 路径片段校验：`/responses` 子路径、Gemini 模型名等客户端可控片段在参与上游请求路径拼接前统一走闭集允许清单校验，不合规请求在入口即被拒绝（GHSA-vrxq-qm4h-6hgg，影响 v0.1.135 ~ v0.1.168，由 @KKBK-233 报告）
  - 容器部署默认启用 no-new-privileges，阻止应用进程提权
  - 安全审计：兼容 Qwen3Guard 输出中的辅助字段
  - 更新 GPT-5.6 Luna 与 Terra 的计费费率


## 0.1.168-1

- Sync upstream image [weishaw/sub2api:0.1.168](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.168](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.168).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - 新增 Passkey（通行密钥）免密登录与模型广场页面；修复升级后安全审计配置丢失死锁、Claude OAuth 缓存断点丢失等多项问题。
  - Passkey 认证：个人资料页可注册/管理通行密钥并用于免密登录，管理员可在系统设置中控制登录开关，注册与撤销需验证账号密码
  - 模型广场：新增公开模型广场页面，按分组展示各平台模型定价，管理员可配置展示范围
  - Kimi K3 模型支持：新增计费与思考协议适配，并正确识别 1M 上下文后缀
  - 账号模型白名单选择器支持一键复制模型 ID


## 0.1.166-1

- Sync upstream image [weishaw/sub2api:0.1.166](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.166](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.166).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - 新增面板 API 限流保护，防止高频请求冲击数据库；修复 WebSocket 多轮会话计费、模型映射统计口径等多项计费与统计准确性问题。
  - 面板 API 限流：管理后台可配置面板接口限流策略，认证接口按用户、公开接口按真实 IP 限流，保护数据库免受高频请求冲击
  - Antigravity OpenAI 兼容转发全面加固，并拒绝仅含 usage 的非流式空响应
  - Codex Responses 与 Anthropic 协议互转兼容性完善（工具调用配对等场景）
  - 伪装的 Claude Code CLI 版本号升级到 2.1.220


## 0.1.165-1

- Sync upstream image [weishaw/sub2api:0.1.165](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.165](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.165).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - 新增 ChatGPT Live（Frameless 实时会话）网关支持，并完整适配 Anthropic 新模型 claude-opus-5。
  - ChatGPT Live 网关：新增 `/v1/live` 与 Codex `/backend-api/codex/realtime/calls` 实时会话转发，支持组级 Live 开关、并发租约控制与用量记录，用量筛选/导出新增 Live 请求类型
  - 适配 Anthropic claude-opus-5：模型清单、Bedrock 默认映射、定价（$5/$25 per MTok、1M 上下文、128K 输出）、前端预设映射与限流 scope 全部登记
  - Ollama Cloud 用量改为请求驱动刷新：空闲账号不再轮询，新增「请求安静等待」参数（默认 1 分钟），原刷新周期改为持续请求下的最长等待时间
  - 用量记录持久化客户端会话标识 session_id，可用于跨请求关联同一会话


## 0.1.164-1

- Sync upstream image [weishaw/sub2api:0.1.164](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.164](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.164).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - 新增聚合分组能力，一个分组可按模型路由规则将请求分发到不同平台的子分组；Ollama 账号支持 Cloud 官方用量自动刷新。
  - 聚合分组：新增 composite 平台类型分组，可配置模型路由规则，将不同模型的请求分发到已关联的各平台子分组，支持模型别名与路由预览，计费按实际转发的具体模型结算
  - Ollama Cloud 用量同步：Ollama 账号支持自动刷新 Cloud 官方用量
  - 支付宝移动端支付：预下单支持深链拉起支付宝客户端完成支付
  - OpenAI 账号测试默认使用具体模型 gpt-5.6-sol，不再优先别名 gpt-5.6


## 0.1.163-1

- Sync upstream image [weishaw/sub2api:0.1.163](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.163](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.163).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - 分组新增 OpenAI 推理策略控制，可按分组约束推理力度；修复优雅关停超时导致缓冲用量/计费记录丢失的问题，并集中修复多处移动端布局适配。
  - 分组级 OpenAI 推理策略：支持设置推理力度上限与精确映射，HTTP 与 WebSocket 转发统一强制执行
  - Grok 兼容 /responses/compact 端点：compact 请求可调度 Grok 账号，并支持链式中继的受保护视频下载
  - Redis 连接支持 ACL 用户名配置
  - 调度器快照发布减少临时分配，降低发布路径开销


## 0.1.161-1

- Sync upstream image [weishaw/sub2api:0.1.161](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.161](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.161).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - 安全防护全面开关化：敏感操作 step-up 2FA 与会话 IP/UA 绑定均改为默认关闭、按需开启，避免升级后误锁定；同时修复 Grok 受保护视频内容访问及一系列媒体链路问题。
  - 敏感操作 step-up 2FA 总开关（默认关闭）：开启后，账号/代理导出、备份创建/下载/恢复、S3 配置修改、提升管理员等操作需在 15 分钟内完成过 TOTP 验证
  - 会话 IP/UA 绑定默认改为关闭（功能保留，可在设置页开启），避免 IP 变动导致登录掉线
  - 安全开关保存字段改为可空：旧客户端全量保存设置不再静默重置安全开关
  - 入口拒绝日志降噪，并强化网关鉴权边界


## 0.1.160-1

- Sync upstream image [weishaw/sub2api:0.1.160](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.160](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.160).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - 新增独立的提示词安全审计引擎：通过 OpenAI 兼容审计节点对用户提示词进行风险扫描，配套完整的管理端审计控制台；修复 Grok 媒体生成的多个可用性问题。
  - 提示词安全审计引擎（默认关闭）：支持配置多个 OpenAI 兼容审计节点（优先级排序、连通性探测、API Key 加密存储），对用户最新提示词异步扫描并记录审计事件；与现有内容审核引擎完全独立，互不影响
  - 审计控制台：管理端新增运行态总览、审计节点池管理、策略配置与事件复查界面，支持保留完整提示词快照、事件筛选与一键删除筛选器
  - 修复 Grok 媒体生成多个问题：参考图 payload 归一化处理；无媒体权限的账号自动隔离并在调度时跳过；修复调度器缓存丢失媒体资格标记导致隔离失效的问题
  - 修复被动携带 image_gen namespace 的请求误触发 403 的问题：仅显式图像生成意图才要求 Responses capability，权限检查与并发槽位判定同步修正


## 0.1.159-1

- Sync upstream image [weishaw/sub2api:0.1.159](https://hub.docker.com/r/weishaw/sub2api).
- Upstream project: [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api).
- Upstream release: [Sub2API 0.1.159](https://github.com/Wei-Shaw/sub2api/releases/tag/v0.1.159).
- Upstream changelog summary:
  - > AI API Gateway Platform - 将 AI 订阅配额分发和管理
  - 修复 v0.1.157 起纯 APIKey 分组无法使用 OpenAI 独立搜索的回归；反向代理部署下审计日志与会话 IP 绑定现在能正确记录真实客户端 IP。
  - 管理端账号列表：支持从 API Key 账号名称直接跳转到上游站点
  - Grok Free 账号：/v1/responses 及 WS 桥接携带函数工具时同样启用免费提示词缓存路由，并处理与内置 web_search 工具重名的冲突
  - 前端 Stripe 支付依赖改为按需加载，未使用支付功能时不再加载相关脚本
  - 修复 v0.1.157 起纯 APIKey 分组调用 OpenAI 独立搜索时无可用账号的问题；混合分组中不支持该端点的 APIKey 账号遇 404/405 自动切换账号，不再误写账号错误状态


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
