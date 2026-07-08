# Changelog

## 1.19.28-1

- Sync upstream image [metacubex/mihomo:v1.19.28](https://hub.docker.com/r/metacubex/mihomo).
- Upstream project: [MetaCubeX/mihomo](https://github.com/MetaCubeX/mihomo).
- Upstream release: [v1.19.28](https://github.com/MetaCubeX/mihomo/releases/tag/v1.19.28).
- Upstream changelog summary:
  - ea19cda0 feat: add `rematch` outbound type and `REMATCH-NAME` rule type (#2862) by @Peter Solomon
  - d20e8508 feat: support custom peer-info for openvpn outbound (#2926) by @Easy-Ez
  - 1686d563 feat: convert support `session-table` and `session-length` for `xhttp-opts` fields (#2889) by @legiz-ru
  - 01111ffa feat: add `handshake-timeout` for masque by @wwqgtxx
  - 1c4f7c4d feat: support shadow-tls for snell by @wwqgtxx
  - 1f80d915 feat: support `session-table` and `session-length` for xhttp client by @wwqgtxx


## 1.19.27-1

- Sync upstream image to v1.19.27.


## 1.19.26-1

- Sync upstream image to v1.19.26.


## 1.19.25-1

- Sync upstream image to v1.19.25.


## 1.19.24-1

- Sync upstream image to v1.19.24.


## 1.19.23-1

- Sync upstream image to v1.19.23.


## 1.19.22-1

- Sync upstream image to v1.19.22.


## 1.19.21-10

- Sync upstream image to v1.19.21.


## 1.19.21-9

- Expose external controller to LAN and add default secret.

## 1.19.21-8

- Fix entrypoint to run /mihomo.

## 1.19.21-7

- Restore default config template and avoid mountpoint removal errors.

## 1.19.21-6

- Restore host_pid/host_ipc settings.

## 1.19.21-5

- Drop host_pid/host_ipc and set explicit capabilities.

## 1.19.21-4

- Remove bundled default config template.

## 1.19.21-3

- Update privileged schema to list format.

## 1.19.21-2

- Update default config template.

## 1.19.21-1

- Initial Home Assistant add-on wrapper for metacubex/mihomo v1.19.21.
