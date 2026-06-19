# tools — A股预期差量化工具（零依赖,urllib）

本地量化脚本,配合 skills 使用。数据源全部免费免key:腾讯行情(qt.gtimg.cn,不封IP)、东财(reportapi/push2his/datacenter-web)。

## 核心模块
- **expectation_gap_monitor.py** — 预期差引擎。函数:`fetch_quotes`(腾讯实时行情)、`fetch_consensus`(东财机构一致预期EPS/目标价)、`fetch_financials`(营收/净利同比)、`fetch_flow`(主力净流入)、`score`(融合PEG/预测增速/目标价空间/营收净利同比/资金确认/透支惩罚的量化预期差分,无机构覆盖用实际财报增速兜底)、`resolve_code`(名称→代码,带缓存)、`confidence`。
- **astock_confirm.py** — 资金确认层(复刻 a-stock-data 东财datacenter逻辑):`dragon`(龙虎榜近30日上榜+机构席位净额)、`lockup`(未来90天解禁)、`flow5`(主力5日净流入)、`confirm`。
- **run_integrated.py** — 整合扫描 = 量化预期差 × 龙虎榜机构席位 × 解禁,一条命令出排序表+资金确认标记(机构买✅/卖⚠️)。
  - `python run_integrated.py 厦门钨业 奕东电子 ...` 或无参用内置名单 → `reports/integrated_YYYYMMDD.txt`
- **update_skills.py** — 从本仓库同步 skills 到 ~/.claude/skills(含自愈补 frontmatter)。

## 板块扫描范式(run_*.py)
对某板块候选股批量打分排序的示例:run_big(综合大池)、run_passive(被动元件)、run_power_semi(功率半导体)、run_cpo(CPO/光引擎)、run_gas(六氟化钨/电子特气)、run_mix / run_k16 / run_user16(自定义篮子)。复制改 WATCHLIST 即可。

## 打分逻辑(预期差分)
低PEG(便宜vs成长)+ 真实净利/营收同比 + 目标价空间 + 资金确认(量比) − 透支惩罚(涨停/PE极端/已过目标价)。无机构覆盖标的仅靠财报增速兜底,标"无覆盖/低置信"。极端同比(低基数/扭亏)已封顶。

> ⚠️ 公开数据仅供研究,不构成投资建议。机构席位净仅反映"机构专用席位"动向。
