#!/usr/bin/env python3
"""Validate public guide metadata and prevent common publication leaks."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDE_ROOT = ROOT / "guides"
REQUIRED_FIELDS = {
    "title",
    "language",
    "canonical_url",
    "published_on",
    "last_reviewed",
    "publisher",
    "mom_licence",
}
FORBIDDEN_TEXT = {
    "source_notes:": "internal source notes",
    "{company_whatsapp_url}": "unresolved application placeholder",
    "APP_KEY": "application secret name",
    "DB_PASSWORD": "database secret name",
}
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
INDEX_REQUIRED_FIELDS = {
    "key",
    "locale",
    "language",
    "slug",
    "translation_key",
    "title",
    "canonical_url",
    "github_path",
    "source_path",
    "source_hash",
    "synced_on",
}


def parse_front_matter(path: Path, text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing opening YAML front matter")

    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("missing closing YAML front matter")

    fields: dict[str, str] = {}
    for line_number, line in enumerate(text[4:end].splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^([a-z][a-z0-9_]*):\s*(.*)$", line)
        if not match:
            raise ValueError(f"invalid front-matter line {line_number}: {line}")
        fields[match.group(1)] = match.group(2).strip().strip('"')

    missing = sorted(REQUIRED_FIELDS - fields.keys())
    if missing:
        raise ValueError(f"missing required fields: {', '.join(missing)}")

    return fields


def validate_date(value: str, field: str) -> None:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field} must use YYYY-MM-DD") from exc

    if parsed > date.today():
        raise ValueError(f"{field} cannot be in the future")


def validate_guide(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ["file is not valid UTF-8"]

    for needle, label in FORBIDDEN_TEXT.items():
        if needle in text:
            errors.append(f"contains {label}: {needle}")

    try:
        fields = parse_front_matter(path, text)
    except ValueError as exc:
        return errors + [str(exc)]

    locale = path.parent.name
    expected_language = "en-SG" if locale == "en" else "zh-SG"
    expected_prefix = (
        "https://goodplus.com.sg/blog/"
        if locale == "en"
        else "https://goodplus.com.sg/cn/blog/"
    )

    if fields["language"] != expected_language:
        errors.append(f"language must be {expected_language}")
    if not fields["canonical_url"].startswith(expected_prefix):
        errors.append(f"canonical_url must start with {expected_prefix}")
    if "?" in fields["canonical_url"] or "#" in fields["canonical_url"]:
        errors.append("canonical_url must not contain query parameters or fragments")
    if fields["publisher"] != "Goodplus Employment Agency":
        errors.append("publisher must be Goodplus Employment Agency")
    if fields["mom_licence"] != "23C1614":
        errors.append("mom_licence must be 23C1614")

    for field in ("published_on", "last_reviewed"):
        try:
            validate_date(fields[field], field)
        except ValueError as exc:
            errors.append(str(exc))

    if "## Direct answer" not in text and "## 直接回答" not in text:
        errors.append("missing Direct answer / 直接回答 section")
    if "## Official sources" not in text and "## 官方资料" not in text:
        errors.append("missing Official sources / 官方资料 section")

    return errors


def load_json(relative_path: str) -> object:
    path = ROOT / relative_path
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_local_links() -> list[str]:
    errors: list[str] = []

    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue

        text = path.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().strip("<>")
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue

            target = target.split("#", 1)[0].split("?", 1)[0]
            if not target:
                continue

            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(
                    f"{path.relative_to(ROOT)}: local link leaves repository: {raw_target}"
                )
                continue

            if not resolved.exists():
                errors.append(
                    f"{path.relative_to(ROOT)}: broken local link: {raw_target}"
                )

    return errors


def validate_article_index(index: object, guide_paths: list[Path]) -> list[str]:
    errors: list[str] = []
    if not isinstance(index, dict) or not isinstance(index.get("articles"), list):
        return ["data/article-index.json must contain an articles array"]

    indexed_paths: set[str] = set()
    indexed_keys: set[str] = set()
    translation_groups: dict[str, list[str]] = {}
    for position, entry in enumerate(index["articles"]):
        label = f"data/article-index.json articles[{position}]"
        if not isinstance(entry, dict):
            errors.append(f"{label} must be an object")
            continue

        missing = sorted(INDEX_REQUIRED_FIELDS - entry.keys())
        if missing:
            errors.append(f"{label} missing fields: {', '.join(missing)}")
            continue

        key = str(entry["key"])
        github_path = str(entry["github_path"])
        if key in indexed_keys:
            errors.append(f"{label} duplicates key {key}")
        indexed_keys.add(key)
        if github_path in indexed_paths:
            errors.append(f"{label} duplicates github_path {github_path}")
        indexed_paths.add(github_path)

        expected_path = f"guides/{entry['locale']}/{entry['slug']}.md"
        if github_path != expected_path:
            errors.append(f"{label} github_path must be {expected_path}")
        if key != f"{entry['locale']}:{entry['slug']}":
            errors.append(f"{label} key must match locale and slug")
        expected_language = "zh-SG" if entry["locale"] == "zh" else "en-SG"
        if entry["language"] != expected_language:
            errors.append(f"{label} language must be {expected_language}")

        translation_key = str(entry["translation_key"])
        if not translation_key:
            errors.append(f"{label} translation_key must not be empty")
        else:
            translation_groups.setdefault(translation_key, []).append(str(entry["locale"]))
        if not re.fullmatch(r"[a-f0-9]{64}", str(entry["source_hash"])):
            errors.append(f"{label} source_hash must be a lowercase SHA-256 hash")
        if not (ROOT / github_path).is_file():
            errors.append(f"{label} points to missing guide {github_path}")
        try:
            validate_date(str(entry["synced_on"]), "synced_on")
        except ValueError as exc:
            errors.append(f"{label} {exc}")

    for translation_key, locales in sorted(translation_groups.items()):
        if sorted(locales) != ["en", "zh"]:
            errors.append(
                "data/article-index.json translation pair "
                f"{translation_key} must contain exactly one English and one Chinese guide"
            )

    actual_paths = {path.relative_to(ROOT).as_posix() for path in guide_paths}
    for path in sorted(actual_paths - indexed_paths):
        errors.append(f"guide is missing from data/article-index.json: {path}")
    for path in sorted(indexed_paths - actual_paths):
        errors.append(f"article index contains a non-guide path: {path}")

    return errors


def main() -> int:
    failures: list[str] = []
    article_index: object | None = None

    for relative_path in (
        "data/article-index.json",
        "data/official-mdw-resources.json",
    ):
        try:
            data = load_json(relative_path)
            if relative_path == "data/article-index.json":
                article_index = data
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"{relative_path}: invalid JSON: {exc}")

    guide_paths = sorted(
        path
        for locale in ("en", "zh")
        for path in (GUIDE_ROOT / locale).glob("*.md")
        if path.name != "README.md"
    )

    for path in guide_paths:
        for error in validate_guide(path):
            failures.append(f"{path.relative_to(ROOT)}: {error}")

    if article_index is not None:
        failures.extend(validate_article_index(article_index, guide_paths))

    failures.extend(validate_local_links())

    if failures:
        print("Content validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Content validation passed ({len(guide_paths)} guide files checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
