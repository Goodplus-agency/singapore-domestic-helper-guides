# Contributing

[简体中文版](CONTRIBUTING.zh-CN.md)

Thank you for helping improve these Singapore domestic-helper guides.

## Before proposing a change

1. Check the matching article on [goodplus.com.sg](https://goodplus.com.sg/).
2. Use a current first-party source for MOM rules or Government requirements.
3. Do not include candidate, employer, customer or staff personal data.
4. Keep English and Chinese pages aligned when the underlying fact changes; add, record and submit each translation pair together.
5. Use the answer-pack structure in [docs/GUIDE_TEMPLATE.md](docs/GUIDE_TEMPLATE.md).
6. For a Goodplus Blog synchronization, run the audit and follow [SYNC_WORKFLOW.md](SYNC_WORKFLOW.md). Do not infer publication from a source file alone.

## Pull request requirements

- Explain what question the change answers.
- Identify the official source used for any rule-sensitive update.
- Update `last_reviewed` only when the page was genuinely checked.
- Use `scripts/sync_goodplus_blog.py record` after reviewing an added or updated Blog-derived guide. This records the verified production source hash in `data/article-index.json`.
- Update the guide and `data/article-index.json` together when renaming or withdrawing a page.
- Run `python scripts/validate_content.py`, the synchronization unit tests and a final audit before submitting.
- Complete the pull request checklist.

Goodplus maintainers may edit, decline or withdraw contributions to protect accuracy, privacy and editorial consistency.

## Reporting an error

Open an issue with the affected file, the statement that may be wrong and a first-party source supporting the correction. Do not post personal information or a candidate profile in an issue.
