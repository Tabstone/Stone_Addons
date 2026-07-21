from __future__ import annotations

import argparse
import json
import re
import urllib.request
from collections.abc import Callable
from typing import Any


SEMVER_RE = re.compile(r"^v?(\d+)\.(\d+)(?:\.(\d+))?$")
SHA_RE = re.compile(r"^sha-[0-9a-f]{7,40}$")


def semver_key(tag: str) -> tuple[int, int, int, int] | None:
    match = SEMVER_RE.fullmatch(tag)
    if not match:
        return None
    major, minor, patch = match.groups()
    return int(major), int(minor), int(patch or 0), int(patch is not None)


def fetch_json(url: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Stone-Addons-Upstream-Sync"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def latest_tag(
    repository: str,
    tag_format: str,
    *,
    initial_url: str | None = None,
    fetch_json: Callable[[str], dict[str, Any]] = fetch_json,
) -> str | None:
    url = initial_url or (
        f"https://hub.docker.com/v2/repositories/{repository}/tags/"
        "?page_size=100&ordering=last_updated"
    )
    seen_urls: set[str] = set()
    semver_tags: list[tuple[tuple[int, int, int, int], str]] = []

    while url and url not in seen_urls:
        seen_urls.add(url)
        data = fetch_json(url)
        tags = [
            result.get("name")
            for result in data.get("results", [])
            if isinstance(result, dict) and isinstance(result.get("name"), str)
        ]

        if tag_format == "sha":
            sha_tag = next((tag for tag in tags if SHA_RE.fullmatch(tag)), None)
            if sha_tag:
                return sha_tag
        elif tag_format == "semver":
            semver_tags.extend(
                (key, tag)
                for tag in tags
                if (key := semver_key(tag)) is not None
            )
        else:
            raise ValueError(f"unsupported tag format: {tag_format}")

        next_url = data.get("next")
        url = next_url if isinstance(next_url, str) else None

    if tag_format == "semver" and semver_tags:
        return max(semver_tags, key=lambda item: item[0])[1]
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository")
    parser.add_argument("tag_format", choices=("semver", "sha"))
    args = parser.parse_args()

    tag = latest_tag(args.repository, args.tag_format)
    if tag:
        print(tag)


if __name__ == "__main__":
    main()
