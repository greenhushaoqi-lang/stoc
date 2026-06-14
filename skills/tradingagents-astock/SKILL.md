---
name: tradingagents-astock
description: Apply simonlin1212 TradingAgents-Astock, an A-share-specialized multi-agent investment research framework. Use for Chinese A股 analysis with 7 analysts: market, sentiment, news, fundamentals, policy, hot-money/龙虎榜, and lockup/unlock monitoring; bull/bear debate, risk debate, A股 T+1/涨跌停/手数/ST constraints, and Chinese research reports.
---

# TradingAgents Astock

Use this skill as a local Codex wrapper for simonlin1212/TradingAgents-astock. It adapts the TradingAgents multi-agent research flow to A-shares.

Research only. Do not issue direct trading orders.

## Analyst Team

Use seven A-share analysts:

1. **市场分析师**: K线、技术指标、量价、换手、趋势。
2. **舆情分析师**: 社交媒体、散户讨论、热度、情绪扩散。
3. **新闻分析师**: 行业新闻、公司公告、宏观事件、海外映射。
4. **基本面分析师**: 财报三表、盈利能力、估值、现金流。
5. **政策分析师**: 监管政策、产业政策、窗口指导、补贴、出口管制。
6. **游资追踪师**: 龙虎榜、大单流向、主力资金、短线资金偏好。
7. **解禁监控师**: 限售股解禁、减持、质押、供给冲击。

## Workflow

1. **A股路由**
   - Identify stock code, exchange, sector, concept, and time window.
   - Use live sources for current market data, announcements, news, 龙虎榜, 解禁, and policy.
   - Respect A-share constraints: T+1, daily price limits, lots, ST risk, trading hours, and liquidity.

2. **Seven reports**
   - Produce a concise view from each analyst.
   - Mark evidence as `Strong`, `Medium`, `Weak`, or `Needs checking`.

3. **Bull/Bear debate**
   - Bull researcher: why the stock can be repriced.
   - Bear researcher: why the idea can fail or already be priced in.
   - Force both sides to name invalidation conditions.

4. **Risk debate**
   - Aggressive view: short-term upside and catalyst path.
   - Conservative view: valuation, crowding, event, liquidity, and downside risk.
   - Neutral view: what evidence is missing.

5. **Final synthesis**
   - Give research priority, not a buy/sell command.
   - Separate `事件催化`, `基本面兑现`, `资金/情绪`, `政策/游资/解禁`, and `失效条件`.

## Output Template

```text
结论：

市场分析师：
舆情分析师：
新闻分析师：
基本面分析师：
政策分析师：
游资追踪师：
解禁监控师：

多空辩论：
风险辩论：

事件催化：
基本面兑现：
资金/情绪：
政策/游资/解禁：
失效条件：
研究优先级：
```

## Source

Reference project: https://github.com/simonlin1212/TradingAgents-astock
