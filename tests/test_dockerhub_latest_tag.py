import importlib.util
from pathlib import Path
import sys
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / ".github" / "scripts" / "dockerhub_latest_tag.py"
SPEC = importlib.util.spec_from_file_location("dockerhub_latest_tag", MODULE_PATH)
dockerhub_latest_tag = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = dockerhub_latest_tag
SPEC.loader.exec_module(dockerhub_latest_tag)


class DockerHubLatestTagTests(unittest.TestCase):
    def test_finds_stable_semver_after_a_page_of_unstable_tags(self):
        first_url = "https://registry.example/tags?page=1"
        second_url = "https://registry.example/tags?page=2"
        pages = {
            first_url: {
                "results": [{"name": f"unstable-202607{day:02d}"} for day in range(1, 51)],
                "next": second_url,
            },
            second_url: {
                "results": [{"name": "v0.9.43"}, {"name": "v0.9.42"}],
                "next": None,
            },
        }

        tag = dockerhub_latest_tag.latest_tag(
            "looplj/axonhub",
            "semver",
            initial_url=first_url,
            fetch_json=pages.__getitem__,
        )

        self.assertEqual(tag, "v0.9.43")

    def test_selects_highest_semver_across_all_pages(self):
        first_url = "https://registry.example/tags?page=1"
        second_url = "https://registry.example/tags?page=2"
        pages = {
            first_url: {
                "results": [{"name": "v0.9.42"}],
                "next": second_url,
            },
            second_url: {
                "results": [{"name": "v0.9.43"}],
                "next": None,
            },
        }

        tag = dockerhub_latest_tag.latest_tag(
            "looplj/axonhub",
            "semver",
            initial_url=first_url,
            fetch_json=pages.__getitem__,
        )

        self.assertEqual(tag, "v0.9.43")

    def test_sha_format_never_falls_back_to_unstable_tag(self):
        url = "https://registry.example/tags?page=1"
        pages = {
            url: {
                "results": [
                    {"name": "unstable-20260721"},
                    {"name": "sha-41767a6"},
                ],
                "next": None,
            },
        }

        tag = dockerhub_latest_tag.latest_tag(
            "1467078763/metapi",
            "sha",
            initial_url=url,
            fetch_json=pages.__getitem__,
        )

        self.assertEqual(tag, "sha-41767a6")


if __name__ == "__main__":
    unittest.main()
