# 网站文章同步流程

[English](SYNC_WORKFLOW.md)

本项目只整理已经在 [goodplus.com.sg](https://goodplus.com.sg/) 正式发布的文章，不负责判断 Goodplus Blog 草稿是否获准发布。

## 最终依据

1. `https://goodplus.com.sg/blog/github-manifest.json` 是生产网站的已发布文章清单。
2. 只有本地 Goodplus Markdown 源文件的 SHA-256 哈希与生产清单一致时，才可用来整理内容。
3. `data/article-index.json` 记录每个 GitHub 指南所对应、已经审核的生产文章哈希。
4. 涉及规则的事实仍以当前的新加坡第一方政府资料为准。

生产清单只包含安全的公开元数据，不会公开文章正文、编辑备注或草稿。

## 审计命令

当 `GoodplusSite` 与本项目位于同一个父目录时，运行：

```powershell
python scripts\sync_goodplus_blog.py audit --goodplus-root ..\GoodplusSite
```

如需机器可读输出：

```powershell
python scripts\sync_goodplus_blog.py audit --goodplus-root ..\GoodplusSite --json
```

每天运行的 GitHub Actions 只读检查使用：

```powershell
python scripts\sync_goodplus_blog.py audit --skip-source-check
```

这个模式不需要访问 Goodplus 私有仓库，可以自动发现缺失、过期、未登记、翻译不完整和已撤下页面；但它不能批准或登记内容。编辑前仍须在本地运行完整的源文件哈希检查。

`--manifest-file path/to/manifest.json` 只应用于可信的已保存清单或离线测试。正常发布判断必须使用生产端点。

审计返回码：`0` 表示完全一致；`1` 表示需要内容处理；`2` 表示无法安全确认来源状态。

## 状态说明

| 状态 | 含义 |
|---|---|
| `translation_missing` | 正式文章尚未同时拥有公开的英文和中文版本。 |
| `source_missing` | 本地 Goodplus 检出中缺少生产文章源文件。 |
| `source_mismatch` | 本地文章与生产网站版本不同。 |
| `missing` | Goodplus 已正式发布，但 GitHub 没有对应指南。 |
| `stale` | GitHub 指南对应的是较旧的生产文章哈希。 |
| `untracked` | 指南存在，但尚未登记到索引。 |
| `orphaned` | 已登记指南对应的文章已不在 Goodplus 生产清单中。 |
| `up_to_date` | 指南与当前生产文章哈希一致。 |

出现 `source_missing` 或 `source_mismatch` 时，不得整理或登记该文章。出现 `translation_missing` 时，应先在 Goodplus 网站完成并发布缺少的语言版本，绝不可用网站草稿填补 GitHub 版本。

## 新增或更新指南

1. 运行完整审计。
2. 只处理符合条件的 `missing` 或 `stale` 项，并在同一批次处理英文及中文版本。
3. 遵守[中文版内容政策](CONTENT_POLICY.zh-CN.md)和[中文答案页模板](docs/GUIDE_TEMPLATE.zh-CN.md)。
4. 编写简明答案页，不要直接复制整篇网站文章。
5. 使用第一方资料复核当前法规内容。
6. 两个语言版本都审核后，登记生产版本：

```powershell
python scripts\sync_goodplus_blog.py record `
  --goodplus-root ..\GoodplusSite `
  --key en:example-slug zh:example-slug
```

`record` 会确认中英文网站文章都已正式发布并同时提供、本地源文件与生产版本一致、两个指南均存在，以及语言和正式网址正确，然后把哈希及同步资料写入 `data/article-index.json`。

不要手动编造或复制 `source_hash`。

## 撤下处理

`orphaned` 状态需要编辑决定。应删除过时指南或用准确的新页面替代，并在同一次修改中更新 `data/article-index.json`。不得让已撤下的价格、规则或流程资料长期公开。

## 必须运行的检查

提交前运行：

```powershell
python scripts\validate_content.py
python -m unittest discover -s tests
python scripts\sync_goodplus_blog.py audit --goodplus-root ..\GoodplusSite
```

校验器会确认每个答案页具有安全元数据、中英文配对和索引记录；最终审计确认所登记的源文件哈希仍与生产网站一致。

## 发布规则

整理和验证内容不等于获得 GitHub 发布授权。只有维护人员明确要求时才可 Commit、Push 或建立 Pull Request。重要公开内容更新通常应通过可审核的分支和 Pull Request 完成。
