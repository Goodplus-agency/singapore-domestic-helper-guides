#!/usr/bin/env python3
"""Audit and record Goodplus Blog-to-GitHub synchronization state."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GOODPLUS_ROOT = ROOT.parent / "GoodplusSite"
DEFAULT_MANIFEST_URL = "https://goodplus.com.sg/blog/github-manifest.json"
INDEX_PATH = Path("data/article-index.json")
GUIDE_FRONT_MATTER = re.compile(r"^---\n(?P<header>.*?)\n---\n", re.DOTALL)
MANIFEST_REQUIRED_FIELDS = {
    "key",
    "locale",
    "language",
    "slug",
    "translation_key",
    "title",
    "canonical_url",
    "source_hash",
    "github_path",
}


class SyncError(RuntimeError):
    """Raised when the synchronization contract cannot be verified safely."""


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SyncError(f"Could not read JSON from {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SyncError(f"Expected a JSON object in {path}.")
    return data


def load_manifest(manifest_file: Path | None, manifest_url: str) -> dict[str, Any]:
    if manifest_file is not None:
        manifest = read_json(manifest_file)
    else:
        request = urllib.request.Request(
            manifest_url,
            headers={"User-Agent": "Goodplus-GitHub-Sync/1.0"},
        )
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                manifest = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise SyncError(f"Could not load the live Goodplus manifest: {exc}") from exc

    if manifest.get("schema_version") != 1:
        raise SyncError("Unsupported or missing Goodplus manifest schema_version.")
    if not isinstance(manifest.get("articles"), list):
        raise SyncError("Goodplus manifest must contain an articles array.")

    keys: list[str | None] = []
    for position, article in enumerate(manifest["articles"]):
        label = f"manifest articles[{position}]"
        if not isinstance(article, dict):
            raise SyncError(f"{label} must be an object.")

        missing = sorted(MANIFEST_REQUIRED_FIELDS - article.keys())
        if missing:
            raise SyncError(f"{label} is missing fields: {', '.join(missing)}")

        locale = article.get("locale")
        slug = article.get("slug")
        key = article.get("key")
        if locale not in {"en", "zh"} or not isinstance(slug, str) or not slug:
            raise SyncError(f"{label} has an invalid locale or slug.")
        if key != f"{locale}:{slug}":
            raise SyncError(f"{label} key does not match its locale and slug.")
        if article.get("language") != ("zh-SG" if locale == "zh" else "en-SG"):
            raise SyncError(f"{label} has an invalid language.")
        if article.get("github_path") != f"guides/{locale}/{slug}.md":
            raise SyncError(f"{label} has an invalid github_path.")
        if not re.fullmatch(r"[a-f0-9]{64}", str(article.get("source_hash"))):
            raise SyncError(f"{label} has an invalid source_hash.")
        if not str(article.get("canonical_url")).startswith("https://goodplus.com.sg/"):
            raise SyncError(f"{label} has an invalid canonical_url.")

        keys.append(key)

    if any(not isinstance(key, str) or not key for key in keys):
        raise SyncError("Every manifest article must have a non-empty key.")
    if len(keys) != len(set(keys)):
        raise SyncError("Goodplus manifest contains duplicate article keys.")

    return manifest


def source_path(goodplus_root: Path, article: dict[str, Any]) -> Path:
    return (
        goodplus_root
        / "resources"
        / "content"
        / "blog"
        / str(article["locale"])
        / f"{article['slug']}.md"
    )


def normalized_source_hash(path: Path) -> str:
    try:
        contents = path.read_bytes().decode("utf-8").replace("\r\n", "\n")
    except (OSError, UnicodeDecodeError) as exc:
        raise SyncError(f"Could not read UTF-8 Blog source {path}: {exc}") from exc
    return hashlib.sha256(contents.encode("utf-8")).hexdigest()


def indexed_articles(repo_root: Path) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    index = read_json(repo_root / INDEX_PATH)
    articles = index.get("articles")
    if not isinstance(articles, list):
        raise SyncError("data/article-index.json must contain an articles array.")

    by_key: dict[str, dict[str, Any]] = {}
    for article in articles:
        if not isinstance(article, dict) or not isinstance(article.get("key"), str):
            raise SyncError("Every article-index entry must be an object with a key.")
        if article["key"] in by_key:
            raise SyncError(f"Duplicate article-index key: {article['key']}")
        by_key[article["key"]] = article

    return index, by_key


def safe_repo_path(repo_root: Path, relative_path: str) -> Path:
    resolved = (repo_root / relative_path).resolve()
    try:
        resolved.relative_to(repo_root.resolve())
    except ValueError as exc:
        raise SyncError(f"Repository path leaves the checkout: {relative_path}") from exc
    return resolved


def audit_inventory(
    manifest: dict[str, Any],
    repo_root: Path,
    goodplus_root: Path,
    verify_source: bool = True,
) -> dict[str, list[str]]:
    _, index_by_key = indexed_articles(repo_root)
    manifest_by_key = {article["key"]: article for article in manifest["articles"]}
    result = {
        "translation_missing": [],
        "source_missing": [],
        "source_mismatch": [],
        "missing": [],
        "stale": [],
        "orphaned": [],
        "untracked": [],
        "up_to_date": [],
    }

    translation_groups: dict[str, list[dict[str, Any]]] = {}
    for article in manifest["articles"]:
        translation_key = article.get("translation_key")
        if not isinstance(translation_key, str) or not translation_key:
            result["translation_missing"].append(
                f"{article['key']} (translation_key missing)"
            )
            continue
        translation_groups.setdefault(translation_key, []).append(article)

    for translation_key, articles in sorted(translation_groups.items()):
        locales = [article["locale"] for article in articles]
        if sorted(locales) != ["en", "zh"]:
            missing_locales = sorted({"en", "zh"} - set(locales))
            detail = (
                f"missing {', '.join(missing_locales)}"
                if missing_locales
                else "expected exactly one en and one zh article"
            )
            result["translation_missing"].append(f"{translation_key} ({detail})")

    for key, article in sorted(manifest_by_key.items()):
        if verify_source:
            local_source = source_path(goodplus_root, article)
            if not local_source.is_file():
                result["source_missing"].append(key)
                continue

            local_hash = normalized_source_hash(local_source)
            if local_hash != article.get("source_hash"):
                result["source_mismatch"].append(key)
                continue

        target = safe_repo_path(repo_root, str(article["github_path"]))
        index_entry = index_by_key.get(key)
        if not target.is_file():
            result["missing"].append(key)
        elif index_entry is None:
            result["untracked"].append(key)
        elif index_entry.get("source_hash") != article.get("source_hash"):
            result["stale"].append(key)
        else:
            result["up_to_date"].append(key)

    for key in sorted(index_by_key.keys() - manifest_by_key.keys()):
        result["orphaned"].append(key)

    indexed_paths = {
        str(entry.get("github_path"))
        for entry in index_by_key.values()
        if entry.get("github_path")
    }
    for locale in ("en", "zh"):
        for path in sorted((repo_root / "guides" / locale).glob("*.md")):
            if path.name == "README.md":
                continue
            relative = path.relative_to(repo_root).as_posix()
            if relative not in indexed_paths:
                key = f"{locale}:{path.stem}"
                if key not in result["untracked"]:
                    result["untracked"].append(key)

    return result


def parse_guide_front_matter(path: Path) -> dict[str, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise SyncError(f"Could not read guide {path}: {exc}") from exc

    match = GUIDE_FRONT_MATTER.match(text)
    if not match:
        raise SyncError(f"Guide has no valid front matter: {path}")

    fields: dict[str, str] = {}
    for line in match.group("header").splitlines():
        item = re.match(r"^([a-z][a-z0-9_]*):\s*(.*)$", line)
        if item:
            fields[item.group(1)] = item.group(2).strip().strip('"')
    return fields


def record_entries(
    manifest: dict[str, Any],
    repo_root: Path,
    goodplus_root: Path,
    keys: list[str],
    synced_on: str | None = None,
) -> None:
    index, index_by_key = indexed_articles(repo_root)
    manifest_by_key = {article["key"]: article for article in manifest["articles"]}
    manifest_by_translation: dict[str, list[dict[str, Any]]] = {}
    for article in manifest["articles"]:
        translation_key = article.get("translation_key")
        if isinstance(translation_key, str) and translation_key:
            manifest_by_translation.setdefault(translation_key, []).append(article)

    requested_keys = set(keys)
    for key in keys:
        article = manifest_by_key.get(key)
        if article is None:
            raise SyncError(f"Article is not published in the live manifest: {key}")
        translation_key = article.get("translation_key")
        if not isinstance(translation_key, str) or not translation_key:
            raise SyncError(f"Published article has no translation_key: {key}")

        translated_articles = manifest_by_translation.get(translation_key, [])
        translated_locales = sorted(item["locale"] for item in translated_articles)
        if translated_locales != ["en", "zh"]:
            raise SyncError(
                f"Both English and Chinese website articles must be published before "
                f"recording translation pair {translation_key}."
            )
        pair_keys = {item["key"] for item in translated_articles}
        if not pair_keys.issubset(requested_keys):
            missing_keys = ", ".join(sorted(pair_keys - requested_keys))
            raise SyncError(
                f"Record English and Chinese guides together for {translation_key}; "
                f"missing key(s): {missing_keys}"
            )

    for key in keys:
        article = manifest_by_key.get(key)
        if article is None:
            raise SyncError(f"Article is not published in the live manifest: {key}")

        local_source = source_path(goodplus_root, article)
        if not local_source.is_file():
            raise SyncError(f"Local Blog source is missing for {key}: {local_source}")
        if normalized_source_hash(local_source) != article.get("source_hash"):
            raise SyncError(
                f"Local source does not match the deployed Goodplus article for {key}. "
                "Deploy the website version before recording the GitHub guide."
            )

        guide = safe_repo_path(repo_root, str(article["github_path"]))
        if not guide.is_file():
            raise SyncError(f"GitHub guide is missing for {key}: {guide}")
        fields = parse_guide_front_matter(guide)
        if fields.get("canonical_url") != article.get("canonical_url"):
            raise SyncError(f"Guide canonical_url does not match the live manifest for {key}.")
        if fields.get("language") != article.get("language"):
            raise SyncError(f"Guide language does not match the live manifest for {key}.")

        index_by_key[key] = {
            "key": key,
            "locale": article["locale"],
            "language": article["language"],
            "slug": article["slug"],
            "translation_key": article["translation_key"],
            "title": fields.get("title", article["title"]),
            "canonical_url": article["canonical_url"],
            "github_path": article["github_path"],
            "source_path": local_source.relative_to(goodplus_root).as_posix(),
            "source_hash": article["source_hash"],
            "published_at": article.get("published_at"),
            "last_modified": article.get("last_modified"),
            "synced_on": synced_on or date.today().isoformat(),
        }

    index["updated_on"] = synced_on or date.today().isoformat()
    index["articles"] = [index_by_key[key] for key in sorted(index_by_key)]
    (repo_root / INDEX_PATH).write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def print_audit(result: dict[str, list[str]], as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    labels = {
        "translation_missing": "Published article has no public translation pair",
        "source_missing": "Local source missing",
        "source_mismatch": "Local source differs from deployed website",
        "missing": "Published on website, missing from GitHub",
        "stale": "GitHub guide is stale",
        "orphaned": "GitHub guide is no longer published on website",
        "untracked": "GitHub guide exists but is not recorded",
        "up_to_date": "Up to date",
    }
    for status, label in labels.items():
        values = result[status]
        print(f"{label}: {len(values)}")
        for value in values:
            print(f"  - {value}")


def common_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--manifest-file",
        type=Path,
        help="Read a saved manifest JSON instead of the live website.",
    )
    parser.add_argument(
        "--manifest-url",
        default=DEFAULT_MANIFEST_URL,
        help="Published Goodplus manifest URL.",
    )
    parser.add_argument(
        "--goodplus-root",
        type=Path,
        default=DEFAULT_GOODPLUS_ROOT,
        help="Path to the sibling GoodplusSite checkout.",
    )
    return parser


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    audit_parser = commands.add_parser("audit", parents=[common_parser()])
    audit_parser.add_argument("--json", action="store_true", help="Print JSON output.")
    audit_parser.add_argument(
        "--skip-source-check",
        action="store_true",
        help="Compare the live manifest with this public repository without a Goodplus checkout.",
    )
    record_parser = commands.add_parser("record", parents=[common_parser()])
    record_parser.add_argument("--key", nargs="+", required=True, help="Reviewed article key(s).")
    args = parser.parse_args()

    try:
        manifest = load_manifest(args.manifest_file, args.manifest_url)
        goodplus_root = args.goodplus_root.resolve()
        if args.command == "audit":
            result = audit_inventory(
                manifest,
                ROOT,
                goodplus_root,
                verify_source=not args.skip_source_check,
            )
            print_audit(result, args.json)
            requires_action = any(
                result[status]
                for status in (
                    "translation_missing",
                    "source_missing",
                    "source_mismatch",
                    "missing",
                    "stale",
                    "orphaned",
                    "untracked",
                )
            )
            return 1 if requires_action else 0

        record_entries(manifest, ROOT, goodplus_root, args.key)
        print(f"Recorded {len(args.key)} reviewed guide(s) in {INDEX_PATH.as_posix()}.")
        return 0
    except SyncError as exc:
        print(f"Sync error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
