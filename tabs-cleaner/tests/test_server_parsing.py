import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1] / "rootfs" / "opt"
sys.path.insert(0, str(ROOT))

from tabs_cleaner import server  # noqa: E402


class ServerParsingTests(unittest.TestCase):
    def test_parse_docker_system_df_preserves_multiword_types(self):
        rows = server.parse_docker_system_df(
            """TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          19        17        5.99GB    4.71GB (78%)
Containers      17        17        1.713GB   0B (0%)
Local Volumes   2         2         108.2MB   0B (0%)
Build Cache     0         0         0B        0B
"""
        )

        self.assertEqual(rows[0]["type"], "Images")
        self.assertEqual(rows[2]["type"], "Local Volumes")
        self.assertEqual(rows[2]["total"], "2")
        self.assertEqual(rows[3]["type"], "Build Cache")
        self.assertEqual(rows[3]["size"], "0B")

    def test_deep_action_catalog_follows_enabled_option(self):
        with mock.patch.dict("os.environ", {"ENABLE_DEEP_CLEAN": "false"}, clear=False):
            self.assertFalse(server.deep_clean_enabled())

        with mock.patch.dict("os.environ", {"ENABLE_DEEP_CLEAN": "true"}, clear=False):
            self.assertTrue(server.deep_clean_enabled())

    def test_journal_vacuum_size_comes_from_environment(self):
        with mock.patch.dict("os.environ", {"JOURNAL_VACUUM_SIZE": "1G"}, clear=False):
            catalog = server.deep_action_catalog()

        journal_action = next(action for action in catalog if action["id"] == "journal_vacuum")
        self.assertEqual(journal_action["journal_vacuum_size"], "1G")

    def test_deep_action_catalog_marks_recommended_and_not_recommended_items(self):
        catalog = server.deep_action_catalog(
            docker={
                "system_df": [
                    {"type": "Containers", "reclaimable": "0B"},
                    {"type": "Images", "reclaimable": "2.0GB (50%)"},
                ]
            },
            journal={"size_bytes": 100 * 1024**2},
            storage={"used_percent": 70},
        )

        containers = next(action for action in catalog if action["id"] == "docker_system_prune")
        images = next(action for action in catalog if action["id"] == "unused_images")
        journal = next(action for action in catalog if action["id"] == "journal_vacuum")

        self.assertEqual(containers["recommendation"], "not_recommended")
        self.assertEqual(images["recommendation"], "recommended")
        self.assertEqual(journal["recommendation"], "not_recommended")

    def test_repository_recommendations_preserve_installed_repositories(self):
        catalog = server.deep_action_catalog(
            store={
                "available": True,
                "repositories": [
                    {"slug": "core", "name": "Core", "source": "core"},
                    {"slug": "music-repo", "name": "Music", "source": "https://example.test/music"},
                    {"slug": "stale-repo", "name": "Stale", "source": "https://example.test/stale"},
                ],
                "addons": [
                    {
                        "slug": "music_player",
                        "installed": "1.2.3",
                        "repository": "https://example.test/music",
                    }
                ],
                "installed_addons": [{"slug": "music_player", "installed": True}],
            }
        )

        repositories = next(action for action in catalog if action["id"] == "delete_repositories")
        items = {item["slug"]: item for item in repositories["items"]}

        self.assertEqual(items["core"]["recommendation"], "not_recommended")
        self.assertEqual(items["music-repo"]["recommendation"], "not_recommended")
        self.assertEqual(items["stale-repo"]["recommendation"], "recommended")
        self.assertEqual(repositories["recommendation"], "recommended")

    def test_backup_recommendations_need_newer_replacements(self):
        catalog = server.deep_action_catalog(
            backups={
                "backups": [
                    {
                        "slug": "old",
                        "name": "Old",
                        "date": "2025-01-01T00:00:00Z",
                        "size_bytes": 1024,
                    },
                    {
                        "slug": "middle",
                        "name": "Middle",
                        "date": "2025-03-01T00:00:00Z",
                        "size_bytes": 1024,
                    },
                    {
                        "slug": "latest",
                        "name": "Latest",
                        "date": "2025-05-01T00:00:00Z",
                        "size_bytes": 1024,
                    },
                ]
            }
        )

        backups = next(action for action in catalog if action["id"] == "delete_backups")
        items = {item["slug"]: item for item in backups["items"]}

        self.assertEqual(items["old"]["recommendation"], "recommended")
        self.assertEqual(items["latest"]["recommendation"], "not_recommended")
        self.assertEqual(backups["recommendation"], "recommended")

    def test_parse_journal_disk_usage(self):
        self.assertEqual(
            server.parse_journal_disk_usage("Archived and active journals take up 812.4M in the file system."),
            851863142,
        )

    def test_parse_du_k_lines_returns_largest_entries(self):
        entries = server.parse_du_k_lines(
            """2048\t/homeassistant/home-assistant_v2.db
512\t/homeassistant/custom_components
4096\t/homeassistant/www
""",
            limit=2,
        )

        self.assertEqual(entries[0]["path"], "/homeassistant/www")
        self.assertEqual(entries[0]["size_bytes"], 4194304)
        self.assertEqual(entries[1]["path"], "/homeassistant/home-assistant_v2.db")

    def test_run_parallel_tasks_returns_results_and_timings(self):
        result = server.run_parallel_tasks(
            {
                "alpha": lambda: "ok",
                "beta": lambda: {"value": 2},
            }
        )

        self.assertEqual(result["results"]["alpha"], "ok")
        self.assertEqual(result["results"]["beta"], {"value": 2})
        self.assertIn("alpha", result["timings"])
        self.assertIsInstance(result["timings"]["alpha"], int)


if __name__ == "__main__":
    unittest.main()
