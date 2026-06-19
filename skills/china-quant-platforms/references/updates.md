# 平台每日更新日志 (Daily Updates)

由定时任务 `daily-quant-sites-learn` 每日抓取 joinquant.com / guorn.com / thinktrader.net(及 dict.thinktrader.net) 的公开更新（文档、公告、产品、社区精华），按日期追加。最新条目在最上方。回答前先看最新日期是否够新。

---

## 2026-06-17

### 聚宽 JoinQuant
- 无公开可见的2026年6月新公告或功能更新。
- jqdatasdk 在 PyPI 上最新版本仍为 **1.9.8**（2026-01-29 发布），pip install -U jqdatasdk 可获取。来源：[jqdatasdk · PyPI](https://pypi.org/project/jqdatasdk/)
- GitHub 官方仓库（[JoinQuant/jqdatasdk](https://github.com/JoinQuant/jqdatasdk)）暂无 Releases 页面发布记录，建议以 PyPI 版本为准。
- 未取到：社区公告页需登录，JS渲染页面内容为空。

### 果仁网 Guorn
- 无公开可见的2026年6月新公告或功能更新。
- 提示：搜索结果中有**策略导出权限**政策说明（属2025年变化，非新变化）：VIP绑定1个券商账户，VIP+ 可绑定5个账户（含通过果仁二维码开户方式），自2025年10月1日起对全部账户生效。来源：[果仁策略导出权限说明](https://guorn.com/forum/post/p.1233980.335463689800847)
- 未取到：首页为静态营销内容，无日期标记；FAQ页无更新公告。

### 迅投 ThinkTrader / QMT
- 无公开可见的2026年6月新版本发布。
- xtquant 官方知识库最新版本仍为 **xtquant_250807**（2025-12-19 发布），主要更新：token模式K线全推调整、智能算法交易支持、当前认购信息查询接口、期货夜盘bug修复。来源：[xtquant版本下载 | 迅投知识库](https://dict.thinktrader.net/nativeApi/download_xtquant.html)
- 社区中发现第三方工具：**XTQuant AI MCP服务器**（非官方），可将xtquant接口集成到AI助手直连操作，参见 [mcp.aibase.cn](https://mcp.aibase.cn/server/1916334490086436865)（仅作参考，需自行评估可靠性）。
- 未取到：知识库文档页面JS渲染，无法直接抓取版本日志详情，以知识库下载页为准。

---

## 2026-06-16 (初始化)
技能创建。三平台基线认知见 SKILL.md 与 references/{joinquant,guorn,thinktrader-qmt}.md。
- 聚宽 JoinQuant：在线研究/回测 + jqdatasdk(JQData) 数据SDK。
- 果仁网 Guorn：网页向导式因子选股/秒级回测/策略广场跟单，零代码。
- 迅投 ThinkTrader/QMT：QMT/miniQMT + xtquant(xtdata/xttrader) 实盘自动交易，覆盖股/期/期权/ETF/债。
> 注：三站深度内容多在登录后，公开可抓取的为文档/公告/产品介绍；后续每日条目仅记录公开可见的变化。

<!-- 新条目插入到这一行下方 -->
