# Changelog

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
