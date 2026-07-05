from __future__ import annotations

import re
from typing import Any


SAFE_CLEAN_ACTIONS: dict[str, dict[str, Any]] = {
    "docker_builder_cache": {
        "label": "Docker build cache",
        "description": "Remove unused Docker builder cache. Does not delete volumes or add-on data.",
        "risk": "low",
        "command": ["docker", "builder", "prune", "-af"],
    },
    "resolution_healthcheck": {
        "label": "Refresh HAOS health checks",
        "description": "Ask the Supervisor Resolution center to refresh health state.",
        "risk": "low",
        "command": ["ha", "resolution", "healthcheck"],
        "optional": True,
    },
}


DEEP_CLEAN_ACTIONS: dict[str, dict[str, Any]] = {
    "docker_system_prune": {
        "label": "Stopped containers and dangling Docker data",
        "description": "Run Docker's default system prune without volumes.",
        "risk": "medium",
        "command": ["docker", "system", "prune", "-f"],
    },
    "unused_images": {
        "label": "Unused Docker images",
        "description": "Remove Docker images that are not used by containers.",
        "risk": "medium",
        "command": ["docker", "image", "prune", "-af"],
    },
    "journal_vacuum": {
        "label": "System journal vacuum",
        "description": "Reduce persistent journal size to the selected limit.",
        "risk": "medium",
        "command_template": ["journalctl", "--vacuum-size={journal_vacuum_size}"],
    },
}


SIZE_RE = re.compile(r"(?P<number>[0-9]+(?:\.[0-9]+)?)\s*(?P<unit>B|K|KB|KIB|M|MB|MIB|G|GB|GIB|T|TB|TIB)", re.IGNORECASE)
UNIT_BYTES = {
    "B": 1,
    "K": 1024,
    "KB": 1024,
    "KIB": 1024,
    "M": 1024**2,
    "MB": 1024**2,
    "MIB": 1024**2,
    "G": 1024**3,
    "GB": 1024**3,
    "GIB": 1024**3,
    "T": 1024**4,
    "TB": 1024**4,
    "TIB": 1024**4,
}


def human_bytes(value: int | float | None) -> str:
    if value is None:
        return "0 B"
    size = float(value)
    units = ["B", "KB", "MB", "GB", "TB"]
    for unit in units:
        if abs(size) < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(size)} B"
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def risk_level(used_percent: int | float) -> str:
    if used_percent >= 90:
        return "critical"
    if used_percent >= 80:
        return "danger"
    if used_percent >= 65:
        return "warning"
    return "healthy"


def parse_size_to_bytes(value: str | int | float | None) -> int:
    if value is None:
        return 0
    if isinstance(value, (int, float)):
        return int(value)
    match = SIZE_RE.search(str(value).strip())
    if not match:
        return 0
    number = float(match.group("number"))
    unit = match.group("unit").upper()
    return int(number * UNIT_BYTES[unit])


def build_safe_plan() -> list[dict[str, Any]]:
    return [
        {
            "id": action_id,
            "label": action["label"],
            "description": action["description"],
            "risk": action["risk"],
            "command": list(action["command"]),
            "optional": bool(action.get("optional", False)),
        }
        for action_id, action in SAFE_CLEAN_ACTIONS.items()
    ]


def build_deep_plan(
    selected_actions: list[str],
    *,
    confirmed: bool,
    journal_vacuum_size: str = "300M",
    backup_slugs: list[str] | None = None,
    repository_slugs: list[str] | None = None,
) -> list[dict[str, Any]]:
    if not confirmed:
        raise ValueError("Deep cleanup requires explicit confirmation.")

    plan: list[dict[str, Any]] = []
    for action_id in selected_actions:
        if action_id == "delete_backups":
            plan.extend(_backup_delete_steps(backup_slugs or []))
            continue
        if action_id == "delete_repositories":
            plan.extend(_repository_delete_steps(repository_slugs or []))
            continue

        action = DEEP_CLEAN_ACTIONS.get(action_id)
        if action is None:
            raise ValueError(f"Unknown deep cleanup action: {action_id}")

        command = list(action.get("command", []))
        if "command_template" in action:
            command = [
                part.format(journal_vacuum_size=_validate_journal_size(journal_vacuum_size))
                for part in action["command_template"]
            ]
        plan.append(
            {
                "id": action_id,
                "label": action["label"],
                "description": action["description"],
                "risk": action["risk"],
                "command": command,
            }
        )

    if not plan:
        raise ValueError("Deep cleanup requires at least one executable selected item.")

    return plan


def summarize_storage(snapshot: dict[str, Any]) -> dict[str, Any]:
    total = int(snapshot.get("total") or 0)
    used = int(snapshot.get("used") or 0)
    free = int(snapshot.get("free") or max(total - used, 0))
    categories = snapshot.get("categories") or {}
    used_percent = int(round((used / total) * 100)) if total > 0 else 0
    largest_name = None
    largest_bytes = 0
    for name, bytes_value in categories.items():
        value = int(bytes_value or 0)
        if value > largest_bytes:
            largest_name = name
            largest_bytes = value

    return {
        "total": total,
        "used": used,
        "free": free,
        "used_percent": used_percent,
        "risk": risk_level(used_percent),
        "human": {
            "total": human_bytes(total),
            "used": human_bytes(used),
            "free": human_bytes(free),
        },
        "categories": categories,
        "largest_category": {"name": largest_name, "bytes": largest_bytes},
    }


