---
name: fincept-terminal
description: Apply the FinceptTerminal-style financial terminal workflow for market analytics, investment research, economic data, portfolio/risk analytics, AI agents, data connectors, and quant-lab style idea generation. Use when the user wants Bloomberg-like research organization, multi-asset analytics, financial terminal workflows, or integrated market/news/macro/portfolio analysis.
---

# Fincept Terminal

Use this skill as a research workflow inspired by FinceptTerminal: organize market research like a terminal, combining data, analytics, agents, portfolio tools, news, and macro context in one structured view.

Do not imply access to proprietary terminal data unless the user provides it. Use public data and clearly mark missing fields.

## Workflow

1. **Workspace**
   - Define asset class: equity, fixed income, crypto, commodity, FX, portfolio, or macro.
   - Define views needed: quote, fundamentals, news, macro, valuation, portfolio, risk, scenario, or factor.

2. **Data connector mindset**
   - Pull current public sources where available.
   - Prefer filings, exchange data, central-bank/statistical databases, reputable financial media, and company materials.
   - Mark unavailable data rather than inventing terminal-like fields.

3. **Terminal panels**
   - Market panel: price, trend, volume, relative strength.
   - Fundamental panel: revenue, margin, cash flow, balance sheet, valuation.
   - News panel: company events, macro, policy, sector catalysts.
   - Risk panel: VaR-like downside, volatility, liquidity, drawdown, event gaps.
   - Portfolio panel: exposure, concentration, correlation, factor/cycle risk.
   - Agent panel: Buffett/Graham/Lynch/Munger-style long-term lens when relevant; trader lens for shorter windows.

4. **Synthesis**
   - Return a compact terminal-style research brief.
   - Separate data, interpretation, and missing checks.
   - Give next actions for verification.

## Output Template

```text
Terminal brief:

Market:
Fundamentals:
News/Macro:
Valuation:
Risk:
Portfolio impact:
Agent views:
Missing data:
Research conclusion:
```

## Source

Reference project: https://github.com/Fincept-Corporation/FinceptTerminal
