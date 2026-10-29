# Changelog

## 1.1.1-1

- Sync upstream image [ghcr.io/nuu987/tvbox-auxiliary:v1.1.1](https://github.com/nuu987/tvbox-auxiliary/pkgs/container/tvbox-auxiliary).
- Upstream project: [nuu987/tvbox-auxiliary](https://github.com/nuu987/tvbox-auxiliary).
- Upstream release: [v1.1.1](https://github.com/nuu987/tvbox-auxiliary/releases/tag/v1.1.1).
- Upstream changelog summary:
  - 包含重大变更的更新通常不兼容旧数据，需清除后重建。
  - 重大变更：
  - **新增聚合时若现存接口不可用默认自动复用最后成功的缓存**
  - **重构添加接口功能，优化速度与体验**
  - **移除并不再支持内嵌式直播源**
  - 主要更新：


## 1.0.0-1

- Initial Home Assistant add-on wrapper for upstream image `ghcr.io/nuu987/tvbox-auxiliary:v1.0`.
- Upstream release: [v1.0 正式版](https://github.com/nuu987/tvbox-auxiliary/releases/tag/v1.0).
- Persist upstream Json data through `DATA_DIR=/config/data`.
