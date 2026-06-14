---
name: tradingagents-cn
description: Apply the TradingAgents-CN Chinese enhanced multi-agent stock research framework. Use for Chinese-language A-share, HK-share, or US-share analysis with localized data-source thinking, A股/港股/美股 support, Chinese reports, AkShare/Tushare/BaoStock-style fallback awareness, model/provider configuration awareness, and learning/research-only multi-agent financial analysis.
---

# TradingAgents-CN

Use this skill as a Chinese-market wrapper inspired by hsliuping/TradingAgents-CN. It adapts the TradingAgents multi-agent framework for Chinese users, Chinese reports, and A-share/HK/US analysis.

Research and learning only. Do not produce direct trading orders.

## Workflow

1. **Market routing**
   - A-share: use stock code, exchange, latest announcements, annual/quarterly reports, interactive Q&A, policy, industry chain, and Chinese financial media.
   - HK-share: use HKEX disclosures, southbound flow, mainland exposure, liquidity, and connected transactions.
   - US-share: use SEC filings, earnings, investor presentations, and global macro/sector catalysts.

2. **Data fallback mindset**
   - Prefer primary sources.
   - When public feeds disagree, cross-check with exchange filings and company announcements.
   - Treat AkShare/Tushare/BaoStock-like data as useful feeds but not final proof for high-conviction claims.

3. **Chinese multi-agent team**
   - 基本面分析师：财务、成长、现金流、估值、商业模式。
   - 情绪分析师：热度、资金、社媒、龙虎榜/北向/南向等可用线索。
   - 新闻分析师：公告、政策、产业新闻、订单、财报、监管事件。
   - 技术分析师：趋势、量价、支撑压力、波动、回撤。
   - 风控经理：估值拥挤、流动性、业绩雷、政策和事件风险。

4. **Report**
   - Produce a Chinese research note with evidence grading.
   - Separate `事件催化`, `基本面兑现`, `资金/情绪`, and `失效条件`.

## Output Template

```text
结论：

基本面分析师：
情绪分析师：
新闻分析师：
技术分析师：
风控经理：

事件催化：
基本面兑现：
预期差：
失效条件：
研究优先级：
```

## Source

Reference project: https://github.com/hsliuping/TradingAgents-CN
