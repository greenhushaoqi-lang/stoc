# TradingAgents Agent Playbook

Use this file when manually simulating or adapting TradingAgents without running the package.

## Market Analyst

Goal: Produce a technical and market-structure report.

Inputs: ticker, date, benchmark, OHLCV, verified snapshot, indicators.

Output:
- trend and regime
- volume and volatility
- up to eight non-redundant indicators
- support/resistance only when backed by data
- tactical implications and data caveats

## Sentiment Analyst

Goal: Produce a grounded sentiment report.

Inputs: social messages, source labels, StockTwits bullish/bearish ratio, Reddit/X/other sources if available.

Output:
- sentiment band
- confidence and sample size
- strongest positive and negative narratives
- crowding/contrarian risk
- source limitations

## News Analyst

Goal: Separate tradable catalysts from background noise.

Inputs: company news, global/macro news, source dates, event tags.

Output:
- top catalysts
- likely impact direction
- recency and source quality
- macro spillovers
- what remains unverified

## Fundamentals Analyst

Goal: Describe valuation-relevant fundamentals.

Inputs: profile, financial statements, cash flow, balance sheet, income statement, filings if available.

Output:
- business and revenue drivers
- margins, cash flow, leverage, liquidity
- growth/quality risks
- financial statement red flags
- table of key metrics

## Bull Researcher

Goal: Argue the strongest investment case.

Output:
- growth and upside thesis
- competitive advantages
- positive data support
- rebuttal to bear concerns
- assumptions required for success

## Bear Researcher

Goal: Argue the strongest downside case.

Output:
- downside thesis
- valuation, execution, financial, macro, and competitive risks
- rebuttal to bull assumptions
- conditions that make the asset unattractive

## Research Manager

Goal: Convert debate into an investment plan.

Output:
- recommendation
- decisive evidence
- unresolved debate points
- base case and alternative cases
- thesis breakers
- research plan for trader

## Trader

Goal: Convert research plan into BUY / HOLD / SELL.

Output:
- transaction action
- timing and execution logic
- sizing/risk guidance when available
- invalidation level or condition
- data gaps that prevent confident execution

## Aggressive Risk Analyst

Goal: Stress opportunity cost and upside.

Output:
- why taking risk may be justified
- upside asymmetry
- objections to cautious views
- execution improvements that preserve upside

## Conservative Risk Analyst

Goal: Protect capital.

Output:
- downside exposure
- fragility of assumptions
- liquidity, volatility, drawdown, and concentration risk
- safer alternatives or reduced exposure

## Neutral Risk Analyst

Goal: Balance both sides.

Output:
- integrated risk/reward
- what both aggressive and conservative views miss
- scenario conditions
- practical middle path

## Portfolio Manager

Goal: Final decision.

Output:
- five-tier portfolio rating
- final action
- confidence
- risk controls
- upgrade/downgrade conditions
- monitoring dashboard
