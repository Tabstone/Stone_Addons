# TabS Cleaner

TabS Cleaner is a CleanMyMac-style storage care add-on for Home Assistant OS.

It provides:

- A modern storage health dashboard.
- HAOS storage scan and category summaries.
- Docker system and build-cache inspection.
- One-click safe cleanup.
- Checkbox-based deep cleanup.
- Cleanup history and audit records.
- Chinese and English UI, with Chinese enabled by default.

## Language

TabS Cleaner opens in Chinese by default. Use the language picker in the sidebar to switch between Chinese and English. The selected language is stored in the browser and does not change cleanup behavior or audit command allowlists.

## Safe Cleanup

Safe cleanup runs only low-risk actions:

```sh
docker builder prune -af
ha resolution healthcheck
```

It does not delete Docker volumes, stopped containers, images, backups, Home Assistant databases, add-on configuration, or files under `/mnt/data/docker/overlay2`.

## Deep Cleanup

Deep cleanup requires selecting explicit items and confirming that a recent backup exists.

The first version supports:

- Docker system prune without volumes, after confirmation.
- Unused Docker images.
- System journal vacuum.
- Selected backup deletion.
- Selected add-on repository deletion.

Deep cleanup items and their child items are marked as either recommended or not recommended. The recommendation engine is conservative:

- Backups are recommended only when they are old, unprotected, and have newer replacement backups.
- Add-on repositories are recommended only when Supervisor metadata does not show installed add-ons coming from that repository.
- Unknown repositories, official/local repositories, current backups, protected backups, Docker volumes, and Home Assistant database files are not recommended for deletion.
- Recommendations never bypass the deep-clean confirmation checkbox or explicit item selection.

## Smart Scan

The scan combines Docker `system df`, mapped Home Assistant directory sizes, backup metadata, journal usage, and Home Assistant database/log file sizes. It separates findings into:

- Safe: can be cleaned automatically without touching user data or persistent runtime data.
- Deep: can reclaim space, but needs explicit review and confirmation.
- Preserve: detected storage that should not be cleaned automatically.

Independent scan components run in parallel and return component timings. If a real HAOS install feels slow, check the "slowest component" value in the Smart Analysis panel before changing cleanup rules.

## Permissions

TabS Cleaner needs Supervisor API and Docker API access to inspect HAOS and Docker storage. Some cleanup operations can fail if the add-on is protected from write access to Docker. When that happens, the UI shows the command output and does not report success.

Home Assistant exposes add-on Docker API access as a restricted interface. TabS Cleaner therefore treats Docker cleanup as an audited best-effort operation: it never manually deletes Docker storage paths, and it records any permission failure instead of bypassing Supervisor protections.

## Recommended Workflow

1. Open TabS Cleaner.
2. Run Scan.
3. Review the dashboard.
4. Run Clean Safely.
5. Create or verify a full Home Assistant backup.
6. Use Deep Clean only for selected items you understand.
