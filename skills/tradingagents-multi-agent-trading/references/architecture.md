# TradingAgents Architecture Reference

Source pattern: TauricResearch/TradingAgents v0.2.5.

## Graph Flow

The framework is built as a LangGraph `StateGraph` over an `AgentState`.

Default analyst sequence:

1. Market Analyst
2. Sentiment Analyst, historically wired as `social`
3. News Analyst
4. Fundamentals Analyst
5. Bull Researcher
6. Bear Researcher
7. Research Manager
8. Trader
9. Aggressive Risk Analyst
10. Conservative Risk Analyst
11. Neutral Risk Analyst
12. Portfolio Manager

Analysts can call tools and then clear their message context before the next analyst. After the selected analysts finish, the graph enters bull/bear debate, then trading proposal, then risk debate, then final portfolio decision.

## Analyst Layer

Market Analyst:
- Uses stock data, indicators, and verified market snapshots.
- Selects up to eight complementary technical indicators.
- Must anchor exact OHLCV, price-level, and indicator claims in verified market snapshots when available.

Sentiment Analyst:
- Uses pre-fetched social/sentiment data instead of free-form invented social claims.
- Produces a sentiment band such as Bullish, Mildly Bullish, Neutral, Mixed, Mildly Bearish, or Bearish.
- Notes sample size, source coverage, and contrarian over-extension risk.

News Analyst:
- Uses ticker news and global/macro news.
- Distinguishes company-specific catalysts from background macro noise.
- Prioritizes recency, source credibility, and event impact.

Fundamentals Analyst:
- Uses company profile, fundamentals, balance sheet, cash flow, and income statement tools.
- Writes enough detail to inform the trader, but should not substitute stale fundamentals for current market data.

## Debate Layer

Bull Researcher:
- Advocates the investment case.
- Emphasizes growth, competitive advantages, positive indicators, and rebuttals to bearish points.

Bear Researcher:
- Argues against investment.
- Emphasizes risks, downside, market saturation, financial instability, macro threats, and rebuttals to bullish points.

Research Manager:
- Facilitates the debate.
- Produces a structured investment plan for the trader.
- Uses a five-tier recommendation scale where useful.

## Trading Layer

Trader:
- Converts the Research Manager plan into a concrete BUY / HOLD / SELL proposal.
- Should describe action, rationale, timing, sizing/risk notes, and key uncertainty.

## Risk And Portfolio Layer

Aggressive Risk Analyst:
- Champions upside and bold strategies.
- Challenges excessive caution and missed opportunity cost.

Conservative Risk Analyst:
- Protects capital.
- Challenges downside exposure, volatility, fragile assumptions, and high-risk execution.

Neutral Risk Analyst:
- Balances risk/reward.
- Challenges both optimistic and overly cautious interpretations.

Portfolio Manager:
- Synthesizes risk debate plus research and trader proposal.
- Produces the final portfolio decision and rating.

## State Hand-Offs

Important state fields:

- `company_of_interest`
- `trade_date`
- `market_report`
- `sentiment_report`
- `news_report`
- `fundamentals_report`
- `investment_debate_state`
- `investment_plan`
- `trader_investment_plan`
- `risk_debate_state`
- `final_trade_decision`

When adapting the framework manually, preserve these hand-offs even if the implementation is not LangGraph.
