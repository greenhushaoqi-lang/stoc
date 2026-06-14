---
name: tauric-trading-agents
description: Use the TauricResearch TradingAgents and Trading-R1-inspired framework for stock, ETF, sector, or market research. Trigger when the user asks for TradingAgents/Tauric/Trading-R1-style analysis, multi-agent equity research, structured investment theses, facts-grounded reasoning, volatility-adjusted decision making, or wants fundamental, sentiment, news, and technical analyst views combined into a ranked research conclusion. Research support only; no trade execution.
---

# Tauric Trading Agents

Use this skill to structure public-market research with a TradingAgents-inspired analyst team and a Trading-R1-inspired reasoning discipline:

`fundamental analyst -> sentiment analyst -> news analyst -> technical analyst -> smart-money monitor -> structured thesis -> evidence grounding -> volatility-adjusted synthesis`

This is a reference workflow inspired by the public TauricResearch TradingAgents and Trading-R1 projects. Use public information only. Do not place trades, guarantee returns, or present the output as financial advice.

## Core Rule

Separate analyst evidence before giving the conclusion. Each analyst should make a concise, source-aware case, then the synthesis should reconcile disagreements and rank research priority.

When the user asks what to buy or what has upside, answer with ranked research priorities and conditions. The trading decision stays with the user.

Trading-R1 adds three required disciplines:

- **Structured thesis composition**: state the setup, evidence, variant view, and invalidation before the final rating.
- **Facts-grounded analysis**: separate confirmed facts, interpretation, and unverified leads.
- **Volatility-adjusted decision making**: downgrade ideas when expected upside is mainly compensation for high volatility, drawdown, crowding, liquidity, or gap risk.

## Workflow

1. **Set scope**
   - Identify ticker, market, sector, time horizon, and whether the user wants short-term catalysts, long-term thesis, or risk review.
   - Use live sources for current prices, filings, earnings, events, policy, market data, news, or "recent/current/latest" claims.
   - For US stocks or global AI/tech/chip names, read `references/smart-money-sources.md` and check political, congressional, ARK, and superinvestor tracking sources when relevant.

2. **Fundamental analyst**
   - Inspect revenue growth, margin trend, cash flow, balance sheet, customer concentration, backlog/orders, capex, dilution, and valuation.
   - Prefer filings, official announcements, exchange documents, investor presentations, and transcripts.
   - Output: `business quality / growth driver / valuation pressure / accounting or financing risk`.

3. **Sentiment analyst**
   - Inspect market attention, fund flows, analyst revisions, institutional positioning where available, social attention, and crowding.
   - Treat social media and unexplained price spikes as weak evidence unless confirmed by stronger sources.
   - Output: `attention level / crowding / sentiment inflection / weak-rumor flags`.

4. **News analyst**
   - Inspect recent company announcements, policy, industry events, product launches, tenders/orders, export controls, earnings calendar, and customer/supplier news.
   - Separate confirmed events from interpretation.
   - Output: `confirmed catalyst / possible catalyst / event date or window / evidence strength`.

5. **Technical analyst**
   - Inspect trend, relative strength, volume/turnover, support/resistance, volatility, drawdown, and whether price action confirms or contradicts the fundamental story.
   - Use technicals as timing and risk context, not as proof of business value.
   - Output: `trend state / momentum / volume confirmation / invalidation level or warning zone`.

6. **Cross-check**
   - Ask where the analysts disagree.
   - Downgrade the idea when fundamentals are weak but sentiment is hot, when news is unconfirmed, or when technicals show exhaustion after a large move.
   - Upgrade the idea when fundamentals, confirmed news, sentiment inflection, and technical confirmation point in the same direction.

7. **Smart-money monitor**
   - For US-listed stocks, check whether the ticker appears in recent political trades, congressional disclosures, ARK/13F activity, or superinvestor portfolios.
   - Treat these as signal sources, not standalone proof. Confirm with SEC filings, official disclosures, or the original disclosure when possible.
   - Separate `new disclosure`, `stale 13F position`, `popular copy-trade signal`, and `confirmed fundamental thesis`.
   - Use `references/smart-money-sources.md` for source-specific rules, cadence, and caveats.

