import importlib.util
from pathlib import Path
import sys
import unittest
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / ".github" / "scripts" / "sync_upstream_metadata.py"
SPEC = importlib.util.spec_from_file_location("sync_upstream_metadata", MODULE_PATH)
sync_upstream_metadata = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = sync_upstream_metadata
SPEC.loader.exec_module(sync_upstream_metadata)


class SyncUpstreamMetadataTests(unittest.TestCase):
    def test_wrapper_version_uses_upstream_base_version(self):
        self.assertEqual(
            sync_upstream_metadata.next_wrapper_version("7.1.58-1", "7.1.58", False),
            "7.1.58-1",
        )
        self.assertEqual(
            sync_upstream_metadata.next_wrapper_version("7.1.58-1", "7.1.58", True),
            "7.1.58-2",
        )
        self.assertEqual(
            sync_upstream_metadata.next_wrapper_version("7.1.58-2", "7.1.59", False),
            "7.1.59-1",
        )

    def test_changelog_entry_links_upstream_release_without_wrapper_suffix(self):
        update = sync_upstream_metadata.AddonUpdate(
            "cli-proxy-api",
            "eceasy/cli-proxy-api",
            "CLI_PROXY_API_VERSION",
            "CLI_PROXY_API_TAG",
            "router-for-me/CLIProxyAPI",
        )

        def fake_find_release(repo, candidates):
            self.assertEqual(repo, "router-for-me/CLIProxyAPI")
            self.assertIn("v7.1.58", candidates)
            self.assertIn("7.1.58", candidates)
            self.assertNotIn("7.1.58-1", candidates)
            return {
                "tag_name": "v7.1.58",
                "name": "v7.1.58",
                "html_url": "https://github.com/router-for-me/CLIProxyAPI/releases/tag/v7.1.58",
                "body": "- Added OAuth support\n- Fixed proxy routing",
            }

        with mock.patch.object(sync_upstream_metadata, "find_release", side_effect=fake_find_release):
            entry = sync_upstream_metadata.build_changelog_entry(update, "7.1.58-1", "7.1.58", "v7.1.58")

        text = "\n".join(entry)
        self.assertIn("## 7.1.58-1", text)
        self.assertIn("Upstream release: [v7.1.58]", text)
        self.assertIn("Added OAuth support", text)
        self.assertIn("Fixed proxy routing", text)


if __name__ == "__main__":
    unittest.main()
