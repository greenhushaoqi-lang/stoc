---
name: tradingagents-framework
description: Apply the TauricResearch TradingAgents multi-agent financial research framework. Use when the user asks for TradingAgents-style stock analysis, analyst-team debates, fundamental/sentiment/news/technical analyst workflows, trader/risk/portfolio-manager synthesis, or research-only trading decision support across US, HK, A-share, crypto, or global tickers.
---

# TradingAgents Framework

Use this skill as a research wrapper for TauricResearch/TradingAgents. The framework decomposes stock analysis into specialized LLM agents: fundamental analyst, sentiment analyst, news analyst, technical analyst, bullish/bearish researchers, trader, risk manager, and portfolio manager.

This is research support only. Do not place trades, guarantee returns, or present outputs as financial advice.

## Workflow

1. **Scope**
   - Identify ticker, market suffix, date window, benchmark, and whether the user wants short-term trading or longer-term research.
   - Use live data for current prices, filings, news, and events.

2. **Analyst team**
   - Fundamental analyst: financials, growth, margins, cash flow, valuation, red flags.
   - Sentiment analyst: social chatter, market mood, fund flows, attention, crowding.
   - News analyst: company news, macro, policy, industry events, earnings calendar.
   - Technical analyst: trend, momentum, volume, support/resistance, volatility.

3. **Research debate**
   - Write a bull researcher view and a bear researcher view.
   - Force both sides to cite evidence and state what would prove them wrong.

4. **Trader synthesis**
   - Convert the analyst and debate outputs into a research action label:
     `Strong Positive`, `Positive`, `Neutral`, `Negative`, or `Strong Negative`.
   - Include catalyst timing, confidence, and invalidation.

5. **Risk and portfolio check**
   - Assess volatility, liquidity, drawdown risk, event gap risk, concentration, and whether the thesis is already crowded.
   - Downgrade when the thesis relies on weak sentiment or stale news.

## Output Template

```text
Conclusion:

Fundamental analyst:
Sentiment analyst:
News analyst:
Technical analyst:

Bull researcher:
Bear researcher:

Trader synthesis:
Risk manager:
Portfolio manager:

Research label:
Confirming evidence:
Invalidation:
```

## Source

Reference project: https://github.com/TauricResearch/TradingAgents
