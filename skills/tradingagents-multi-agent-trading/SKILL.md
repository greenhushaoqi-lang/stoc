---
name: tradingagents-multi-agent-trading
description: Use the TauricResearch TradingAgents framework pattern for multi-agent stock or asset trading research: market, sentiment/news, fundamentals, bull/bear debate, trader proposal, risk debate, and portfolio decision. Use when the user asks for TradingAgents-style analysis, multi-agent trading decisions, buy/hold/sell workflows, or installing/running TradingAgents.
---

# TradingAgents Multi-Agent Trading

Use this skill for TradingAgents-style market research and trading decision workflows. It adapts the TauricResearch TradingAgents architecture into Codex-friendly instructions while preserving the original framework's staged analyst, debate, trader, risk, and portfolio-manager flow.

Treat outputs as research analysis, not personalized investment advice. For current market data, prices, news, filings, model availability, package versions, and regulations, verify from current sources before making claims.

## When To Use

- The user asks to run, install, explain, or adapt TauricResearch TradingAgents.
- The user wants a multi-agent stock/asset decision process rather than a single analyst note.
- The user asks for buy/hold/sell, portfolio rating, risk debate, technical + fundamental + news synthesis, or a TradingAgents-style report.

## Core Workflow

1. Define the asset, market, date, horizon, language, benchmark, and data vendors.
2. Run analyst reports:
   - Market Analyst: price action, OHLCV, technical indicators, trend, volatility, support/resistance, benchmark context.
   - Sentiment Analyst: StockTwits/Reddit/social messages when available, source quality, bullish/bearish balance, contrarian risk.
   - News Analyst: ticker news plus global/macro news, event relevance, recency, catalysts, and data-source limitations.
   - Fundamentals Analyst: profile, financial statements, cash flow, balance sheet, valuation-relevant fundamentals.
3. Run the investment debate:
   - Bull Researcher argues the positive case from the analyst reports.
   - Bear Researcher argues the downside case and challenges optimistic assumptions.
   - Research Manager synthesizes the debate into a structured investment plan.
4. Run the transaction layer:
   - Trader converts the research plan into BUY / HOLD / SELL with sizing, timing, and execution notes when possible.
5. Run the risk debate:
   - Aggressive Risk Analyst argues for high-upside/high-risk opportunities.
   - Conservative Risk Analyst protects capital and challenges downside exposure.
   - Neutral Risk Analyst balances both sides and stress-tests assumptions.
   - Portfolio Manager produces the final portfolio decision and rating.
6. End with an audit trail: sources, unverifiable data, conflict checks, thesis breakers, and monitoring metrics.

## Output Discipline

- Separate facts, tool output, market consensus, and agent inference.
- Do not invent exact prices, indicators, filings, social sentiment, or news counts.
- If a tool/source conflicts with another, flag the discrepancy and prefer verified primary or market-data snapshots.
- Use a five-tier portfolio rating when appropriate: Strong Buy / Buy / Hold / Sell / Strong Sell.
- Keep the final decision connected to both upside and downside cases.

## References

Read these only when needed:

- `references/architecture.md`: graph flow, roles, state, and decision hand-offs.
- `references/install-run.md`: install commands, environment variables, CLI/API usage, and vendor configuration.
- `references/agent-playbook.md`: compact role prompts and expected outputs for each agent.

## Local Execution Pattern

If the user wants the real package executed, first read `references/install-run.md`, then verify dependencies and API keys. Typical commands:

```powershell
python -m pip install "git+https://github.com/TauricResearch/TradingAgents.git"
tradingagents
```

For programmatic use, prefer importing `TradingAgentsGraph` from the installed package and using explicit config rather than relying on hidden defaults.

## Report Template

```markdown
# TradingAgents Decision: [Ticker / Asset]

## 0. Final Decision
- Portfolio Rating:
- Trader Action:
- Confidence:
- Horizon:
- Key Reason:
- Thesis Breaker:

## 1. Analyst Reports
### Market Analyst
### Sentiment Analyst
### News Analyst
### Fundamentals Analyst

## 2. Bull / Bear Debate
### Bull Case
### Bear Case
### Research Manager Synthesis

## 3. Trader Proposal
- Action:
- Entry / Exit Logic:
- Position / Risk Notes:
- Data Gaps:

## 4. Risk Debate
### Aggressive Risk View
### Conservative Risk View
### Neutral Risk View

## 5. Portfolio Manager Decision
- Rating:
- Rationale:
- Conditions To Upgrade / Downgrade:

## 6. Source And Data Audit
- Sources:
- Unverified Data:
- Conflicts:
- Monitoring Dashboard:
```