def analyze_scan(scan: dict[str, Any]) -> dict[str, Any]:
    storage = scan.get("storage") or {}
    docker = scan.get("docker") or {}
    backups = scan.get("backups") or {}
    homeassistant = scan.get("homeassistant") or {}
    journal = scan.get("journal") or {}
    docker_rows = {row.get("type"): row for row in docker.get("system_df", [])}

    build_cache_bytes = _row_reclaimable_bytes(docker_rows.get("Build Cache"))
    images_bytes = _row_reclaimable_bytes(docker_rows.get("Images"))
    containers_bytes = _row_reclaimable_bytes(docker_rows.get("Containers"))
    volumes_bytes = _row_reclaimable_bytes(docker_rows.get("Local Volumes"))
    backup_bytes = sum(int(item.get("size_bytes") or 0) for item in backups.get("backups", []))
    journal_bytes = int(journal.get("size_bytes") or 0)
    database_bytes = int((homeassistant.get("database") or {}).get("size_bytes") or 0)

    findings: list[dict[str, Any]] = []
    safe_reclaimable = 0
    deep_reclaimable = 0

    if build_cache_bytes > 0:
        safe_reclaimable += build_cache_bytes
        findings.append(
            _finding(
                "safe_docker_build_cache",
                "safe",
                "low",
                build_cache_bytes,
                "docker_builder_cache",
                "Docker build cache can be pruned without touching images, containers, volumes, backups, or add-on data.",
                "official-docker-builder-prune",
            )
        )

    if containers_bytes > 0:
        deep_reclaimable += containers_bytes
        findings.append(
            _finding(
                "deep_stopped_containers",
                "deep",
                "medium",
                containers_bytes,
                "docker_system_prune",
                "Stopped containers are unused at runtime, but system prune is still a review action on HAOS.",
                "official-docker-system-prune",
            )
        )

    if images_bytes > 0:
        deep_reclaimable += images_bytes
        findings.append(
            _finding(
                "deep_unused_images",
                "deep",
                "medium",
                images_bytes,
                "unused_images",
                "Unused images can usually be re-downloaded, but removing them can slow future add-on starts or rebuilds.",
                "official-docker-image-prune",
            )
        )

    if backup_bytes > 0:
        deep_reclaimable += backup_bytes
        findings.append(
            _finding(
                "deep_backups",
                "deep",
                "high",
                backup_bytes,
                "delete_backups",
                "Backups are often large and safe to delete only when the user selects specific restore points.",
                "ha-backup-workflow",
            )
        )

    if journal_bytes >= 256 * 1024**2:
        deep_reclaimable += journal_bytes
        findings.append(
            _finding(
                "deep_journal",
                "deep",
                "medium",
                journal_bytes,
                "journal_vacuum",
                "Journal vacuum removes older logs first and should be explicit because logs are useful during incident review.",
                "systemd-journal-vacuum",
            )
        )

    if volumes_bytes > 0:
        findings.append(
            _finding(
                "preserve_docker_volumes",
                "preserve",
                "high",
                volumes_bytes,
                None,
                "Docker volumes can contain persistent add-on data. TabS Cleaner never removes them automatically.",
                "official-docker-volume-prune",
            )
        )

    if database_bytes >= 1024**3:
        findings.append(
            _finding(
                "review_recorder_database",
                "review",
                "medium",
                database_bytes,
                None,
                "Large recorder databases should be handled through Home Assistant recorder purge settings, not raw file deletion.",
                "ha-recorder-docs",
            )
        )

    used_percent = int(storage.get("used_percent") or 0)
    pressure = risk_level(used_percent)
    score = max(0, min(100, 100 - used_percent + min(15, safe_reclaimable // (1024**3))))

    return {
        "score": int(score),
        "pressure": pressure,
        "safe_reclaimable_bytes": safe_reclaimable,
        "deep_reclaimable_bytes": deep_reclaimable,
        "safe_reclaimable": human_bytes(safe_reclaimable),
        "deep_reclaimable": human_bytes(deep_reclaimable),
        "findings": findings,
        "guardrails": [
            "never_delete_docker_volumes",
            "never_delete_overlay2_manually",
            "never_delete_backups_without_selection",
            "never_delete_homeassistant_database_file",
            "never_run_docker_image_prune_in_safe_mode",
        ],
    }


def _row_reclaimable_bytes(row: dict[str, Any] | None) -> int:
    if not row:
        return 0
    return parse_size_to_bytes(row.get("reclaimable"))


def _finding(
    finding_id: str,
    tier: str,
    risk: str,
    estimate_bytes: int,
    action_id: str | None,
    detail: str,
    source: str,
) -> dict[str, Any]:
    return {
        "id": finding_id,
        "tier": tier,
        "risk": risk,
        "estimate_bytes": estimate_bytes,
        "estimate": human_bytes(estimate_bytes),
        "action_id": action_id,
        "detail": detail,
        "source": source,
    }


def _validate_journal_size(value: str) -> str:
    if not re.fullmatch(r"[1-9][0-9]*(K|M|G)", value):
        raise ValueError("journal_vacuum_size must look like 300M, 1G, or 512K.")
    return value


def _validate_slug(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", value):
        raise ValueError(f"Invalid slug: {value}")
    return value


def _backup_delete_steps(slugs: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "id": "delete_backups",
            "label": f"Delete backup {slug}",
            "description": "Delete a selected Home Assistant backup.",
            "risk": "high",
            "command": ["ha", "backups", "delete", _validate_slug(slug)],
        }
        for slug in slugs
    ]


def _repository_delete_steps(slugs: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "id": "delete_repositories",
            "label": f"Delete repository {slug}",
            "description": "Delete a selected add-on repository.",
            "risk": "medium",
            "command": ["ha", "store", "delete", _validate_slug(slug)],
        }
        for slug in slugs
    ]
