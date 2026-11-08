# Magpie

Magpie 的 Home Assistant add-on 薄封装，复用上游官方容器镜像 `ghcr.io/yetone/magpie`。这个 add-on 运行无桌面环境下的 Magpie 网关和 Web 管理界面，Agent 本身仍运行在其他电脑上。

## 访问方式

- 网关：`http://<Home Assistant 主机>:3425`
- Web 管理界面：`http://<Home Assistant 主机>:3430/`
- OpenAI 兼容接口：`http://<Home Assistant 主机>:3425/v1`
- Anthropic 兼容接口：`http://<Home Assistant 主机>:3425`

容器启动时，Magpie 会在 add-on 日志中打印带 `?k=` 的完整 Web 登录链接。也可以手动打开 Web 管理界面，再粘贴日志中 `k=` 后面的密钥。

如果希望密钥在重启后保持不变，请把 `MAGPIE_WEB_KEY` 配置为至少 16 个字符，只使用字母、数字和 `- . _ ~`。留空时 Magpie 每次启动会生成临时密钥。

Web 管理界面可以查看和修改 provider、账号、网关密钥等敏感信息。只应通过可信局域网或 VPN 访问，不要直接暴露到公网。跨互联网使用时，应在上游前置 HTTPS 反向代理或 VPN。

## 网关密钥

来自容器外的请求必须携带已启用的 Magpie 网关密钥。首次打开 Web 管理界面后，进入 **网关 → 网关密钥** 创建密钥，并把生成的密钥填入其他电脑上的 Agent。

可以直接在 Web 管理界面给每台设备创建独立密钥，并为主要客户端配置每日、每周或每月额度。API key 不是 Magpie Web 登录密钥，两者不能混用。

## 持久化目录

add-on 使用 Home Assistant 的 `addon_config` 映射，并将整个上游 `/config` 数据目录持久化：

```text
/addon_configs/<实际 add-on slug>/
  magpie/   Magpie 设置、provider、网关密钥和路由组
  home/     ChatGPT、Claude、Codex 等账号登录信息
  cache/    模型目录、Bun 和按需下载的 Claude Code
  data/     Magpie 其他数据
  state/    Magpie 运行状态
```

升级或重装 add-on 时不要删除这个目录。账号登录、provider 凭据、插件和用量记录都在其中。

## 配置项

- `TZ`：时区，默认 `Asia/Shanghai`。
- `MAGPIE_PUBLIC_URL`：其他机器访问本实例时使用的网关地址，例如 `http://homeassistant.local:3425`。
- `MAGPIE_WEB_KEY`：固定 Web 管理界面登录密钥，留空时由 Magpie 临时生成。
- `MAGPIE_ALLOW_IPS`：允许访问网关和 Web 管理界面的 IP 或 CIDR 列表，多个值用逗号分隔。
- `env_vars`：透传上游支持但未显式建模的环境变量。名称必须以字母或下划线开头，后续只能包含字母、数字或下划线。

`MAGPIE_PUBLIC_URL` 只影响 Magpie 显示和提供给客户端的地址，不会改变监听端口。修改后需要重启 add-on。

## 登录订阅

ChatGPT、Claude 等订阅登录会在浏览器里跳回 `localhost` 回调地址。远程使用 Web 管理界面时，需要复制浏览器最终停留的完整回调 URL，粘贴回 Magpie 的登录页面。

Claude 订阅登录依赖 Claude Code。Magpie 会先说明下载版本、来源和保存位置，然后把官方构建保存到持久化的 `cache/` 目录。

## 升级

- `build.yaml` 固定上游镜像的明确版本 tag，不使用 `latest`。
- `config.yaml.version` 使用 `<upstream-version>-<wrapper-revision>`，供 Home Assistant 检测 add-on 升级。
- 仓库同步 workflow 会从 GHCR 读取最新稳定 semver tag，并同步 `build.yaml`、`config.yaml.version` 和 `CHANGELOG.md`。

上游 Docker 使用说明：<https://usemagpie.ai/docs/zh/docker>
