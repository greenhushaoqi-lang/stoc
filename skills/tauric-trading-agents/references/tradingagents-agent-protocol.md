# TradingAgents Agent Protocol

This file condenses the TauricResearch `TradingAgents` source into a local Codex research protocol.

## Agent Order

1. **Market analyst**
   - Source role: `agents/analysts/market_analyst.py`
   - Inputs: stock data, technical indicators, verified market snapshot.
   - Output: trend, momentum, indicator fit, exact price/volume caveats, warning zones.
   - Local rule: do not invent exact OHLCV or support/resistance levels; verify with market-data skills.

2. **Sentiment analyst**
   - Source role: `agents/analysts/sentiment_analyst.py`
   - Inputs: news headlines, StockTwits-style retail messages, Reddit-style discussions.
   - Output: sentiment band, score, confidence, narrative, divergences, catalysts and risks.
   - Local rule: social/X/Xueqiu/Taoguba posts are weak signals until confirmed by price, filings, or credible news.

3. **News analyst**
   - Source role: `agents/analysts/news_analyst.py`
   - Inputs: company/asset news, global news, macro indicators, prediction-market probabilities.
   - Output: confirmed catalysts, macro/sector impact, evidence table.
   - Local rule: separate confirmed event, reasonable inference, and unverified lead.

4. **Fundamentals analyst**
   - Source role: `agents/analysts/fundamentals_analyst.py`
   - Inputs: fundamentals, balance sheet, cash flow, income statement.
   - Output: business quality, financial trend, valuation pressure, accounting and financing risk.
   - Local rule: for A-shares, use official filings, exchange announcements, annual/interim reports, and local financial data skills where available.

5. **Bull researcher**
   - Source role: `agents/researchers/bull_researcher.py`
   - Task: argue growth potential, competitive advantage, positive indicators, and refute bear concerns with evidence.

6. **Bear researcher**
   - Source role: `agents/researchers/bear_researcher.py`
   - Task: argue risks, competitive weakness, negative indicators, downside skew, and refute bull claims with evidence.

7. **Research manager**
   - Source role: `agents/managers/research_manager.py`
   - Task: reconcile the bull/bear debate into `Buy / Overweight / Hold / Underweight / Sell`.
   - Local mapping: convert this into research priority and scenario weighting, not a direct trade command.

8. **Trader**
   - Source role: `agents/trader/trader.py`
   - Task: convert the research plan into `Buy / Hold / Sell`, reasoning, optional entry, stop-loss, sizing.
   - Local mapping: present as hypothetical execution context only. Avoid deterministic buy/sell instructions.

9. **Risk debate**
   - Source roles:
     - `risk_mgmt/aggressive_debator.py`
     - `risk_mgmt/neutral_debator.py`
     - `risk_mgmt/conservative_debator.py`
   - Task: stress test upside pursuit, balanced risk/reward, and capital protection.
   - Local rule: downgrade crowded, extended, low-liquidity, rumor-heavy, or gap-risk setups.

10. **Portfolio manager**
    - Source role: `agents/managers/portfolio_manager.py`
    - Task: synthesize risk debate into `Buy / Overweight / Hold / Underweight / Sell`, thesis, target/time horizon if supported.
    - Local mapping: provide `Strong Positive / Positive / Neutral / Negative / Strong Negative` only as research labels.

11. **Trading-R1 pass**
    - Source status: public `Trading-R1` repo has no terminal code at snapshot.
    - Task: add thesis completeness, evidence grounding, counterfactual checks, and volatility-adjusted ranking.

## Output Contract For A-Share Short-Term Reports

Use this compact structure:

```text
结论：

确认事实：
合理推断：
X/雪球/淘股吧/研报弱信号：

市场分析师：
情绪分析师：
新闻分析师：
基本面分析师：

多空辩论：
- 看多理由：
- 反方理由：

风险辩论：
- 激进视角：
- 中性视角：
- 保守视角：

Trading-R1：
- 设定：
- 证据接地：
- 机制：
- 缺失证据：
- 失效条件：
- 波动/回撤调整：
- 标签：
```

For ranked lists, use:

```text
排名 | 股票 | 板块 | 催化 | 确认事实 | 弱信号 | 盘面确认 | 海外映射 | 风险 | Trading-R1标签
```

## Rating Translation

- `Buy` -> `Strong Positive` only when evidence is strong, catalyst is timely, and risk burden is acceptable.
- `Overweight` -> `Positive`.
- `Hold` -> `Neutral`.
- `Underweight` -> `Negative`.
- `Sell` -> `Strong Negative`.

If the thesis relies mainly on social posts or screenshots, cap the label at `Neutral` or `Positive` unless market/filing/news confirmation is also present.
