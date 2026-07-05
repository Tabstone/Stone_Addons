from __future__ import annotations

import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable
from urllib.parse import unquote, urlparse

from tabs_cleaner.core import analyze_scan, build_deep_plan, build_safe_plan, human_bytes, parse_size_to_bytes, summarize_storage


APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
CONFIG_DIR = Path(os.environ.get("TABS_CLEANER_CONFIG_DIR", "/config"))
HISTORY_FILE = CONFIG_DIR / "history.json"
PORT = int(os.environ.get("PORT", "8099"))
MAX_OUTPUT_BYTES = 12_000


SCAN_PATHS = [
    ("backups", "/backup"),
    ("homeassistant", "/homeassistant"),
    ("share", "/share"),
    ("media", "/media"),
    ("ssl", "/ssl"),
    ("addon_configs", "/addon_configs"),
    ("addons", "/addons"),
    ("own_config", "/config"),
]


def main() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"TabS Cleaner listening on :{PORT}", flush=True)
    server.serve_forever()


class Handler(BaseHTTPRequestHandler):
    server_version = "TabSCleaner/0.1"

    def do_HEAD(self) -> None:
        request_path = urlparse(self.path).path
        if request_path in ("/", "/index.html"):
            path = STATIC_DIR / "index.html"
            self.send_response(HTTPStatus.OK)
            self.send_header("content-type", "text/html; charset=utf-8")
            self.send_header("content-length", str(path.stat().st_size if path.exists() else 0))
            self.end_headers()
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_GET(self) -> None:
        request_path = urlparse(self.path).path
        if request_path in ("/", "/index.html"):
            self._send_static("index.html", "text/html; charset=utf-8")
            return
        if request_path.startswith("/static/"):
            filename = unquote(request_path.removeprefix("/static/"))
            content_type = "text/plain"
            if filename.endswith(".css"):
                content_type = "text/css; charset=utf-8"
            elif filename.endswith(".js"):
                content_type = "application/javascript; charset=utf-8"
            self._send_static(filename, content_type)
            return
        if request_path == "/api/status":
            self._send_json({"ok": True, "name": "TabS Cleaner", "version": "0.1.0"})
            return
        if request_path == "/api/history":
            self._send_json({"history": load_history()})
            return
        if request_path == "/api/config":
            self._send_json(
                {
                    "safe_actions": build_safe_plan(),
                    "deep_actions": deep_action_catalog() if deep_clean_enabled() else [],
                    "deep_clean_enabled": deep_clean_enabled(),
                    "journal_vacuum_size": journal_vacuum_size(),
                }
            )
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        payload = self._read_json()
        request_path = urlparse(self.path).path
        if request_path == "/api/scan":
            self._send_json(scan_system())
            return
        if request_path == "/api/clean/safe":
            self._send_json(run_cleanup("safe_clean", build_safe_plan(), payload))
            return
        if request_path == "/api/clean/deep":
            if not deep_clean_enabled():
                self._send_json({"ok": False, "error": "Deep cleanup is disabled in add-on options."}, status=403)
                return
            try:
                plan = build_deep_plan(
                    payload.get("actions", []),
                    confirmed=bool(payload.get("confirmed")),
                    journal_vacuum_size=payload.get("journal_vacuum_size", journal_vacuum_size()),
                    backup_slugs=payload.get("backup_slugs", []),
                    repository_slugs=payload.get("repository_slugs", []),
                )
            except ValueError as exc:
                self._send_json({"ok": False, "error": str(exc)}, status=400)
                return
            self._send_json(run_cleanup("deep_clean", plan, payload))
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"{self.address_string()} - {fmt % args}", flush=True)

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("content-length") or 0)
        if length <= 0:
            return {}
        data = self.rfile.read(length)
        try:
            return json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            return {}

    def _send_json(self, payload: dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "application/json; charset=utf-8")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_static(self, filename: str, content_type: str) -> None:
        path = (STATIC_DIR / filename).resolve()
        if STATIC_DIR.resolve() not in path.parents and path != STATIC_DIR.resolve():
            self.send_error(HTTPStatus.FORBIDDEN)
            return
        if not path.exists() or not path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        data = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("content-type", content_type)
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def scan_system() -> dict[str, Any]:
    started = time.time()
    scan_tasks = run_parallel_tasks(
        {
            "storage": lambda: build_storage_snapshot(supervisor_get("/host/disks/default/usage") or {}),
            "docker": docker_snapshot,
            "backups": backups_snapshot,
            "resolution": resolution_snapshot,
            "homeassistant": homeassistant_snapshot,
            "journal": journal_snapshot,
            "path_profiles": mapped_path_profiles,
            "store": store_snapshot,
        }
    )
    task_results = scan_tasks["results"]
    storage = task_results.get("storage", {})
    docker = task_results.get("docker", {})
    backups = task_results.get("backups", {})
    resolution = task_results.get("resolution", {})
    homeassistant = task_results.get("homeassistant", {})
    journal = task_results.get("journal", {})
    path_profiles = task_results.get("path_profiles", {})
    store = task_results.get("store", {})

    result = {
        "ok": True,
        "duration_ms": int((time.time() - started) * 1000),
        "timings": {**scan_tasks["timings"], "total": int((time.time() - started) * 1000)},
        "storage": storage,
        "docker": docker,
        "backups": backups,
        "resolution": resolution,
        "homeassistant": homeassistant,
        "journal": journal,
        "path_profiles": path_profiles,
        "store": store,
        "safe_actions": decorate_plan(build_safe_plan(), docker=docker),
        "deep_actions": deep_action_catalog(backups=backups, docker=docker, journal=journal, store=store, storage=storage)
        if deep_clean_enabled()
        else [],
        "deep_clean_enabled": deep_clean_enabled(),
        "journal_vacuum_size": journal_vacuum_size(),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    result["intelligence"] = analyze_scan(result)
    append_history({"mode": "scan", "summary": scan_summary(result), "result": compact_result(result)})
    return result


def run_parallel_tasks(tasks: dict[str, Callable[[], Any]]) -> dict[str, Any]:
    if not tasks:
        return {"results": {}, "timings": {}}

    results: dict[str, Any] = {}
    timings: dict[str, int] = {}
    max_workers = min(8, max(1, len(tasks)))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {executor.submit(run_timed_task, task): name for name, task in tasks.items()}
        for future in as_completed(future_map):
            name = future_map[future]
            try:
                value, duration_ms = future.result()
            except Exception as exc:
                value = {"available": False, "error": str(exc)}
                duration_ms = 0
            results[name] = value
            timings[name] = duration_ms
    return {"results": results, "timings": timings}


def run_timed_task(task: Callable[[], Any]) -> tuple[Any, int]:
    started = time.time()
    value = task()
    return value, int((time.time() - started) * 1000)


def run_cleanup(mode: str, plan: list[dict[str, Any]], payload: dict[str, Any]) -> dict[str, Any]:
    before = scan_light()
    results = []
    for step in plan:
        command = step["command"]
        result = run_command(command, timeout=300)
        results.append({**step, "result": result})
        if not result["ok"] and not step.get("optional"):
            break
    after = scan_light()
    report = {
        "ok": all(item["result"]["ok"] or item.get("optional") for item in results),
        "mode": mode,
        "before": before,
        "after": after,
        "results": results,
        "requested": payload,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    append_history({"mode": mode, "summary": cleanup_summary(report), "result": compact_result(report)})
    return report


def build_storage_snapshot(host_usage: dict[str, Any]) -> dict[str, Any]:
    total = first_number(host_usage, ["total", "total_bytes", "size"])
    used = first_number(host_usage, ["used", "used_bytes"])
    free = first_number(host_usage, ["free", "free_bytes", "available"])
    if not total:
        df = run_command(["df", "-k", "/"], timeout=10)
        total, used, free = parse_df_k(df["stdout"])

    categories = mapped_path_sizes()
    if total and used:
        summary = summarize_storage({"total": total, "used": used, "free": free, "categories": categories})
    else:
        summary = summarize_storage({"total": 0, "used": 0, "free": 0, "categories": categories})
    summary["category_human"] = {name: human_bytes(value) for name, value in categories.items()}
    return summary


def mapped_path_sizes() -> dict[str, int]:
    categories: dict[str, int] = {}
    for name, path in SCAN_PATHS:
        if not Path(path).exists():
            continue
        result = run_command(["du", "-sk", path], timeout=60)
        if result["ok"]:
            try:
                kb = int(result["stdout"].split()[0])
            except (IndexError, ValueError):
                kb = 0
            categories[name] = kb * 1024
    return categories


def mapped_path_profiles() -> dict[str, Any]:
    profiles: dict[str, Any] = {}
    for name, path in SCAN_PATHS:
        if not Path(path).exists():
            continue
        profiles[name] = {"path": path, "top_entries": top_path_entries(path)}
    return profiles


def top_path_entries(path: str, limit: int = 8) -> list[dict[str, Any]]:
    result = run_command(["find", path, "-mindepth", "1", "-maxdepth", "1", "-exec", "du", "-sk", "{}", "+"], timeout=60)
    if not result["ok"]:
        return []
    return parse_du_k_lines(result["stdout"], limit=limit)


def parse_du_k_lines(text: str, limit: int = 8) -> list[dict[str, Any]]:
    entries = []
    for line in text.splitlines():
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            continue
        try:
            size_bytes = int(parts[0]) * 1024
        except ValueError:
            continue
        entries.append({"path": parts[1], "name": Path(parts[1]).name, "size_bytes": size_bytes, "size": human_bytes(size_bytes)})
    return sorted(entries, key=lambda item: item["size_bytes"], reverse=True)[:limit]


def homeassistant_snapshot() -> dict[str, Any]:
    base = Path("/homeassistant")
    database = file_profile(base / "home-assistant_v2.db")
    wal = file_profile(base / "home-assistant_v2.db-wal")
    shm = file_profile(base / "home-assistant_v2.db-shm")
    logs = [
        profile
        for profile in [
            file_profile(base / "home-assistant.log"),
            file_profile(base / "home-assistant.log.1"),
            file_profile(base / "home-assistant.log.fault"),
        ]
        if profile.get("exists")
    ]
    return {
        "available": base.exists(),
        "database": database,
        "database_wal": wal,
        "database_shm": shm,
        "logs": logs,
    }


def file_profile(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"path": str(path), "exists": False, "size_bytes": 0, "size": "0 B"}
    try:
        size = path.stat().st_size
    except OSError:
        size = 0
    return {"path": str(path), "name": path.name, "exists": True, "size_bytes": size, "size": human_bytes(size)}


def journal_snapshot() -> dict[str, Any]:
    result = run_command(["journalctl", "--disk-usage"], timeout=10)
    size_bytes = parse_journal_disk_usage(result["stdout"] if result["ok"] else "")
    return {
        "available": result["ok"],
        "size_bytes": size_bytes,
        "size": human_bytes(size_bytes),
        "raw": result["stdout"],
        "error": result["stderr"] if not result["ok"] else "",
    }


def parse_journal_disk_usage(text: str) -> int:
    return parse_size_to_bytes(text)


def docker_snapshot() -> dict[str, Any]:
    system_df = run_command(["docker", "system", "df"], timeout=60)
    ps = run_command(["docker", "ps", "-a", "--size", "--format", "{{.Names}}\t{{.Status}}\t{{.Size}}"], timeout=60)
    images = run_command(["docker", "images", "--format", "{{.Repository}}:{{.Tag}}\t{{.Size}}"], timeout=60)
    return {
        "available": system_df["ok"],
        "system_df": parse_docker_system_df(system_df["stdout"]),
        "raw_system_df": system_df["stdout"],
        "containers": parse_table_lines(ps["stdout"], ["name", "status", "size"]),
        "images": parse_table_lines(images["stdout"], ["image", "size"]),
        "errors": [r["stderr"] for r in (system_df, ps, images) if not r["ok"] and r["stderr"]],
    }


def backups_snapshot() -> dict[str, Any]:
    raw = run_command(["ha", "backups", "list", "--raw-json"], timeout=60)
    if not raw["ok"]:
        return {"available": False, "backups": [], "error": raw["stderr"] or raw["stdout"]}
    try:
        data = json.loads(raw["stdout"])
        backups = data.get("data", {}).get("backups", [])
    except json.JSONDecodeError:
        backups = []
    return {"available": True, "backups": backups}


def resolution_snapshot() -> dict[str, Any]:
    raw = run_command(["ha", "resolution", "info", "--raw-json"], timeout=60)
    if not raw["ok"]:
        return {"available": False, "issues": [], "suggestions": [], "error": raw["stderr"] or raw["stdout"]}
    try:
        data = json.loads(raw["stdout"]).get("data", {})
    except json.JSONDecodeError:
        data = {}
    return {
        "available": True,
        "issues": data.get("issues", []),
        "suggestions": data.get("suggestions", []),
        "unhealthy": data.get("unhealthy", []),
        "unsupported": data.get("unsupported", []),
    }


def store_snapshot() -> dict[str, Any]:
    store = supervisor_get("/store") or {}
    repositories = supervisor_get("/store/repositories") or []
    addons = supervisor_get("/addons") or {}

    store_addons = normalize_supervisor_list(store.get("addons", []) if isinstance(store, dict) else [])
    repository_items = normalize_supervisor_list(repositories)
    installed_addons = normalize_supervisor_list(addons.get("addons", []) if isinstance(addons, dict) else [])

    if not store_addons and not repository_items and not installed_addons:
        return {"available": False, "repositories": [], "addons": [], "installed_addons": []}

    return {
        "available": True,
        "repositories": repository_items,
        "addons": store_addons,
        "installed_addons": installed_addons,
    }


def normalize_supervisor_list(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        for key in ("repositories", "addons", "data"):
            nested = value.get(key)
            if isinstance(nested, list):
                return [item for item in nested if isinstance(item, dict)]
    return []


def scan_light() -> dict[str, Any]:
    return {
        "storage": build_storage_snapshot(supervisor_get("/host/disks/default/usage") or {}),
        "docker": docker_snapshot(),
    }


def supervisor_get(path: str) -> dict[str, Any] | None:
    token = os.environ.get("SUPERVISOR_TOKEN")
    if not token:
        return None
    url = f"http://supervisor{path}"
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None
    if isinstance(payload, dict) and payload.get("result") == "ok":
        return payload.get("data", payload)
    return payload if isinstance(payload, dict) else None


def run_command(command: list[str], timeout: int = 120) -> dict[str, Any]:
    started = time.time()
    try:
        completed = subprocess.run(command, text=True, capture_output=True, timeout=timeout, check=False)
        stdout = trim_output(completed.stdout)
        stderr = trim_output(completed.stderr)
        return {
            "ok": completed.returncode == 0,
            "returncode": completed.returncode,
            "stdout": stdout,
            "stderr": stderr,
            "duration_ms": int((time.time() - started) * 1000),
        }
    except FileNotFoundError as exc:
        return {"ok": False, "returncode": 127, "stdout": "", "stderr": str(exc), "duration_ms": 0}
    except subprocess.TimeoutExpired as exc:
        return {
            "ok": False,
            "returncode": 124,
            "stdout": trim_output(exc.stdout or ""),
            "stderr": f"Timed out after {timeout}s",
            "duration_ms": int((time.time() - started) * 1000),
        }


def parse_docker_system_df(text: str) -> list[dict[str, str]]:
    rows = []
    for line in text.splitlines():
        if not line.strip() or line.startswith("TYPE"):
            continue
        parts = line.split()
        if len(parts) >= 6 and parts[0] in {"Local", "Build"}:
            type_name = f"{parts[0]} {parts[1]}"
            total, active, size = parts[2], parts[3], parts[4]
            reclaimable = " ".join(parts[5:])
        elif len(parts) >= 5:
            type_name = parts[0]
            total, active, size = parts[1], parts[2], parts[3]
            reclaimable = " ".join(parts[4:])
        else:
            continue
        rows.append(
            {
                "type": type_name,
                "total": total,
                "active": active,
                "size": size,
                "reclaimable": reclaimable,
            }
        )
    return rows


def parse_table_lines(text: str, fields: list[str]) -> list[dict[str, str]]:
    rows = []
    for line in text.splitlines():
        if not line.strip():
            continue
        values = line.split("\t")
        row = {field: values[index] if index < len(values) else "" for index, field in enumerate(fields)}
        rows.append(row)
    return rows


def parse_df_k(text: str) -> tuple[int, int, int]:
    lines = [line for line in text.splitlines() if line.strip()]
    if len(lines) < 2:
        return 0, 0, 0
    parts = lines[1].split()
    if len(parts) < 4:
        return 0, 0, 0
    return int(parts[1]) * 1024, int(parts[2]) * 1024, int(parts[3]) * 1024


def first_number(data: dict[str, Any], keys: list[str]) -> int:
    for key in keys:
        value = data.get(key)
        if isinstance(value, (int, float)):
            return int(value)
    return 0


def decorate_plan(plan: list[dict[str, Any]], *, docker: dict[str, Any]) -> list[dict[str, Any]]:
    system_df = docker.get("system_df", [])
    build_cache = next((row for row in system_df if row.get("type") == "Build Cache"), None)
    return [
        {
            **step,
            "estimate": build_cache.get("reclaimable", "") if step["id"] == "docker_builder_cache" and build_cache else "",
        }
        for step in plan
    ]


def deep_action_catalog(
    backups: dict[str, Any] | None = None,
    *,
    docker: dict[str, Any] | None = None,
    journal: dict[str, Any] | None = None,
    store: dict[str, Any] | None = None,
    storage: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    docker_rows = {row.get("type"): row for row in (docker or {}).get("system_df", [])}
    used_percent = int((storage or {}).get("used_percent") or 0)
    backup_items = recommended_backup_items((backups or {}).get("backups", []))
    repository_items = recommended_repository_items(store or {})
    system_prune_estimate = reclaimable_for(docker_rows.get("Containers"))
    image_estimate = reclaimable_for(docker_rows.get("Images"))
    journal_size = int((journal or {}).get("size_bytes") or 0)

    system_prune_decision = cleanup_decision(
        system_prune_estimate > 0,
        "deep.reason.stoppedContainersRecommended",
        "deep.reason.stoppedContainersNotRecommended",
    )
    image_decision = cleanup_decision(
        image_estimate >= 1024**3 or (used_percent >= 80 and image_estimate > 0),
        "deep.reason.unusedImagesRecommended",
        "deep.reason.unusedImagesNotRecommended",
    )
    journal_decision = cleanup_decision(
        journal_size >= 512 * 1024**2,
        "deep.reason.journalRecommended",
        "deep.reason.journalNotRecommended",
    )
    backup_decision = cleanup_decision(
        any(item["recommendation"] == "recommended" for item in backup_items),
        "deep.reason.backupsRecommended",
        "deep.reason.backupsNotRecommended",
    )
    repository_decision = cleanup_decision(
        any(item["recommendation"] == "recommended" for item in repository_items),
        "deep.reason.repositoriesRecommended",
        "deep.reason.repositoriesNotRecommended",
    )

    return [
        {
            "id": "docker_system_prune",
            "label": "Stopped containers and dangling Docker data",
            "risk": "medium",
            "description": "Runs Docker system prune without volumes. Review before running on HAOS.",
            "estimate": human_bytes(system_prune_estimate) if system_prune_estimate else "",
            **system_prune_decision,
        },
        {
            "id": "unused_images",
            "label": "Unused Docker images",
            "risk": "medium",
            "description": "Deletes images not used by any container. Re-download may be needed later.",
            "estimate": human_bytes(image_estimate) if image_estimate else "",
            **image_decision,
        },
        {
            "id": "journal_vacuum",
            "label": "System journal vacuum",
            "risk": "medium",
            "description": "Caps system journal size. Older logs are removed first.",
            "journal_vacuum_size": journal_vacuum_size(),
            "estimate": human_bytes(journal_size) if journal_size else "",
            **journal_decision,
        },
        {
            "id": "delete_backups",
            "label": "Selected backups",
            "risk": "high",
            "description": "Deletes only backups selected below.",
            "items": backup_items,
            **backup_decision,
        },
        {
            "id": "delete_repositories",
            "label": "Selected stale repositories",
            "risk": "medium",
            "description": "Deletes selected add-on repositories by slug. Do not remove repositories that provide installed add-ons.",
            "items": repository_items,
            **repository_decision,
        },
    ]


def recommended_backup_items(backups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    enriched = [{"backup": backup, "created": backup_timestamp(backup)} for backup in backups]
    dated = [item["created"] for item in enriched if item["created"]]
    newest = max(dated) if dated else None
    now = time.time()
    items = []

    for entry in enriched:
        backup = entry["backup"]
        created = entry["created"]
        newer_count = sum(1 for other in dated if created and other > created)
        age_days = int((now - created) / 86400) if created else None
        size_bytes = int(backup.get("size_bytes") or 0)
        protected = bool(backup.get("protected"))
        recommended = (
            bool(created)
            and not protected
            and created != newest
            and newer_count >= 2
            and (age_days or 0) >= 45
        ) or (
            bool(created)
            and not protected
            and created != newest
            and newer_count >= 1
            and (age_days or 0) >= 30
            and size_bytes >= 5 * 1024**3
        )
        reason_key = "deep.reason.backupItemRecommended" if recommended else backup_not_recommended_reason(protected, created, newer_count)
        items.append(
            {
                "slug": backup.get("slug", ""),
                "name": backup.get("name", backup.get("slug", "")),
                "size": backup.get("size", ""),
                "size_bytes": size_bytes,
                "created": backup.get("date") or backup.get("created") or backup.get("created_at") or "",
                "age_days": age_days,
                **cleanup_decision(recommended, reason_key, reason_key),
            }
        )

    return items


def backup_timestamp(backup: dict[str, Any]) -> float | None:
    value = backup.get("date") or backup.get("created") or backup.get("created_at")
    if not value:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).replace("Z", "+00:00")
    for fmt, slice_end in (("%Y-%m-%dT%H:%M:%S", 19), ("%Y-%m-%d", 10)):
        try:
            return time.mktime(time.strptime(text[:slice_end], fmt))
        except ValueError:
            continue
    return None


def backup_not_recommended_reason(protected: bool, created: float | None, newer_count: int) -> str:
    if protected:
        return "deep.reason.backupItemProtected"
    if not created:
        return "deep.reason.backupItemUnknown"
    if newer_count == 0:
        return "deep.reason.backupItemLatest"
    return "deep.reason.backupItemRecent"


def recommended_repository_items(store: dict[str, Any]) -> list[dict[str, Any]]:
    repositories = store.get("repositories") or []
    addons = store.get("addons") or []
    installed_addons = store.get("installed_addons") or []
    installed_sources = repository_sources_with_installed_addons(addons, installed_addons)
    items = []

    for repository in repositories:
        slug = str(repository.get("slug") or "")
        source = str(repository.get("source") or repository.get("url") or "")
        source_keys = {str(key) for key in [slug, source, repository.get("url"), repository.get("name")] if key}
        official_or_local = slug in {"core", "local"} or source in {"core", "local"}
        has_installed = bool(source_keys & installed_sources)
        recommended = bool(store.get("available") and slug and not official_or_local and not has_installed)
        reason_key = "deep.reason.repositoryItemRecommended" if recommended else repository_not_recommended_reason(store, official_or_local, has_installed)
        items.append(
            {
                "slug": slug,
                "name": repository.get("name") or slug,
                "source": source,
                "maintainer": repository.get("maintainer", ""),
                **cleanup_decision(recommended, reason_key, reason_key),
            }
        )

    return items


def repository_sources_with_installed_addons(addons: list[dict[str, Any]], installed_addons: list[dict[str, Any]]) -> set[str]:
    sources: set[str] = set()
    installed_slugs = {str(addon.get("slug")) for addon in installed_addons if addon_is_installed(addon)}
    for addon in addons:
        if addon_is_installed(addon) or str(addon.get("slug")) in installed_slugs:
            for key in ("repository", "repository_url", "repository_slug"):
                value = addon.get(key)
                if value:
                    sources.add(str(value))
    for addon in installed_addons:
        for key in ("repository", "repository_url", "repository_slug"):
            value = addon.get(key)
            if value:
                sources.add(str(value))
    return sources


def addon_is_installed(addon: dict[str, Any]) -> bool:
    installed = addon.get("installed")
    if isinstance(installed, bool):
        return installed
    if installed in (None, "", "false", "False", "0", 0, False):
        return False
    return True


def repository_not_recommended_reason(store: dict[str, Any], official_or_local: bool, has_installed: bool) -> str:
    if not store.get("available"):
        return "deep.reason.repositoryItemUnknown"
    if official_or_local:
        return "deep.reason.repositoryItemOfficial"
    if has_installed:
        return "deep.reason.repositoryItemInstalled"
    return "deep.reason.repositoryItemKeep"


def cleanup_decision(recommended: bool, recommended_reason: str, not_recommended_reason: str) -> dict[str, str | bool]:
    return {
        "recommendation": "recommended" if recommended else "not_recommended",
        "recommended": recommended,
        "reason_key": recommended_reason if recommended else not_recommended_reason,
    }


def reclaimable_for(row: dict[str, Any] | None) -> int:
    return parse_size_to_bytes((row or {}).get("reclaimable"))


def deep_clean_enabled() -> bool:
    return os.environ.get("ENABLE_DEEP_CLEAN", "true").lower() in {"1", "true", "yes", "on"}


def journal_vacuum_size() -> str:
    return os.environ.get("JOURNAL_VACUUM_SIZE", "300M")


def load_history() -> list[dict[str, Any]]:
    if not HISTORY_FILE.exists():
        return []
    try:
        data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def append_history(entry: dict[str, Any]) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    history = load_history()
    history.insert(0, {"timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **entry})
    HISTORY_FILE.write_text(json.dumps(history[:50], ensure_ascii=False, indent=2), encoding="utf-8")


def scan_summary(result: dict[str, Any]) -> str:
    storage = result.get("storage", {})
    return f"Scanned storage: {storage.get('human', {}).get('used', 'unknown')} used, {storage.get('human', {}).get('free', 'unknown')} free."


def cleanup_summary(report: dict[str, Any]) -> str:
    status = "completed" if report.get("ok") else "stopped with errors"
    return f"{report.get('mode', 'cleanup')} {status} with {len(report.get('results', []))} action(s)."


def compact_result(result: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in result.items()
        if key
        in {
            "ok",
            "mode",
            "storage",
            "docker",
            "backups",
            "resolution",
            "homeassistant",
            "journal",
            "intelligence",
            "duration_ms",
            "timings",
            "safe_actions",
            "deep_actions",
            "before",
            "after",
            "results",
        }
    }


def trim_output(text: str | bytes) -> str:
    if isinstance(text, bytes):
        text = text.decode("utf-8", "ignore")
    if len(text.encode("utf-8")) <= MAX_OUTPUT_BYTES:
        return text
    return text.encode("utf-8")[:MAX_OUTPUT_BYTES].decode("utf-8", "ignore") + "\n... output trimmed ..."


if __name__ == "__main__":
    main()
