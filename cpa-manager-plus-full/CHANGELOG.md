# Changelog

## 1.12.0-1

- Sync upstream image [seakee/cpa-manager-plus:v1.12.0](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.12.0](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.12.0).
- Upstream changelog summary:
  - > 196 commits · 552 files changed · +119770 / -24846
  - >
  - > v1.12.0-rc.3 → v1.12.0: 0 product commits · 0 product files changed
  - > [English ->](https://github.com/seakee/CPA-Manager-Plus/blob/v1.12.0/docs/release-notes/v1.12.0-en.md)
  - `v1.12.0` 是经过完整 RC 验证的 1.x 稳定版。产品源码与 `v1.12.0-rc.3` 完全一致，本次仅增加正式版发布材料并以 `VERSION=v1.12.0` 重新构建，因此不会引入 RC.3 之后的运行行为变化。此版本将统一的 Accounts...
  - `/accounts` 成为统一凭证管理入口，集中提供额度、配置、模型、活动、巡检与重新登录工作流，并适配桌面和移动端。


## 1.11.12-1

- Sync upstream image [seakee/cpa-manager-plus:v1.11.12](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.11.12](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.11.12).
- Upstream changelog summary:
  - > 16 commits · 71 files changed · +9754 / -872
  - > [English ->](https://github.com/seakee/CPA-Manager-Plus/blob/v1.11.12/docs/release-notes/v1.11.12-en.md)
  - 本版本聚焦大规模用量监控的查询性能、SQLite/WAL 状态可观测性和受保护的发布流程。Manager Server 为长窗口监控增加可恢复的派生数据与后台补齐机制，SQLite 存储状态现集中在系统信息页并适配桌面、平板和移动端；发布流程要求完成 `dev` 集成、`main` 晋级和来源校验后才创建标签。
  - 系统信息页提供 SQLite 存储状态模块，展示数据库、WAL、SHM、总占用和检查点状态，并采用桌面、平板和移动端响应式布局（`web/system-info`）。
  - Dashboard 移除 SQLite 存储卡片并恢复原有四列数据布局（`web/dashboard`）。
  - 7 天和 30 天监控分析会在派生数据覆盖后使用可恢复的 SQLite 读取路径，减少对大型 `usage_events` 原始表的扫描（`manager-server/monitoring`）。


## 1.11.11-1

- Sync upstream image [seakee/cpa-manager-plus:v1.11.11](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.11.11](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.11.11).
- Upstream changelog summary:
  - > 2 commits · 2 files changed · +65 / -14
  - > [English ->](https://github.com/seakee/CPA-Manager-Plus/blob/v1.11.11/docs/release-notes/v1.11.11-en.md)
  - 本安全补丁修复了 Manager Server 插件资源代理中的认证权限提升路径。未通过 CPAMP Admin Key 验证的插件资源请求不再隐式借用服务器已保存的 CPA Management Key；调用方自身的 Authorization 会保留转发，未提供认证时则由上游 CPA 或插件的公开资源策略决定。
  - `/v0/resource/plugins/*` 仅在请求携带有效的 CPAMP Admin Key 后才使用保存的 CPA Management Key；无认证的 GET/HEAD 请求不会再以管理权限访问上游插件资源（`manager-server/plugin-resource-proxy`）。
  - 所有已支持的插件资源 HTTP 方法现在遵循相同的权限边界：插件调用方携带的 Authorization 会原样转发，而无认证请求仍受上游 CPA 或插件的公开资源策略约束（`manager-server/plugin-resource-proxy`）。
  - `v1.5.0` 至 `v1.11.10` 受影响。若 Manager Server 曾可被不可信客户端访问，请尽快升级。


## 1.11.10-1

- Sync upstream image [seakee/cpa-manager-plus:v1.11.10](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.11.10](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.11.10).
- Upstream changelog summary:
  - > 22 commits · 112 files changed · +30546 / -2253
  - > [English ->](https://github.com/seakee/CPA-Manager-Plus/blob/v1.11.10/docs/release-notes/v1.11.10-en.md)
  - 本次发布聚焦本地成本估算精度、认证文件操作安全性和实时监控可读性。模型价格同步会优先使用 models.dev 的第一方官方元数据，并把上下文阶梯与 Fast/Priority service tier 应用于 Dashboard、监控和账户历史；认证文件变更会按规范凭据身份校验，实时请求表则统一采用总延迟 TPS。
  - 模型价格同步优先读取 models.dev catalog 的规范模型元数据，并依次使用 LiteLLM、OpenRouter 回退；只有唯一强身份匹配会自动保存，全部来源失败时会保留最后有效价格（`manager-server/model-pricing`）。
  - 解析、校验并持久化 models.dev 上下文价格阶梯与显式 Fast/Priority 费率，通过持久化定价汇总将其应用到 Dashboard、监控、账户历史和前端用量成本（`manager-server/usage-pricing`、`web/usage`）。
  - 模型价格页可只读展示同步的上下文阶梯和 service tier 规则，并按来源保留歧义候选；保存手动基础价格前会提示其将清除同步的高级规则（`web/model-prices`）。


## 1.11.9-1

- Sync upstream image [seakee/cpa-manager-plus:v1.11.9](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.11.9](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.11.9).
- Upstream changelog summary:
  - > 3 commits · 17 files changed · +781 / -172
  - > [English ->](https://github.com/seakee/CPA-Manager-Plus/blob/v1.11.9/docs/release-notes/v1.11.9-en.md)
  - 本次发布提升用量数据处理的可靠性，并加强高风险删除操作的保护。账户历史汇总可在并发写入期间稳定追上进度，大规模监控筛选不再触发 SQLite 条件上限，AI Provider 与认证文件的手动删除则增加目标明确的第二次确认。
  - 账户历史汇总在用量事件并发写入时会等待 SQLite 写入槽位，避免 WAL 快照失效导致汇总进度长期滞后（`manager-server/sqlite`）。
  - 监控筛选通过单个 JSON 参数处理大量认证索引、Provider 和账户，避免大规模已保存筛选返回 SQLite 变量上限错误（`manager-server/monitoring`）。
  - AI Provider 与认证文件的手动删除需要针对掩码目标、删除范围或受影响文件数完成第二次确认，降低永久误删风险（`web/providers-auth-files`）。


## 1.11.8-1

- Sync upstream image [seakee/cpa-manager-plus:v1.11.8](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.11.8](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.11.8).
- Upstream changelog summary:
  - > 3 commits · 27 files changed · +6402 / -272
  - > [English ->](https://github.com/seakee/CPA-Manager-Plus/blob/v1.11.8/docs/release-notes/v1.11.8-en.md)
  - 本次发布强化 Manager Server 凭证健康巡检的执行生命周期：跨实例使用可恢复的 SQLite 租约避免重复巡检，运行中的任务可由用户取消，服务重启及短暂 SQLite 写锁不会遗留无终态运行记录。
  - 凭证健康巡检通过数据库租约在多个 Manager Server 实例间保持单实例执行，避免同一批凭证被重复巡检或并发处理（`manager-server/codexinspection`）。
  - 运行中的凭证健康巡检可在监控面板请求停止；页面会显示取消中、已取消和中断状态，并保留已完成的结果与日志（`web/monitoring`）。
  - 服务启动会恢复过期的巡检租约，关闭过程会等待进行中的巡检写入终态；短暂 SQLite 写锁不再阻塞整个巡检生命周期（`manager-server/codexinspection`）。


## 1.11.7-1

- Sync upstream image [seakee/cpa-manager-plus:v1.11.7](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.11.7](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.11.7).
- Upstream changelog summary:
  - > 18 commits · 82 files changed · +16432 / -1171
  - > [English ->](https://github.com/seakee/CPA-Manager-Plus/blob/v1.11.7/docs/release-notes/v1.11.7-en.md)
  - 本次发布为用量数据引入可续传导入与持久化小时汇总，在保留原始事件和兼容回退路径的前提下，让大规模历史数据导入和监控分析更可靠。同时，凭证巡检会呈现更准确的执行结果与日志，已验证的付费 xAI OAuth 凭证将使用官方 API 完成真实推理检查，并修复编辑抽屉在拖选文本时意外关闭的问题。
  - 用量历史支持基于会话的分块上传、续传、取消与进度展示，可处理超过旧版单请求限制的大文件（`manager-server/usage`、`web/monitoring`）。
  - Dashboard 和用量分析可从持久化 UTC 小时汇总与最新原始数据共同读取；不支持的筛选条件和时区边界会安全回退到原始事件查询（`manager-server/usageaggregate`）。
  - 监控中心按当前标签加载分析数据，并将账户和 API Key 选择器与指标请求分离，减少无关标签的查询工作（`web/monitoring`）。


## 1.11.6-1

- Sync upstream image [seakee/cpa-manager-plus:v1.11.6](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.11.6](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.11.6).
- Upstream changelog summary:
  - > 11 commits · 61 files changed · +6692 / -1975
  - > [English ->](https://github.com/seakee/CPA-Manager-Plus/blob/v1.11.6/docs/release-notes/v1.11.6-en.md)
  - 本次发布将凭证健康巡检扩展到 Codex 与 xAI，并统一轻量 CPA Panel 的浏览器本地巡检和 Manager Server 的服务端巡检体验。xAI 默认采用计费优先检查，用户可按需启用最小化真实推理；结果页会区分计费、配额、认证、模型和推理故障，并提供响应式配置、脱敏失败详情与更清晰的运维入口。
  - 凭证健康巡检支持 Codex 与 xAI Provider，可在浏览器本地和 Manager Server 工作流中使用一致的配置、筛选、配额窗口与结果展示（`web/monitoring`、`manager-server/codexinspection`）。
  - xAI 巡检默认执行计费状态检查，并可显式启用基于待检凭据的最小化非流式 Responses 推理；模型、提示词与失败分类均按 Provider 处理（`web/monitoring`、`manager-server/codexinspection`）。
  - 巡检结果可区分计费、配额、认证、模型与推理故障，保留脱敏 HTTP 证据和可展开的完整失败详情，同时不在结果列表暴露 `auth_index`（`web/monitoring`）。


## 1.11.3-1

- Sync upstream image [seakee/cpa-manager-plus:v1.11.3](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.11.3](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.11.3).
- Upstream changelog summary:
  - > 26 commits · 154 files changed · +10034 / -2403
  - > [English ->](https://github.com/seakee/CPA-Manager-Plus/blob/v1.11.3/docs/release-notes/v1.11.3-en.md)
  - 本次发布补齐 xAI API Key Provider 管理与 Claude 模型级周额度展示，并修复付费 xAI OAuth 配额探测、安装器旧卷管理员密钥错配、客户端 API Key 复制和 Dashboard Token 构成等问题。中英文文档也围绕 Lightweight Panel 与 Full Mode 的实际任务完成重组。
  - 新增完整的 xAI API Key Provider 管理，支持新增、编辑、测试、启停、删除、优先级和运行时开关，并在 Dashboard、Monitoring 与 Usage Analytics 中正确识别 xAI 来源（`web/providers`、`web/monitoring`）。
  - Claude 配额卡片支持从现有 usage payload 展示模型级周额度，并在顶层账号额度缺失时安全恢复五小时与全模型周额度；重复、部分和异常记录会被稳定隔离和去重（`web/quota`）。
  - 付费 xAI OAuth 凭证无法访问 Grok CLI 账单接口时，可通过只读官方身份接口展示健康状态；该回退不会虚构额度、调用模型或自动恢复账号，并提供更明确的本地化诊断（`web/quota`、`manager-server/inspection`）。


## 1.11.2-1

- Sync upstream image [seakee/cpa-manager-plus:v1.11.2](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.11.2](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.11.2).
- Upstream changelog summary:
  - > 24 commits · 115 files changed · +12881 / -1413
  - > [English ->](https://github.com/seakee/CPA-Manager-Plus/blob/v1.11.2/docs/release-notes/v1.11.2-en.md)
  - 本次发布新增 xAI/Grok 账单优先的账号健康巡检与 Sub2API 账号导入，系统性加固账号自动化、CPA 响应处理和缓存 Token 统计口径，并将大库历史迁移改为后台可恢复执行。长窗口 Monitoring 查询也获得显著性能提升。
  - 新增本地与定时 xAI 账号巡检，通过账单接口检查周/月额度和账号状态，无需调用推理模型；同时支持 xAI OAuth 重新授权和带身份校验的失效凭证删除（`web/inspection`、`manager-server/inspection`）。
  - 支持直接上传或粘贴官方 Sub2API 账号导出，浏览器会将多个 OpenAI OAuth 账号转换为独立的 CPA Codex 认证文件，并准确报告部分上传失败（`web/auth-files`）。
  - Auth Files 新增需要重新授权、人工复核、自动禁用和额度冷却状态提示，帮助定位账号自动化决策（`web/auth-files`、`manager-server/account-actions`）。


## 1.11.1-1

- Sync upstream image [seakee/cpa-manager-plus:v1.11.1](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.11.1](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.11.1).
- Upstream changelog summary:
  - > 12 commits · 30 files changed · +2035 / -144
  - > [English ->](https://github.com/seakee/CPA-Manager-Plus/blob/v1.11.1/docs/release-notes/v1.11.1-en.md)
  - 本次发布提升 Usage Analytics 和 Dashboard 在大规模数据下的查询效率，修复细粒度缓存 Token 在统计页面中的展示遗漏，并修复 Windows 环境下 SQLite 数据库路径兼容性。
  - Usage Analytics 的概览、趋势、模型/API Key/凭据统计改为使用紧凑汇总数据，降低浏览器传输与处理开销（`web/usage-analytics`、`manager-server/usage-analytics`）。
  - 凭据趋势数据按需加载，避免在未打开明细时执行额外查询（`web/usage-analytics`）。
  - 在 SQLite 中预聚合凭据时间线和延迟分位数读取，减少历史使用事件扫描（`manager-server/usage-analytics`）。


## 1.11.0-1

- Sync upstream image [seakee/cpa-manager-plus:v1.11.0](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.11.0](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.11.0).
- Upstream changelog summary:
  - > 51 commits · 194 files changed · +12966 / -1862
  - > [English ->](https://github.com/seakee/CPA-Manager-Plus/blob/v1.11.0/docs/release-notes/v1.11.0-en.md)
  - 本次发布集中提升 Manager Server、Dashboard、Usage Analytics 和 Request Monitoring 的性能与长期运行稳定性，并新增 GPT-5.6 定价、长上下文计费和 xAI 免费额度耗尽后的自动冷却支持。同时修复缓存命中率、模型成本、并发配置保存、插件配置和 OAuth 兼容性问题。
  - 新增 GPT-5.6 官方定价、长上下文倍率、cache read/write 和 cache creation 成本计算，并支持模型别名与 service tier（`manager-server/pricing`、`web/model-prices`）。
  - xAI `free-usage-exhausted` 事件可触发受控的 24 小时自动冷却，恢复后自动解除 CPAMP 管理的禁用状态，并在 Auth Files 与自动化配置中展示对应状态（`manager-server/quota-cooldown`、`web/auth-files`）。
  - 对齐上游 v1.18 auth-files OAuth 兼容行为，并加固插件信任、配置更新和 provider 并发保存（`web/auth-files`、`web/plugins`、`web/providers`）。


## 1.10.5-1

- Sync upstream image [seakee/cpa-manager-plus:v1.10.5](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.10.5](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.10.5).
- Upstream changelog summary:
  - > 6 commits · 18 files changed · +1512 / -97
  - > [English ->](https://github.com/seakee/CPA-Manager-Plus/blob/v1.10.5/docs/release-notes/v1.10.5-en.md)
  - 本次发布聚焦前端配额可视化与插件安装体验。Quota 视图和监控账号行新增 xAI/Grok 周额度摘要，插件商店支持按 GitHub Release 或手动 tag 安装版本，同时修复 provider 与 quota 状态条在紧凑布局下的重叠和换行问题。
  - xAI/Grok quota 请求现在会同时获取周额度与月度账单数据，并合并为统一的 quota summary；Quota 卡片和监控账号行会展示周限制与产品用量（`web/quota`）。
  - 插件商店新增安装版本模式，可在 latest、GitHub Release 列表和手动 tag 之间选择，并支持 prerelease 切换、release 元数据缓存和多语言文案（`web/plugins`）。
  - 紧凑 quota 状态条改为固定 grid 轨道布局，让 block strip 和 rate badge 在认证文件与 provider 卡片中保持稳定宽度，减少窄卡片中的换行和拥挤（`web/quota`）。


## 1.10.4-1

- Sync upstream image [seakee/cpa-manager-plus:v1.10.4](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.10.4](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.10.4).
- Upstream changelog summary:
  - > 11 commits · 30 files changed · +2743 / -177
  - > [English ->](https://github.com/seakee/CPA-Manager-Plus/blob/v1.10.4/docs/release-notes/v1.10.4-en.md)
  - 本次发布聚焦账号历史统计与 provider 优先级管理。Manager Server 新增基于 SQLite 侧边汇总的账号历史统计能力，为账号级摘要读取提供低延迟数据源；前端则把 provider 优先级调整收敛到表格内直接编辑，并继续打磨监控 quota 信息与中文筛选文案。
  - Manager Server 新增 `usage_rollup_checkpoints` 和 `usage_account_model_rollups` SQLite 侧边汇总表、repository 与 Store 接入，用 `usage_events` 作为权威来源累计账号/模型历史请求、token、成本与成功率统计（`manager-...
  - 新增 `/v0/management/monitoring/account-history` API，支持最多 200 个账号目标、可选 catch-up，并返回 checkpoint/pending 状态、总请求数、成功/失败次数、总 token、成本、成功率和首末次出现时间（`manager-server/monitoring`）。
  - 新增账号历史汇总后台 worker，在服务启动、使用事件进入和定时检查时推进汇总 checkpoint，避免账号摘要读取同步扫描原始事件（`manager-server/worker`）。


## 1.10.3-1

- Sync upstream image [seakee/cpa-manager-plus:v1.10.3](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.10.3](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.10.3).
- Upstream changelog summary:
  - > 7 commits · 14 files changed · +1067 / -898
  - > [English ->](https://github.com/seakee/CPA-Manager-Plus/blob/v1.10.3/docs/release-notes/v1.10.3-en.md)
  - 本次补丁发布聚焦 quota 可见性、管理面板静态文件响应稳定性和用户文案打磨。前端现在能拆分 xAI 月度赠送额度与 pay-as-you-go 用量，Manager Server 为 `/management.html` 补齐 `Content-Length` 和静态文件响应语义，中文 README 也新增 Telegram 社区入口。
  - xAI quota 摘要和监控账号行现在区分月度赠送额度与按量付费用量，并在配置 on-demand 上限时展示剩余额度；未配置上限时显示禁用状态（`web/quota`）。
  - Manager Server 的 embedded panel 和 `PANEL_PATH` 管理面板响应补齐 `Content-Length`，`PANEL_PATH` 路径改用 `http.ServeContent`，改善 nginx/反向代理代理大体积 single-file HTML 时的下载稳定性，并覆盖 HEAD、range 和...
  - 监控账号 quota 条目移除 Kimi amount labels，避免不同 provider 的额度展示混杂（`web/monitoring`）。


## 1.10.2-1

- Sync upstream image [seakee/cpa-manager-plus:v1.10.2](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.10.2](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.10.2).
- Upstream changelog summary:
  - > 8 commits · 15 files changed · +1579 / -104
  - > [English ->](https://github.com/seakee/CPA-Manager-Plus/blob/v1.10.2/docs/release-notes/v1.10.2-en.md)
  - 本次补丁发布聚焦 auth files 和管理面板可读性的稳定性修复。Manager Server 在 CPA auth-files 大响应场景下改为流式定位目标账号，避免读取被截断影响 quota 和账号操作；前端会在 Codex cooldown 恢复或过期 usage header 检测后主动刷新 quota，并补齐导航、日志、监控和 auth...
  - Manager Server 的 quota 与账号操作路径改为流式查找 CPA auth-files 目标账号，并在新版 CPA 状态更新中传递 `auth_index`，避免大体积 auth-files 响应被截断后误判账号状态（`manager-server/auth-files`）。
  - Codex auth file quota 会在 CPAMP cooldown 恢复或 usage header 过期后自动刷新，避免 quota badge 继续显示旧窗口数据，同时保持 `authIndex` 隔离（`web/auth-files`）。
  - 展开的侧边栏恢复显示完整导航标签，短标签仍保留给紧凑导航场景使用（`web/navigation`）。


## 1.10.1-1

- Sync upstream image [seakee/cpa-manager-plus:v1.10.1](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.10.1](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.10.1).
- Upstream changelog summary:
  - > 17 commits · 36 files changed · +3084 / -174
  - > [English ->](https://github.com/seakee/CPA-Manager-Plus/blob/v1.10.1/docs/release-notes/v1.10.1-en.md)
  - 本次发布聚焦 native package 的后台控制能力、配额提供商适配和计费聚合准确性。原生包新增并加固后台启动/停止脚本,Antigravity 与 Codex quota 展示覆盖更多边界场景,Manager Server 也会在模型别名场景下回退到请求模型价格,避免通道聚合成本显示为 0。
  - 新增 native package 后台控制脚本,为 Unix 和 Windows 原生部署提供启动、停止、状态检查和 PID 文件管理能力(`native`)。
  - Antigravity quota 优先读取 summary 数据,并在 quota 卡片中展示订阅套餐信息,缺失 summary 时仍可回退到可用模型数据(`web/quota`)。
  - 批量 provider quota 刷新改为有界并发队列,降低分页或全量刷新时对上游 provider 的瞬时请求压力(`web/quota`)。


## 1.10.0-1

- Sync upstream image [seakee/cpa-manager-plus:v1.10.0](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.10.0](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.10.0).
- Upstream changelog summary:
  - > 33 commits · 167 files changed · +22962 / -2971
  - > [English ->](https://github.com/seakee/CPA-Manager-Plus/blob/v1.10.0/docs/release-notes/v1.10.0-en.md)
  - 本次发布聚焦部署落地、公开文档和可试用体验:新增引导式 CPAMP 部署脚本、双语文档站和隔离 demo runtime,同时补齐插件商店认证能力、Codex quota reset credit 展示以及 quota/监控 header 时序修复。
  - 新增引导式 CPAMP 部署脚本,覆盖 Docker full-stack、CPAMP-only Docker 和 native package 部署,并包含生成密钥、dry-run、重复执行、写入预检和启动健康检查(`installer`)。
  - 新增前端 mock demo runtime,复用真实页面和本地 fixture 数据,并将 demo build 限定在 `/demo` 路由下运行(`web/demo`)。
  - 插件商店支持版本选择、认证状态、平台 metadata 和 `plugins.store-auth` 可视化配置,安装指定旧版本时会等待用户显式选择(`web/plugins`)。


## 1.9.2-1

- Sync upstream image [seakee/cpa-manager-plus:v1.9.2](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.9.2](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.9.2).
- Upstream changelog summary:
  - > 15 commits · 52 files changed · +1925 / -524
  - > [English ->](https://github.com/seakee/CPA-Manager-Plus/blob/v1.9.2/docs/release-notes/v1.9.2-en.md)
  - 本次发布聚焦 AI Providers 配置体验与 Codex quota 可观测性:新增 reset credits 展示、Codex 连通性测试和跨 provider 的 disableCooling 配置开关,同时优化模型发现去重、插件 OAuth provider 识别和监控过滤器结构。
  - 在 Codex quota 状态中展示可用的 rate limit reset credits,并在专用接口不可用时保留 usage payload 计数回退(`web/quota`)。
  - 为 Claude、Codex、Gemini 和 OpenAI provider 增加 disableCooling 编辑字段与详情页快捷开关,支持乐观更新和失败回滚(`web/ai-providers`)。
  - 在 Codex provider 编辑抽屉中新增连通性测试,可选择测试模型并通过 `/v1/responses` 验证当前配置(`web/ai-providers`)。


## 1.9.1-1

- Sync upstream image [seakee/cpa-manager-plus:v1.9.1](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.9.1](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.9.1).
- Upstream changelog summary:
  - > 2 commits · 21 files changed · +1567 / -140
  - > [English ->](https://github.com/seakee/CPA-Manager-Plus/blob/v1.9.1/docs/release-notes/v1.9.1-en.md)
  - 本次补丁发布修复 Codex quota 在手动刷新、页面重载和多 auth file 场景下的状态持久化与隔离问题。前端现在会保留成功的手动 quota 刷新结果,并避免旧的 usage header 或检查结果覆盖更新、更准确的 quota 状态。
  - 持久化成功的手动 Codex quota 刷新结果,页面完整刷新后仍可复用最近一次有效结果(`web/quota`)。
  - 按 auth file identity 与 auth index 隔离 Codex quota 状态,避免同名文件或不同账号复用过期、错配的 quota 结果(`web/auth-files`)。
  - 当存在更新的 quota 或 header 数据时,抑制较旧的 Codex inspection 与 usage-header quota 信号,减少过期限额状态误报(`web/auth-files`, `web/quota`)。


## 1.8.1-1

- Sync upstream image [seakee/cpa-manager-plus:v1.8.1](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.8.1](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.8.1).
- Upstream changelog summary:
  - > 12 commits · 38 files changed · +1651 / -336
  - > [English ->](https://github.com/seakee/CPA-Manager-Plus/blob/v1.8.1/docs/release-notes/v1.8.1-en.md)
  - 本次发布改善 quota、实时监控与认证文件体验:新增 quota 账号与通知遮罩,让敏感账号信息更适合截图和共享;实时监控补充 reasoning token 展示并修复失败提示溢出;OpenAI provider、Antigravity 订阅和 reauth 检查结果也获得了更稳定的状态处理。
  - 新增 quota 账号遮罩,并在 quota 页面提供遮罩状态控制,降低截图或展示时暴露账号信息的风险(`web/quota`)。
  - 新增 quota 通知遮罩,让 quota 区块中的通知信息也能按当前隐私设置隐藏(`web/quota`)。
  - 为 reauth 检查结果增加显式删除入口,便于清理不再需要的检查记录(`web/monitoring`)。


## 1.7.0-1

- Sync upstream image [seakee/cpa-manager-plus:v1.7.0](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.7.0](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.7.0).
- Upstream changelog summary:
  - > 72 commits · 103 files changed · +23372 / -1083
  - > [English ->](https://github.com/seakee/CPA-Manager-Plus/blob/v1.7.0/docs/release-notes/v1.7.0-en.md)
  - 本次发布围绕监控与用量分析展开:新增完整的 Usage Analytics 工作区,将模型、API Key、凭证、热力图与异常明细统一到可钻取的分析视图中;后端同步扩展监控聚合、筛选、时区与执行上下文能力。Codex 检查、账号处理策略与仪表盘统计也获得了多项可用性和准确性修复。
  - 新增用量分析工作区,支持概览、趋势、模型、API Key、凭证与热力图钻取(`web/usage-analytics`)。
  - 用量分析筛选器、当前 tab 与 drilldown 状态可持久化,跨刷新保留分析上下文(`web/usage-analytics`)。
  - 引入共享 ECharts 渲染层,为监控与用量分析提供更丰富的图表呈现(`web/charts`)。


## 1.6.0-1

- Sync upstream image [seakee/cpa-manager-plus:v1.6.0](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.6.0](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.6.0).
- Upstream changelog summary:
  - > 18 commits · 98 files changed · +2310 / -2233
  - > [English ->](https://github.com/seakee/CPA-Manager-Plus/blob/v1.6.0/docs/release-notes/v1.6.0-en.md)
  - 本次发布聚焦 CPA Manager Plus 的 API 表面收敛与插件生态安全加固:后端清理了无效的短路径回退与多余的 worker helper,前端将第三方插件安装改为强制确认,同时新增 Codex 提供商联通性测试与 Claude 模型发现恢复,统一了出站 HTTP 超时。配套移除了 ampcode 提供商集成,文档同步更新。
  - 日志增量拉取支持 cursor 分页(`web/logs`)。
  - Codex 提供商联通性测试(编辑页)(`web/codex`)。
  - 第三方插件安装需输入 repo slug / plugin id 强制确认(`web/plugins`)。


## 1.4.2-1

- Sync upstream image [seakee/cpa-manager-plus:v1.4.2](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.4.2](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.4.2).
- Upstream changelog summary:
  - > 6 commits · 35 files changed · +2598 / -755
  - > [English ->](./v1.4.2-en.md)
  - 本次发布聚焦 Codex 配额体验与 provider 配置兼容性。管理端现在能识别 Codex Team 的月度配额窗口，避免短窗口耗尽时误判为账号不可用；前端补齐 reset-credit 消耗入口，并在 provider 编辑流程中保留 v1.16 新增字段，减少保存后配置丢失风险。
  - Codex 配额卡片支持 reset-credit 消耗操作，包含确认流程、状态刷新、reset 可用性与订阅元数据展示，以及本地化文案和测试覆盖。(`quota`, `web`)
  - Manager Server 将 Codex `plan_type` 纳入配额窗口分类，Team secondary window 缺少 duration 时会按月度配额处理，避免短窗口耗尽但月度配额仍可用时误停账号。(`manager-server`, `codexinspection`)
  - Provider 编辑 drawer、完整编辑页、API transformer 与 model entry helper 现在会保留 CPA v1.16 的 disable-cooling、Claude CCH signing、cloak cache-user-id、图片/思考模型元数据，并把未知原始字段合并回保存 payload。(`ai-...


## 1.4.1-1

- Sync upstream image [seakee/cpa-manager-plus:v1.4.1](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.4.1](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.4.1).
- Upstream changelog summary:
  - > 9 commits · 23 files changed · +3691 / -603
  - > [English ->](./v1.4.1-en.md)
  - 本次发布在 v1.4.0 的基础上收尾账号动作自动停用的诊断与可观测细节，统一 auth file 解析路径，并补齐 quota cooldown 的配置文档。AI Providers 的新增/编辑交互顺势合并到 drawer 与 tab 联动的流程中，进一步减少冗余入口切换；worker 与 collector...
  - AI Providers 新增/编辑配置改为 drawer 形式，并在已选中 provider tab 时支持直接新增，减少冗余入口切换。(`ai-providers`)
  - 账号动作 opt-in 自动停用补齐诊断日志，覆盖命中/跳过/成功/失败路径，便于复盘。(`account-actions`)
  - 监控账号状态停止跨 provider 串扰 auth file 元数据，provider 切换时身份信息保持一致。(`monitoring`)


## 1.3.0-1

- Sync upstream image [seakee/cpa-manager-plus:v1.3.0](https://hub.docker.com/r/seakee/cpa-manager-plus).
- Upstream project: [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus).
- Upstream release: [v1.3.0](https://github.com/seakee/CPA-Manager-Plus/releases/tag/v1.3.0).
- Upstream changelog summary:
  - > 7 commits · 28 files changed · +1819 / -296
  - > [English ->](./v1.3.0-en.md)
  - 本次发布继续增强 Auth Files 管理体验，新增账号级批量控制、账号补丁基础能力和更可读的默认认证文件名，减少批量导入、编辑和识别认证文件时的重复操作。同时，Codex 巡检会正确处理已停用 workspace，配置与巡检页面复用新的 segmented tabs 组件，提升多模式切换的一致性。
  - Auth Files 新增账号级批量控制，可在账号维度批量处理认证文件相关操作。(`auth-files`)
  - Auth Files 增加账号级 patch primitives，为更细粒度的认证账号更新提供基础能力。(`auth-files`)
  - Auth Files 生成更可读的默认认证文件名，降低导入后识别账号和来源的成本。(`auth-files`)


## 1.2.1-1

- Sync upstream image to v1.2.1.


## 1.1.1-1

- Sync upstream image to v1.1.1.


## 1.1.0-1

- Sync upstream image to v1.1.0.


## 1.0.1-1

- Add CPA Manager Plus full Docker mode as a Home Assistant add-on.
