# Changelog

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

- Add CPA Manager Plus CPA panel mode helper as a Home Assistant add-on.
