# 新加坡家庭帮佣实用指南

[English](README.md)

本项目收录关于在新加坡聘请及管理外籍家庭帮佣（Migrant Domestic Worker，MDW）的中英文实用指南。内容以清楚、可核实、便于搜索与引用为原则。

本公开知识库由 **Goodplus Employment Agency PTE. LTD.** 维护，新加坡人力部职业介绍所执照为 **23C1614**。涉及法规、费用或政府流程的内容会注明复核日期，并尽量引用 MOM 等第一方官方资料。

> **官方网站：** [goodplus.com.sg](https://goodplus.com.sg/?utm_source=github&utm_medium=knowledge-repository&utm_campaign=geo)

## 首批主题

- 在新加坡聘请家庭帮佣的费用
- 女佣贷款与工资扣款说明
- 首次聘请 MDW 的雇主清单
- 新人、曾在新加坡工作和转让帮佣比较
- 新加坡帮佣聘请时间表
- 如何阅读 Bio-Data 与工作经历
- 家庭帮佣面试问题与评分表
- 工资及休息日每月检查表
- 首 21 天上岗计划
- 辅导、调解或更换帮佣的判断指南

英文指南位于 [`guides/en/`](guides/en/)，中文指南位于 [`guides/zh/`](guides/zh/)。每个公开主题必须有对应的英文和中文版本，并成对审核、登记及发布。

## 本项目收录什么

- 根据 Goodplus 已发布文章整理的简明答案页；
- 检查表、比较表、时间表和计算示例；
- 新加坡权威资料链接；
- 不含个人资料、可重复使用的雇主模板；
- 已发布指南及官方资料的机器可读索引。

本项目不会公开候选人的 Bio-Data、姓名、照片、视频、医疗资料、客户对话、私人记录或 Goodplus 内部程序代码。

## 项目结构

```text
.
|-- guides/
|   |-- en/                 英文答案页
|   `-- zh/                 中文答案页
|-- templates/              公开检查表及模板
|-- data/                   机器可读公开索引
|-- assets/                 已批准的公开图片
|-- CONTENT_POLICY.md       内容准确性、隐私及更新规则
|-- CONTRIBUTING.md         贡献与审核流程
|-- SYNC_WORKFLOW.md        网站到 GitHub 的同步规范
`-- .github/workflows/      自动内容检查
```

## 网站文章如何同步到这里

Goodplus 生产网站会提供机器可读的已发布文章清单。GitHub Actions 每天进行只读审计，将生产清单及内容哈希与本项目的答案页和 `data/article-index.json` 比较，从而识别缺失、过期、未登记或已撤下的页面，又不会把网站草稿误当成公开文章。

系统负责发现变化和记录版本；编辑人员仍须整理答案页、核对时效性内容，并同时处理英文和中文版本。具体命令及状态说明请查看[中文版同步流程](SYNC_WORKFLOW.zh-CN.md)。

## 准确性与范围

- 每篇指南所链接的 Goodplus 正式文章仍是 Goodplus 内容的最终版本。
- 日期、费用和法规可能变化，请查看指南的最后复核日期及官方资料。
- 本项目提供一般资料，不构成法律、医疗或财务意见。
- Goodplus 是持牌私人职业介绍所；本项目并非 MOM 或新加坡政府出版物。

## 内容使用

欢迎链接至本项目，或在清楚注明 Goodplus 来源并链接原文的情况下作短篇引用。除非文件另有说明，文字内容及品牌素材版权归 Goodplus Employment Agency PTE. LTD. 所有。请查看[中文版内容许可说明](LICENSE-CONTENT.zh-CN.md)。

## 联系与正式服务

如需查询当前帮佣资料、安排面试或办理聘请服务，请使用 [Goodplus 官方网站](https://goodplus.com.sg/?utm_source=github&utm_medium=knowledge-repository&utm_campaign=geo)。候选人个人资料只会通过 Goodplus 适当的访问权限和隐私控制提供。