8. **Trading-R1 reasoning pass**
   - Convert the four analyst views into a structured thesis:
     `setup -> evidence -> mechanism -> expected path -> risk-adjusted payoff -> invalidation`.
   - Score the idea on both return potential and risk burden. Consider volatility, maximum drawdown risk, downside skew, liquidity, event gap risk, and crowded positioning.
   - Run a short counterfactual check: "What would I believe if price action were ignored?" and "What would I believe if the recent news did not exist?"
   - Prefer a cautious rating when the thesis needs several unverified events to happen in sequence.

9. **Synthesis**
   - Give a ranked research conclusion.
   - Explain the strongest reason, the biggest risk, and what would change the view.
   - Use labels: `Strong`, `Medium`, `Weak`, or `Needs checking` for evidence quality.
   - Use the five-tier research scale when the user wants a decisive view:
     `Strong Positive`, `Positive`, `Neutral`, `Negative`, `Strong Negative`.
   - Never present the rating as a trade order.

## Trading-R1 Decision Discipline

Use this pass whenever the user asks for short-term upside, trading potential, event catalysts, or a decisive view.

1. **Thesis completeness**
   - Define the mechanism: why should the asset be repriced?
   - Define the time window: days, weeks, quarter, or 6-12 months.
   - Define the missing proof: what public evidence is still absent?

2. **Grounding check**
   - Mark each key claim as `confirmed fact`, `reasonable inference`, or `unverified lead`.
   - Do not let a thesis depend on one weak claim.
   - If data is unavailable, say exactly what needs checking.

3. **Risk-adjusted check**
   - Compare upside quality against volatility and drawdown risk.
   - Downgrade if the stock is already extended, liquidity is poor, the catalyst is widely known, or downside gaps are large.
   - Upgrade only when evidence strength, catalyst timing, and price/volume confirmation align.

4. **Decision label**
   - `Strong Positive`: multiple strong sources, clear repricing mechanism, favorable risk-adjusted setup, and defined invalidation.
   - `Positive`: good evidence and catalyst, but valuation, crowding, or timing is not ideal.
   - `Neutral`: mixed evidence, unclear timing, or balanced upside/downside.
   - `Negative`: weak evidence, poor risk-adjusted setup, deteriorating fundamentals, or exhausted technicals.
   - `Strong Negative`: thesis contradicted by strong evidence or downside risk dominates.

## Output Shape

For one company:

```text
Conclusion: [research priority and reason]

Fundamental analyst: ...
Sentiment analyst: ...
News analyst: ...
Technical analyst: ...
Smart-money monitor: ...

Trading-R1 reasoning:
- Setup:
- Evidence grounding:
- Risk-adjusted view:
- Counterfactual check:

Team synthesis:
- Bull case:
- Bear case:
- What would confirm it:
- What would invalidate it:
- Research priority:
```

For multiple companies:

```text
Rank | Company | Fundamental | Sentiment | News catalyst | Technical state | Smart-money signal | Risk-adjusted view | Research priority
```

Then add a short synthesis explaining why the top names ranked above the rest.

For short-term opportunities:

```text
Rank | Company | Catalyst | Smart-money signal | Evidence quality | Price/volume confirmation | Volatility/drawdown risk | Trading-R1 label | Why it ranks here
```

## Evidence Standards

- Strong: filings, official announcements, exchange documents, transcripts, regulatory/project records, contracts, or hard data.
- Medium: reputable financial media, industry media, specialist research with visible assumptions, company product pages, association data.
- Weak: social posts, forum claims, screenshots, unexplained volume spikes, or unattributed channel checks.
- Needs checking: important but not verified with available tools.

Do not build a high-conviction conclusion on weak evidence alone.

## Risk Boundary

Use direct but bounded language:

- "I would rank this higher as a research priority because..."
- "The idea weakens if..."
- "This is still only a lead because..."

Avoid:

- guaranteed return language;
- direct buy/sell orders;
- coordinated trading language;
- rumor-based recommendations;
- invented prices, customers, orders, or financial data.

## Chinese Style

For Chinese market prompts, answer in Chinese and keep the role labels clear:

```text
结论：

基本面分析师：
情绪分析师：
新闻分析师：
技术分析师：

Trading-R1 推理：
事实接地：
波动/回撤调整：

团队综合：
看多理由：
反方理由：
确认信号：
失效条件：
研究优先级：
```

If the user asks for A 股 short-term opportunities, explicitly separate `事件催化` from `基本面兑现`, add a `波动/回撤风险` line, and warn when the trade is mainly sentiment-driven.
