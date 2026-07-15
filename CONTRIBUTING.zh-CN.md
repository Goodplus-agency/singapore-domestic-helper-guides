# 贡献说明

[English](CONTRIBUTING.md)

感谢你协助改善这些新加坡家庭帮佣指南。

## 提交修改前

1. 查看 [goodplus.com.sg](https://goodplus.com.sg/) 上对应的正式文章。
2. 涉及 MOM 规则或政府要求时，使用当前的第一方资料。
3. 不得加入候选人、雇主、客户或员工的个人资料。
4. 底层事实变化时，同时检查英文和中文页面；每一对翻译必须一同新增、登记和提交。
5. 使用[中文答案页模板](docs/GUIDE_TEMPLATE.zh-CN.md)。
6. 同步 Goodplus Blog 时，先运行审计并遵守[中文版同步流程](SYNC_WORKFLOW.zh-CN.md)，不得仅凭源文件存在就判断文章已经发布。

## Pull Request 要求

- 说明这次修改回答什么问题。
- 涉及规则的修改须说明所采用的官方资料。
- 只有真正完成复核后，才更新 `last_reviewed`。
- Blog 答案页审核完成后，使用 `scripts/sync_goodplus_blog.py record` 登记已核实的生产版本哈希，并同时登记中英文版本。
- 页面重命名或撤下时，在同一次修改中更新指南和 `data/article-index.json`。
- 提交前运行内容校验、同步工具单元测试和最终审计。
- 完成 Pull Request 检查清单。

Goodplus 维护人员可以编辑、拒绝或撤下贡献，以保障准确性、隐私和编辑一致性。

## 报告错误

建立 Issue 时，请指出受影响文件、可能错误的内容，以及支持更正的第一方资料。不要在 Issue 中公开个人资料或候选人档案。
