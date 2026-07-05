import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "rootfs" / "opt"
sys.path.insert(0, str(ROOT))

from tabs_cleaner.core import (  # noqa: E402
    analyze_scan,
    build_deep_plan,
    build_safe_plan,
    human_bytes,
    parse_size_to_bytes,
    risk_level,
    summarize_storage,
)


class CoreTests(unittest.TestCase):
    def test_safe_plan_never_includes_high_risk_docker_flags(self):
        plan = build_safe_plan()
        commands = "\n".join(" ".join(step["command"]) for step in plan)

        self.assertIn("docker builder prune -af", commands)
        self.assertNotIn("docker system prune -f", commands)
        self.assertNotIn("--volumes", commands)
        self.assertNotIn("image prune -a", commands)
        self.assertNotIn("/mnt/data/docker/overlay2", commands)

    def test_deep_plan_requires_confirmation(self):
        with self.assertRaises(ValueError):
            build_deep_plan(["unused_images"], confirmed=False)

    def test_deep_plan_rejects_empty_executable_plan(self):
        with self.assertRaises(ValueError):
            build_deep_plan([], confirmed=True)

        with self.assertRaises(ValueError):
            build_deep_plan(["delete_backups"], confirmed=True, backup_slugs=[])

    def test_deep_plan_only_allows_known_actions(self):
        with self.assertRaises(ValueError):
            build_deep_plan(["unused_images", "rm -rf /"], confirmed=True)

    def test_deep_plan_builds_selected_safe_commands(self):
        plan = build_deep_plan(
            ["docker_system_prune", "unused_images", "journal_vacuum"],
            confirmed=True,
            journal_vacuum_size="300M",
        )
        commands = [" ".join(step["command"]) for step in plan]

        self.assertEqual(commands[0], "docker system prune -f")
        self.assertEqual(commands[1], "docker image prune -af")
        self.assertEqual(commands[2], "journalctl --vacuum-size=300M")

    def test_deep_plan_deletes_only_selected_repository_slugs(self):
        plan = build_deep_plan(
            ["delete_repositories"],
            confirmed=True,
            repository_slugs=["community-addons"],
        )

        self.assertEqual(len(plan), 1)
        self.assertEqual(plan[0]["command"], ["ha", "store", "delete", "community-addons"])

    def test_deep_plan_rejects_unsafe_repository_slug(self):
        with self.assertRaises(ValueError):
            build_deep_plan(
                ["delete_repositories"],
                confirmed=True,
                repository_slugs=["../../supervisor"],
            )

    def test_storage_summary_computes_percent_and_risk(self):
        summary = summarize_storage(
            {
                "total": 1000,
                "used": 910,
                "free": 90,
                "categories": {"docker": 600, "supervisor": 300, "logs": 10},
            }
        )

        self.assertEqual(summary["used_percent"], 91)
        self.assertEqual(summary["risk"], "critical")
        self.assertEqual(summary["largest_category"]["name"], "docker")
        self.assertEqual(summary["largest_category"]["bytes"], 600)

    def test_human_bytes_formats_values(self):
        self.assertEqual(human_bytes(0), "0 B")
        self.assertEqual(human_bytes(1024), "1.0 KB")
        self.assertEqual(human_bytes(1024 * 1024 * 3), "3.0 MB")

    def test_risk_level_thresholds(self):
        self.assertEqual(risk_level(49), "healthy")
        self.assertEqual(risk_level(70), "warning")
        self.assertEqual(risk_level(86), "danger")
        self.assertEqual(risk_level(95), "critical")

    def test_parse_size_to_bytes_handles_docker_units(self):
        self.assertEqual(parse_size_to_bytes("6.567GB"), 7051262558)
        self.assertEqual(parse_size_to_bytes("3.852GB (45%)"), 4136053506)
        self.assertEqual(parse_size_to_bytes("108.2MB"), 113455923)
        self.assertEqual(parse_size_to_bytes("0B"), 0)

    def test_analyze_scan_separates_safe_and_deep_findings(self):
        analysis = analyze_scan(
            {
                "storage": {"used_percent": 92, "human": {"free": "2.0 GB"}},
                "docker": {
                    "system_df": [
                        {"type": "Build Cache", "reclaimable": "6.0GB"},
                        {"type": "Images", "reclaimable": "4.0GB (40%)"},
                        {"type": "Local Volumes", "reclaimable": "2.0GB (20%)"},
                    ]
                },
                "backups": {"backups": [{"slug": "a", "name": "Full", "size_bytes": 5 * 1024**3}]},
                "homeassistant": {"database": {"size_bytes": 3 * 1024**3}},
                "journal": {"size_bytes": 800 * 1024**2},
            }
        )

        self.assertGreaterEqual(analysis["safe_reclaimable_bytes"], 6 * 1024**3)
        self.assertGreaterEqual(analysis["deep_reclaimable_bytes"], 9 * 1024**3)
        self.assertEqual(analysis["pressure"], "critical")
        ids = [finding["id"] for finding in analysis["findings"]]
        self.assertIn("safe_docker_build_cache", ids)
        self.assertIn("deep_unused_images", ids)
        self.assertIn("preserve_docker_volumes", ids)


if __name__ == "__main__":
    unittest.main()
