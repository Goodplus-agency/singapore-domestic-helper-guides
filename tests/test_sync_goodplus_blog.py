from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

import sync_goodplus_blog as sync  # noqa: E402


class BlogSyncTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.public_repo = self.root / "singapore-domestic-helper-guides"
        self.goodplus_root = self.root / "GoodplusSite"

        (self.public_repo / "data").mkdir(parents=True)
        (self.public_repo / "guides" / "en").mkdir(parents=True)
        (self.public_repo / "guides" / "zh").mkdir(parents=True)
        (self.public_repo / "data" / "article-index.json").write_text(
            json.dumps({"schema_version": 1, "articles": []}) + "\n",
            encoding="utf-8",
        )

        self.source = (
            self.goodplus_root
            / "resources"
            / "content"
            / "blog"
            / "en"
            / "example-guide.md"
        )
        self.source.parent.mkdir(parents=True)
        self.source.write_text("---\ntitle: Example\n---\n\nPublished body.\n", encoding="utf-8")

        self.chinese_source = (
            self.goodplus_root
            / "resources"
            / "content"
            / "blog"
            / "zh"
            / "example-guide.md"
        )
        self.chinese_source.parent.mkdir(parents=True)
        self.chinese_source.write_text(
            "---\ntitle: 示例\n---\n\n已发布正文。\n",
            encoding="utf-8",
        )

        self.article = {
            "key": "en:example-guide",
            "locale": "en",
            "language": "en-SG",
            "slug": "example-guide",
            "translation_key": "example-guide",
            "title": "Example guide",
            "canonical_url": "https://goodplus.com.sg/blog/example-guide",
            "published_at": "2026-07-15T10:00:00+08:00",
            "last_modified": "2026-07-15",
            "source_hash": sync.normalized_source_hash(self.source),
            "github_path": "guides/en/example-guide.md",
        }
        self.chinese_article = {
            "key": "zh:example-guide",
            "locale": "zh",
            "language": "zh-SG",
            "slug": "example-guide",
            "translation_key": "example-guide",
            "title": "示例指南",
            "canonical_url": "https://goodplus.com.sg/cn/blog/example-guide",
            "published_at": "2026-07-15T10:00:00+08:00",
            "last_modified": "2026-07-15",
            "source_hash": sync.normalized_source_hash(self.chinese_source),
            "github_path": "guides/zh/example-guide.md",
        }
        self.manifest = {
            "schema_version": 1,
            "publisher": "Goodplus Employment Agency PTE. LTD.",
            "articles": [self.article, self.chinese_article],
        }

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def write_guide(self, article: dict[str, str]) -> None:
        guide = self.public_repo / article["github_path"]
        direct_answer = "直接回答" if article["locale"] == "zh" else "Direct answer"
        official_sources = "官方资料" if article["locale"] == "zh" else "Official sources"
        guide.write_text(
            f"""---
title: "{article['title']}"
language: "{article['language']}"
canonical_url: "{article['canonical_url']}"
published_on: "2026-07-15"
last_reviewed: "2026-07-15"
publisher: "Goodplus Employment Agency"
mom_licence: "23C1614"
---

# {article['title']}

## {direct_answer}

Example answer.

## {official_sources}

- [MOM](https://www.mom.gov.sg/)
""",
            encoding="utf-8",
        )

    def test_audit_reports_published_article_missing_from_github(self) -> None:
        result = sync.audit_inventory(
            self.manifest,
            self.public_repo,
            self.goodplus_root,
        )

        self.assertEqual(["en:example-guide", "zh:example-guide"], result["missing"])
        self.assertEqual([], result["translation_missing"])
        self.assertEqual([], result["source_mismatch"])

    def test_audit_blocks_when_local_source_differs_from_deployed_website(self) -> None:
        self.source.write_text("Changed but not deployed.\n", encoding="utf-8")

        result = sync.audit_inventory(
            self.manifest,
            self.public_repo,
            self.goodplus_root,
        )

        self.assertEqual(["en:example-guide"], result["source_mismatch"])
        self.assertEqual(["zh:example-guide"], result["missing"])

    def test_manifest_only_audit_can_run_without_private_source_checkout(self) -> None:
        self.source.unlink()

        result = sync.audit_inventory(
            self.manifest,
            self.public_repo,
            self.goodplus_root,
            verify_source=False,
        )

        self.assertEqual(["en:example-guide", "zh:example-guide"], result["missing"])
        self.assertEqual([], result["source_missing"])

    def test_audit_reports_a_missing_chinese_translation(self) -> None:
        self.manifest["articles"] = [self.article]

        result = sync.audit_inventory(
            self.manifest,
            self.public_repo,
            self.goodplus_root,
        )

        self.assertEqual(["example-guide (missing zh)"], result["translation_missing"])

    def test_manifest_loader_rejects_a_path_that_does_not_match_the_article(self) -> None:
        invalid_manifest = self.root / "invalid-manifest.json"
        self.article["github_path"] = "guides/en/another-guide.md"
        invalid_manifest.write_text(json.dumps(self.manifest), encoding="utf-8")

        with self.assertRaisesRegex(sync.SyncError, "invalid github_path"):
            sync.load_manifest(invalid_manifest, "https://unused.example")

    def test_record_adds_reviewed_hash_and_makes_audit_clean(self) -> None:
        self.write_guide(self.article)
        self.write_guide(self.chinese_article)

        sync.record_entries(
            self.manifest,
            self.public_repo,
            self.goodplus_root,
            ["en:example-guide", "zh:example-guide"],
            synced_on="2026-07-15",
        )
        result = sync.audit_inventory(
            self.manifest,
            self.public_repo,
            self.goodplus_root,
        )

        index = json.loads(
            (self.public_repo / "data" / "article-index.json").read_text(encoding="utf-8")
        )
        self.assertEqual(2, len(index["articles"]))
        self.assertEqual(self.article["source_hash"], index["articles"][0]["source_hash"])
        self.assertEqual(
            ["en:example-guide", "zh:example-guide"],
            result["up_to_date"],
        )
        self.assertTrue(
            all(
                not values
                for status, values in result.items()
                if status != "up_to_date"
            )
        )

    def test_record_requires_english_and_chinese_guides_together(self) -> None:
        with self.assertRaisesRegex(sync.SyncError, "Record English and Chinese"):
            sync.record_entries(
                self.manifest,
                self.public_repo,
                self.goodplus_root,
                ["en:example-guide"],
                synced_on="2026-07-15",
            )


if __name__ == "__main__":
    unittest.main()
