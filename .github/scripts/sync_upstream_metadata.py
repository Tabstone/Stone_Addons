from __future__ import annotations

import json
import os
import re
import textwrap
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AddonUpdate:
    slug: str
    image: str
    version_env: str
    tag_env: str
    upstream_repo: str | None
    image_page: str | None = None


UPDATES = [
    AddonUpdate("trendradar", "wantcat/trendradar", "TRENDRADAR_VERSION", "TRENDRADAR_TAG", "sansan0/TrendRadar"),
    AddonUpdate("trendradar-mcp", "wantcat/trendradar-mcp", "TRENDRADAR_MCP_VERSION", "TRENDRADAR_MCP_TAG", "sansan0/TrendRadar"),
    AddonUpdate("cpa-manager-plus-full", "seakee/cpa-manager-plus", "CPA_MANAGER_PLUS_VERSION", "CPA_MANAGER_PLUS_TAG", "seakee/CPA-Manager-Plus"),
    AddonUpdate("cpa-manager-plus-panel", "seakee/cpa-manager-plus", "CPA_MANAGER_PLUS_VERSION", "CPA_MANAGER_PLUS_TAG", "seakee/CPA-Manager-Plus"),
    AddonUpdate("axonhub", "looplj/axonhub", "AXONHUB_VERSION", "AXONHUB_TAG", "looplj/axonhub"),
    AddonUpdate("drpy-node", "ghcr.io/hjdhnx/drpy-node", "DRPY_NODE_VERSION", "DRPY_NODE_TAG", "hjdhnx/drpy-node", "https://github.com/users/hjdhnx/packages/container/package/drpy-node"),
    AddonUpdate("atvloadly", "ghcr.io/bitxeno/atvloadly", "ATVLOADLY_VERSION", "ATVLOADLY_TAG", "bitxeno/atvloadly", "https://github.com/bitxeno/atvloadly/pkgs/container/atvloadly"),
    AddonUpdate("microsoft-rewards-script", "ghcr.io/thenetsky/microsoft-rewards-script", "MICROSOFT_REWARDS_SCRIPT_VERSION", "MICROSOFT_REWARDS_SCRIPT_TAG", "TheNetsky/Microsoft-Rewards-Script", "https://github.com/TheNetsky/Microsoft-Rewards-Script/pkgs/container/microsoft-rewards-script"),
    AddonUpdate("claude-code-hub", "ghcr.io/ding113/claude-code-hub", "CLAUDE_CODE_HUB_VERSION", "CLAUDE_CODE_HUB_TAG", "ding113/claude-code-hub", "https://github.com/ding113/claude-code-hub/pkgs/container/claude-code-hub"),
    AddonUpdate("cli-proxy-api", "eceasy/cli-proxy-api", "CLI_PROXY_API_VERSION", "CLI_PROXY_API_TAG", "router-for-me/CLIProxyAPI"),
    AddonUpdate("mihomo", "metacubex/mihomo", "MIHOMO_VERSION", "MIHOMO_TAG", "MetaCubeX/mihomo"),
    AddonUpdate("metacubexd", "ghcr.io/metacubex/metacubexd", "METACUBEXD_VERSION", "METACUBEXD_TAG", "MetaCubeX/metacubexd", "https://github.com/MetaCubeX/metacubexd/pkgs/container/metacubexd"),
    AddonUpdate("sub2api", "weishaw/sub2api", "SUB2API_VERSION", "SUB2API_TAG", "Wei-Shaw/sub2api"),
    AddonUpdate("metapi", "1467078763/metapi", "METAPI_VERSION", "METAPI_TAG", "cita-777/metapi"),
]


def github_api_json(path: str) -> dict | list | None:
    token = os.environ.get("GH_API_TOKEN") or os.environ.get("GITHUB_TOKEN")
    request = urllib.request.Request(f"https://api.github.com{path}")
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("User-Agent", "Stone-Addons-Upstream-Sync")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None


def image_url(update: AddonUpdate) -> str:
    image = update.image
    if update.image_page:
        return update.image_page
    if image.startswith("ghcr.io/"):
        parts = image.split("/")
        if len(parts) >= 3:
            owner = parts[1]
            package = parts[-1]
            return f"https://github.com/users/{owner}/packages/container/package/{package}"
        return f"https://{image}"
    return f"https://hub.docker.com/r/{image}"


def version_candidates(image_tag: str, upstream: str) -> list[str]:
    values = [image_tag, upstream]
    for value in (image_tag, upstream):
        if value.startswith("v"):
            values.append(value[1:])
        elif re.match(r"^\d+\.\d+\.\d+", value):
            values.append(f"v{value}")
    unique = []
    for value in values:
        if value and value not in unique:
            unique.append(value)
    return unique


def find_release(repo: str, candidates: list[str]) -> dict | None:
    for tag in candidates:
        encoded = urllib.parse.quote(tag, safe="")
        release = github_api_json(f"/repos/{repo}/releases/tags/{encoded}")
        if isinstance(release, dict) and release.get("html_url"):
            return release
    latest = github_api_json(f"/repos/{repo}/releases/latest")
    if isinstance(latest, dict) and latest.get("html_url"):
        latest_tag = str(latest.get("tag_name", ""))
        if latest_tag in candidates:
            return latest
    return None


