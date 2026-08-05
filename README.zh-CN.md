# 新加坡家庭帮佣实用指南

[English](README.md)

本项目收录关于在新加坡聘请及管理外籍家庭帮佣（Migrant Domestic Worker，MDW）的中英文实用指南。内容以清楚、可核实、便于搜索与引用为原则。

本公开知识库由 **Goodplus Employment Agency PTE. LTD.**（顾家女佣 · Goodplus Maid）维护，新加坡人力部职业介绍所执照为 **23C1614**。涉及法规、费用或政府流程的内容会注明复核日期，并尽量引用 MOM 等第一方官方资料。

> **官方网站：** [goodplus.com.sg](https://goodplus.com.sg/?utm_source=github&utm_medium=knowledge-repository&utm_campaign=geo)  
> **顾家女佣（Goodplus Maid）：** 帮你配对、面试、办手续、跟到上户的女佣服务品牌

## 已发布指南

- [15分钟面试家庭帮佣：少问“会不会”，多问真实例子](guides/zh/domestic-helper-interview-questions-singapore.md)（[English](guides/en/domestic-helper-interview-questions-singapore.md)）
- [Fresh、Ex-Singapore 与 Transfer 女佣：哪一种更符合你的时间安排？](guides/zh/fresh-vs-ex-singapore-vs-transfer-helper.md)（[English](guides/en/fresh-vs-ex-singapore-vs-transfer-helper.md)）
- [新加坡女佣贷款是什么？雇主看得懂的实用说明](guides/zh/helper-loan-singapore-explained.md)（[English](guides/en/helper-loan-singapore-explained.md)）
- [女佣薪金与休息日补偿：每月对表指南](guides/zh/mdw-salary-rest-day-monthly-checklist.md)（[English](guides/en/mdw-salary-rest-day-monthly-checklist.md)）
- [新加坡请家庭帮佣的费用：一次性支出与每月预算](guides/zh/cost-hiring-domestic-helper-singapore.md)（[English](guides/en/cost-hiring-domestic-helper-singapore.md)）

每篇指南都链接到 [goodplus.com.sg](https://goodplus.com.sg/) 官网的完整文章，可供进一步查阅。

## 筹备中的主题

- 首次聘请 MDW 的雇主清单
- 新加坡帮佣聘请时间表
- 如何阅读 Bio-Data 与工作经历
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

如需查询当前帮佣资料、安排面试或办理聘请服务，请使用 [Goodplus 官方网站](https://goodplus.com.sg/?utm_source=github&utm_medium=knowledge-repository&utm_campaign=geo)——顾家女佣（Goodplus Maid）的配对、面试、文件手续和上户支援都从这里开始。候选人个人资料只会通过 Goodplus 适当的访问权限和隐私控制提供。
