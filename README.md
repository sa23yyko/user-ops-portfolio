# 教育科技用户运营作品集

**模拟数据 / 独立项目。当前为第一阶段：数据核验、SQL / 分析脚本、案例文案初稿。尚未制作作品集网页。**

研究问题：语言学习产品的新用户为什么没有开始学习，或开始之后未能持续使用？

## 当前成果

- `DATA_QUALITY_AUDIT.md`：V1 数据登记、六类质量与分析边界审计、未来 V2 的独立保存规则。
- `PORTFOLIO_CASE_STUDY.md`：中文案例初稿，含核验指标、分群与行为分析、策略建议、实验框架和限制。
- `sql/funnel_analysis.sql`：SQLite 用户级指标视图及七组汇总查询。
- `analysis/verify_metrics.py`：原始 CSV 检查、独立 Python 计算、内存 SQLite 查询、逐用户对账和结果导出，仅使用 Python 标准库。
- `analysis/test_verify_metrics.py`：5 项关键口径测试，使用独立人工测试数据。
- `analysis/results/verification_report.md`：自动生成的数据核验报告。
- `analysis/results/metrics.json`：全部结果、源文件及 SQL 指纹、数据诊断完整用户 ID。
- `analysis/results/*.csv`：核心指标、分群、首日任务、学习活跃度、流失召回、注册队列、事件分布及逐用户指标。

原始数据与研究资料保留原路径：

- `english_app_user_events_1000.csv`：1000 名模拟用户的 7306 条行为记录。
- `教育行业用户运营_用户研究成果包/`：模拟访谈 Word/PDF、Excel、3 份研究 CSV、质性 SQL、已有研究展示 HTML。
- `Codex_用户运营作品集交接包/`：项目主上下文、执行指令和操作指南。

## 数据版本

现有行为 CSV 及研究资料登记为 **V1 模拟数据 / 独立项目基线**，保留原文件与内容；`analysis/results/` 是 V1 分析结果。本轮未生成 V2，不静默补造或删除事件。V1 行为 CSV 的 SHA-256、六类问题与处理方式见 [DATA_QUALITY_AUDIT.md](DATA_QUALITY_AUDIT.md)。

如未来生成 V2，须另存 `data/v2/` 并使用独立输出目录 `analysis/results_v2/`，记录生成规则、种子、用途及 V1 / V2 差异。不得覆盖 V1 或将版本间的指标变化描述为运营提升。

## 复现

在项目根目录使用 Python 3.9 或以上版本：

```bash
python3 analysis/verify_metrics.py
python3 -B -m unittest discover -s analysis -p 'test_*.py' -v
```

脚本自动以只读方式加载原始 CSV，在内存 SQLite 中创建 `user_events` 表，执行 `sql/funnel_analysis.sql`，并将结果写入 `analysis/results/`。不需要现有数据库、第三方依赖或联网。重复执行会覆盖这些生成结果，不会改写原始 CSV、Excel、Word 或交接文档。输出不含运行时间戳，同一输入和代码应生成相同文件内容。

Python 独立计算每个用户的注册日、激活、D1、D7、首日完成、D0–D6 学习天数及流失召回日期，再与 SQL 逐用户比较。若字段、日期、注册记录、类型一致性、重复行或 D7 观察窗检查失败，脚本报错，不生成新结果；此前结果如存在仍是旧版本，不能当作本次成功产物。

在 DB Browser for SQLite 中复现 SQL：将行为 CSV 导入一张名为 `user_events` 的表，勾选首行为列名，保持四列名称与 CSV 一致并使用文本类型；在同一数据库连接中先执行 SQL 文件首段 `CREATE TEMP VIEW`，再依次执行各个 `-- report:` 后的查询。临时视图只在当前连接有效；重复执行建视图前可重开数据库连接。不要将旧的质性编码 SQL 当成行为漏斗 SQL。

更新数据时，建议另存新 CSV，然后指定输入与独立输出目录：

```bash
python3 analysis/verify_metrics.py --input /absolute/path/new_events.csv --output /absolute/path/new_results
```

如果新数据不满足当前口径，先更新口径和验证，不要为复现旧数字删改数据。案例文案为人工整理，不会随脚本自动更新；数据变更后需要依据新报告同步修订。

## 关键口径

- 激活：注册日 `start_learning`；首日完成任务另用 `complete_task` 统计。
- D1 / D7：注册后第 1 / 7 天 `open_app`，分母为全体注册用户；这不是有效学习留存。
- 严格漏斗：注册 → 注册日开始学习 → D1 打开 → D7 打开，逐级取交集。
- 学习活跃度：D0–D6 有开始学习或完成任务的不同日期数，不包含 D7。
- 召回率：流失标记后发生召回事件的用户 / 带流失标记用户；不代表活动效果。
- 痛点保留原始 5 类为证据口径，案例另说明与主上下文 6 类展示方式的映射。

## 使用边界

高顿教育市场内容运营属于主上下文记载的真实经历，与本独立项目分开展示。当前目录没有简历和实习证明原件，本阶段未重新核实实习数据，也未改写其成果归因。

简历可以写“基于 1000 名模拟用户、7306 条模拟日志，使用 Python 与 SQLite 完成指标核验、分群留存和行为关联分析，并设计待验证运营策略”。8 位样本应写为“模拟用户样本 / 模拟访谈”，不应写成实际招募并访谈了 8 位真实用户。

不得将模拟数据写成真实公司内部数据，不得把策略建议写成已上线功能，不得把组间留存差异写成真实提升。A/B 部分仅为实验设计，无已执行实验或实验结果。