def find_tag_url(repo: str, candidates: list[str]) -> tuple[str, str] | None:
    tags = github_api_json(f"/repos/{repo}/tags?per_page=100")
    if not isinstance(tags, list):
        return None
    for tag in tags:
        name = str(tag.get("name", ""))
        if name in candidates:
            return name, f"https://github.com/{repo}/tree/{urllib.parse.quote(name, safe='')}"
    return None


def summarize_release_body(body: str, max_lines: int = 6) -> list[str]:
    lines: list[str] = []
    in_comment = False
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("<!--"):
            in_comment = not line.endswith("-->")
            continue
        if in_comment:
            if line.endswith("-->"):
                in_comment = False
            continue
        if line.startswith("#"):
            continue
        line = re.sub(r"^[-*]\s+", "", line)
        line = re.sub(r"^\d+[.)]\s+", "", line)
        line = re.sub(r"\s+", " ", line).strip()
        if not line or line in {"---", "***"}:
            continue
        lines.append(textwrap.shorten(line, width=180, placeholder="..."))
        if len(lines) >= max_lines:
            break
    return lines


def build_changelog_entry(update: AddonUpdate, wrapper_version: str, upstream: str, image_tag: str) -> list[str]:
    repo_url = f"https://github.com/{update.upstream_repo}" if update.upstream_repo else None
    lines = [
        f"## {wrapper_version}",
        "",
        f"- Sync upstream image [{update.image}:{image_tag}]({image_url(update)}).",
    ]
    if repo_url:
        lines.append(f"- Upstream project: [{update.upstream_repo}]({repo_url}).")
        candidates = version_candidates(image_tag, upstream)
        release = find_release(update.upstream_repo, candidates)
        if release:
            tag_name = str(release.get("tag_name") or image_tag)
            release_name = str(release.get("name") or tag_name)
            lines.append(f"- Upstream release: [{release_name}]({release['html_url']}).")
            summary = summarize_release_body(str(release.get("body") or ""))
            if summary:
                lines.append("- Upstream changelog summary:")
                lines.extend(f"  - {item}" for item in summary)
        else:
            tag = find_tag_url(update.upstream_repo, candidates)
            if tag:
                tag_name, tag_url = tag
                lines.append(f"- Upstream tag: [{tag_name}]({tag_url}).")
            else:
                lines.append("- Upstream release notes were not published or could not be resolved for this image tag.")
    return lines + [""]


def current_addon_version(config_text: str) -> str:
    match = re.search(r'version: "([^"]+)"', config_text)
    return match.group(1) if match else ""


def next_wrapper_version(current_version: str, upstream: str, bump_wrapper: bool) -> str:
    base_version = upstream.split("-", 1)[0]
    current_base, current_suffix = (current_version.split("-", 1) + [None])[:2] if current_version else ("", None)
    current_suffix_num = int(current_suffix) if current_suffix and current_suffix.isdigit() else None
    if base_version == current_base:
        if bump_wrapper:
            return f"{base_version}-{(current_suffix_num or 0) + 1}"
        return current_version or f"{base_version}-1"
    return f"{base_version}-1"


def main() -> None:
    bump_wrapper = os.environ.get("BUMP_WRAPPER", "false").lower() == "true"
    changed = False

    for update in UPDATES:
        upstream = os.environ.get(update.version_env, "").strip()
        image_tag = os.environ.get(update.tag_env, "").strip()
        if not upstream or not image_tag:
            continue

        config_file = Path(update.slug) / "config.yaml"
        build_file = Path(update.slug) / "build.yaml"
        changelog_file = Path(update.slug) / "CHANGELOG.md"

        config_text = config_file.read_text(encoding="utf-8")
        wrapper_version = next_wrapper_version(current_addon_version(config_text), upstream, bump_wrapper)

        build_text = build_file.read_text(encoding="utf-8")
        new_build = re.sub(rf"{re.escape(update.image)}:[^\n]+", f"{update.image}:{image_tag}", build_text)
        if new_build != build_text:
            build_file.write_text(new_build, encoding="utf-8")
            changed = True

        new_config = re.sub(r'version: "[^"]+"', f'version: "{wrapper_version}"', config_text, count=1)
        if new_config != config_text:
            config_file.write_text(new_config, encoding="utf-8")
            changed = True

        changelog_text = changelog_file.read_text(encoding="utf-8")
        heading = f"## {wrapper_version}"
        if heading not in changelog_text:
            entry = build_changelog_entry(update, wrapper_version, upstream, image_tag)
            lines = changelog_text.splitlines()
            changelog_file.write_text("\n".join(lines[:1] + [""] + entry + lines[1:]).rstrip() + "\n", encoding="utf-8")
            changed = True

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with Path(github_output).open("a", encoding="utf-8") as output:
            output.write(f"changed={str(changed).lower()}\n")
    else:
        print(f"changed={str(changed).lower()}")


if __name__ == "__main__":
    main()
