# Singapore Domestic Helper Guides

[简体中文版](README.zh-CN.md)

Practical, evidence-based English and Chinese guides for hiring and managing migrant domestic workers (MDWs) in Singapore.

This public knowledge base is maintained by **Goodplus Employment Agency PTE. LTD.** (MOM Employment Agency Licence **23C1614**). Rule-sensitive guidance is checked against current Singapore Ministry of Manpower (MOM) sources and includes a visible review date.

> **Official website:** [goodplus.com.sg](https://goodplus.com.sg/?utm_source=github&utm_medium=knowledge-repository&utm_campaign=geo)

## Guides we are preparing

- Cost of hiring a domestic helper in Singapore
- Helper loan and salary deductions explained
- First-time MDW employer checklist
- Fresh, ex-Singapore and transfer helper comparison
- Singapore helper hiring timeline
- How to read Bio-Data and employment history
- Domestic helper interview questions and scorecard
- Salary and rest-day monthly checklist
- First 21 days onboarding plan
- Coach, mediate or replace decision guide

English guides will live in [`guides/en/`](guides/en/). Chinese guides will live in [`guides/zh/`](guides/zh/).

## 中文说明

这是由 **Goodplus Employment Agency PTE. LTD.**（新加坡人力部职业介绍所执照 **23C1614**）维护的公开知识库，提供关于在新加坡聘请及管理家庭帮佣的中英文实用指南。完整中文说明请查看[中文版 README](README.zh-CN.md)。

涉及法规、费用或政府流程的内容，会注明最后复核日期并链接至 MOM 等第一方资料。中文指南将收录于 [`guides/zh/`](guides/zh/)。

## What belongs here

- concise answer pages derived from approved Goodplus guides;
- checklists, comparison tables and worked examples;
- links to authoritative Singapore sources;
- reusable employer templates that contain no personal data;
- a machine-readable index of published guides and official resources.

This repository does **not** publish candidate Bio-Data, names, photos, videos, medical information, customer conversations, private records or internal Goodplus application code.

## Repository structure

```text
.
|-- guides/
|   |-- en/                 English answer pages
|   `-- zh/                 Chinese answer pages
|-- templates/              Public employer checklists and templates
|-- data/                   Machine-readable public indexes
|-- assets/                 Approved public illustrations
|-- CONTENT_POLICY.md       Accuracy, privacy and update rules
|-- CONTRIBUTING.md         Contribution and review process
|-- SYNC_WORKFLOW.md        Website-to-GitHub synchronization contract
`-- .github/workflows/      Automated content validation
```

## How website updates reach this repository

The production Goodplus website publishes a machine-readable inventory of live Blog articles. A daily read-only GitHub Actions audit compares that inventory and its source hashes with the answer packs and `data/article-index.json` in this repository. It detects missing translations, missing pages, stale pages, untracked pages and withdrawals without treating unpublished Blog drafts as public.

Editorial review remains required: the tool identifies what changed and records the reviewed version, while maintainers write concise answer packs and verify time-sensitive facts. See [SYNC_WORKFLOW.md](SYNC_WORKFLOW.md) for commands and status handling.

## Accuracy and scope

- The official Goodplus article linked from each guide remains the source of truth.
- Dates, fees and regulatory requirements can change. Check the guide's `Last reviewed` date and its linked official sources.
- This repository provides general information, not legal, medical or financial advice.
- Goodplus is a licensed private employment agency. This repository is not an MOM or Singapore Government publication.

## Content use

Linking to these guides and short quotations with clear attribution are welcome. Unless a file states otherwise, written content and brand assets remain copyright Goodplus Employment Agency PTE. LTD. See [LICENSE-CONTENT.md](LICENSE-CONTENT.md).

## Contact and official services

For current helper availability, interviews or hiring services, use the [official Goodplus website](https://goodplus.com.sg/?utm_source=github&utm_medium=knowledge-repository&utm_campaign=geo). Personal candidate information is available only through the appropriate Goodplus access and privacy controls.
