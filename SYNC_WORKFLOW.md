# Website synchronization workflow

[简体中文版](SYNC_WORKFLOW.zh-CN.md)

This repository represents selected articles that are already public on [goodplus.com.sg](https://goodplus.com.sg/). It does not decide which Goodplus Blog drafts are approved for publication.

## Sources of truth

1. `https://goodplus.com.sg/blog/github-manifest.json` is the production publication inventory.
2. The matching Goodplus Markdown source may be used only when its SHA-256 hash matches the manifest.
3. `data/article-index.json` records the exact production source hash reviewed into each GitHub guide.
4. Current first-party Singapore Government pages remain the source for rule-sensitive facts.

The manifest intentionally contains only safe public metadata. It does not expose article bodies, editorial notes or drafts.

## Audit

With `GoodplusSite` and this repository checked out as siblings, run:

```powershell
python scripts\sync_goodplus_blog.py audit --goodplus-root ..\GoodplusSite
```

For machine-readable output:

```powershell
python scripts\sync_goodplus_blog.py audit --goodplus-root ..\GoodplusSite --json
```

The scheduled GitHub Actions workflow runs a public-inventory-only variant:

```powershell
python scripts\sync_goodplus_blog.py audit --skip-source-check
```

That mode does not need the private Goodplus checkout and can automatically detect `translation_missing`, `missing`, `stale`, `untracked` and `orphaned` pages. It must not be used to approve or record content; run the full local source check before editing.

Use `--manifest-file path/to/manifest.json` only for a saved, trusted manifest fixture or an offline test. Normal publication decisions must use the production endpoint.

The audit exits `0` when clean, `1` when content action is required and `2` when the source state cannot be verified safely.

## Status meanings

| Status | Meaning |
|---|---|
| `translation_missing` | A public article does not yet have both an English and Chinese public counterpart. |
| `source_missing` | The live article is absent from the local Goodplus checkout. |
| `source_mismatch` | The local article differs from the deployed website version. |
| `missing` | A live Goodplus article has no GitHub guide. |
| `stale` | A guide represents an older production source hash. |
| `untracked` | A guide exists but has not been recorded in the index. |
| `orphaned` | An indexed guide is no longer live on Goodplus. |
| `up_to_date` | The guide represents the current live source hash. |

Do not prepare or record a guide while its key is `source_missing` or `source_mismatch`. A `translation_missing` pair must first be completed and published on the Goodplus website; never use a website draft to fill the gap.

## Add or update a guide

1. Run the audit.
2. Work only on eligible `missing` or `stale` keys, and handle the English and Chinese translation pair in the same batch.
3. Follow [CONTENT_POLICY.md](CONTENT_POLICY.md) and [docs/GUIDE_TEMPLATE.md](docs/GUIDE_TEMPLATE.md).
4. Write a concise answer pack; do not blindly mirror the full website article.
5. Check current regulatory claims against first-party sources.
6. Review the page and then record the production version:

```powershell
python scripts\sync_goodplus_blog.py record `
  --goodplus-root ..\GoodplusSite `
  --key en:example-slug zh:example-slug
```

The `record` operation verifies that both translations are live and supplied together, each local source matches production, each guide exists, and its language and canonical URL are correct. It then writes the source hash and synchronization metadata to `data/article-index.json`.

Do not manually invent or copy a `source_hash`.

## Withdrawal

An `orphaned` result requires an editorial decision. Remove an obsolete guide or replace it with an accurate successor, and update `data/article-index.json` in the same change. Do not leave withdrawn pricing, rules or process guidance public without review.

## Required checks

Before committing:

```powershell
python scripts\validate_content.py
python -m unittest discover -s tests
python scripts\sync_goodplus_blog.py audit --goodplus-root ..\GoodplusSite
```

The validator ensures every answer pack has safe metadata and an index record. The final audit confirms the recorded source hashes still match production.

## Publication rule

Content preparation and validation are separate from GitHub publication. Commit, push or open a pull request only with explicit maintainer authorization. Substantive public content updates should normally use a reviewable branch and pull request.
