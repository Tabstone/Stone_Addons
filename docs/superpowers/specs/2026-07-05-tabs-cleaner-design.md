# TabS Cleaner Design

## Goal

TabS Cleaner is a Home Assistant add-on that gives HAOS users a modern CleanMyMac-style storage dashboard, safe one-click cleanup, and explicit opt-in deep cleanup for higher-risk storage maintenance.

## Product Direction

The UI should feel like a contemporary system care application, not an old disk tree viewer. The first screen is a health dashboard with a large storage ring, a primary scan/clean action, and module cards. Detailed paths and command output are available, but they are secondary. Users should understand the storage problem before seeing raw Linux details.

The product model mirrors CleanMyMac-style flows:

1. Scan the system.
2. Review safe findings and riskier findings separately.
3. Run safe cleanup with one action.
4. Use deep cleanup only after selecting individual items.
5. Show a clear before/after report and persistent history.

## Information Architecture

The left navigation contains:

- Smart Clean: primary dashboard, scan button, safe cleanup summary.
- Storage Map: HAOS storage categories, Docker, supervisor data, backups, logs.
- Docker System: Docker images, containers, build cache, volumes, and reclaimable space.
- Add-on Data: large add-on config and data directories with non-destructive inspection.
- Backups: backup list, size, age, and manual deletion candidates.
- Health: Supervisor health, supported state, Resolution issues and suggestions.
- History: scan and cleanup audit records.

## Main Dashboard

The dashboard includes:

- A large circular storage health visualization with total, used, free, and risk status.
- A primary action button that starts as Scan and becomes Clean Safely after scan results are available.
- Four compact status cards: Docker cache, add-on data, backups, and HAOS health.
- A review section with three groups:
  - Safe to Clean
  - Review Needed
  - Not Recommended

## Safe Automatic Cleanup

Safe cleanup must avoid user-owned persistent data. The first version may run only these actions:

- Docker build cache cleanup: `docker builder prune -af`
- Resolution healthcheck refresh: `ha resolution healthcheck`

Safe cleanup must not run:

- `docker system prune --volumes`
- `docker system prune -f`
- `docker image prune -a`
- Manual deletion under `/mnt/data/docker/overlay2`
- Backup deletion
- Home Assistant database deletion
- Add-on config or data deletion

## Deep Cleanup

Deep cleanup is a separate view with checkboxes. It must never run without explicit selections and a confirmation flag.

Initial deep cleanup items:

- Docker system prune without volumes: `docker system prune -f`
- Unused Docker images: `docker image prune -af`
- Selected backups: delete only backups selected by slug.
- Journal vacuum: `journalctl --vacuum-size=<configured-size>`
- Stale corrupt repositories: remove selected store repositories only when no installed add-on uses the repository slug.

Deep cleanup cards show:

- Estimated reclaimable space when available.
- Risk badge: low, medium, or high.
- Exact command or API action in an expandable details panel.
- A confirmation checkbox before execution.

## Safety Model

The backend exposes only allowlisted actions. The UI cannot submit arbitrary shell commands.

Automatic cleanup is intentionally narrower than many community recovery recipes. It never removes containers, images, volumes, backups, recorder databases, add-on configs, or Docker storage-driver directories. Those items are either deep-clean selections or preserve/review findings.

Every cleanup action writes an audit record with:

- Timestamp.
- Mode: scan, safe_clean, deep_clean.
- Selected actions.
- Before and after storage snapshot when available.
- Command exit status.
- User-facing summary.
- Raw command output trimmed to a bounded size.

The add-on should detect missing permissions and report them clearly. If Docker cleanup is unavailable because Docker API access is read-only or protection mode blocks it, the UI should show the exact failing operation and the required add-on settings instead of pretending cleanup succeeded.

## Backend Architecture

Use Python standard library HTTP server for the first version to keep the image small and predictable. The backend provides:

- `GET /api/status`
- `POST /api/scan`
- `POST /api/clean/safe`
- `POST /api/clean/deep`
- `GET /api/history`
- `GET /api/config`

System integration boundaries:

- Docker data comes from `docker system df`, `docker ps`, and `docker images` when Docker CLI is available.
- Supervisor data comes from the Supervisor API when `SUPERVISOR_TOKEN` is present.
- Filesystem data comes from mapped HA add-on directories and safe `du` summaries.

## Frontend Architecture

Use a static HTML, CSS, and JavaScript frontend. Avoid a build pipeline in the first version. The UI uses:

- Responsive sidebar.
- Storage ring visualization.
- Modern cards with compact metrics.
- Segmented controls for Smart Clean, Deep Clean, and History.
- Checkbox-based deep cleanup list.
- Toast/status messages for long-running operations.

The UI should work inside Home Assistant Ingress and direct port access.

All static assets and API calls use relative URLs so that Home Assistant Ingress path prefixes stay inside the add-on instead of escaping to Home Assistant's own routes.

The UI is internationalized with Chinese as the default language and English as the secondary language. The language switch is client-side, stored in browser local storage, and must not change backend cleanup action identifiers or audit semantics.

## Add-on Packaging

Create a new add-on directory:

`tabs-cleaner/`

Required metadata:

- Name: TabS Cleaner
- Slug: `tabs-cleaner`
- Ingress enabled.
- Web UI port: `8099`
- `hassio_api: true`
- `hassio_role: admin`
- `docker_api: true`
- Mapped directories for read-only inspection where possible.
- Own `addon_config` writable for history.

Docker cleanup must respect the Docker capability Home Assistant exposes to add-ons. If that interface is restricted, TabS Cleaner records the failure and never bypasses Supervisor by deleting Docker storage directories directly.

## First Release Scope

Version `0.1.0-1` includes:

- Dashboard UI.
- Scan API.
- Safe cleanup API.
- Deep cleanup API with allowlisted initial actions.
- History persistence.
- Add-on metadata, docs, changelog, and repository README entry.
- Unit tests for cleanup allowlists, deep cleanup validation, and scan summarization.

Out of scope for the first version:

- Authentication beyond Home Assistant Ingress.
- Real-time websocket progress.
- Docker storage driver migration.
- Automatic add-on data deletion.
- Duplicate file scanning.
