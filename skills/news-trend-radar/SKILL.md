---
name: news-trend-radar
description: Use live Buzzing, NewsNow, and 今日热榜/TopHub sources to scan global and Chinese news, tech, finance, science, developer, product, policy, and market narratives. Trigger when the user asks for trending topics, narrative discovery, market catalysts, stock/crypto/theme monitoring, overseas/domestic news mapping, Hacker News/Product Hunt/Reuters/Bloomberg/FT/WSJ/BBC/TopHub/NewsNow scans, or real-time public-opinion/news radar research.
---

# News Trend Radar

Use this skill to turn live news and trend aggregators into a research radar. It covers:

- **Buzzing**: overseas tech, finance, science, developer, media, China-topic, and global-news feeds.
- **NewsNow**: domestic Chinese real-time news and social hot-topic aggregation.
- **今日热榜 / TopHub**: Chinese internet hot lists, especially technology, finance, social, and platform trends.

Read `references/source-map.md` before using this skill on a live scan.

## Core Rule

Always fetch or search live sources for current claims. Do not rely on static memories of what is trending.

Separate:

- `confirmed news`: reported by a credible source or multiple aggregators;
- `trend signal`: repeatedly appearing across aggregators, but not yet proven important;
- `market catalyst`: likely to affect stocks, sectors, commodities, crypto, rates, or policy expectations;
- `noise`: high heat but weak investment or research relevance.

## Workflow

1. **Set scope**
   - Region: overseas, China, or cross-market.
   - Domain: tech, AI, semiconductors, finance, macro, geopolitics, science, product/startup, developer, consumer, crypto, or all.
   - Time window: default to today and the last 24 hours; use last 7 or 30 days when the user asks for trend evolution.

2. **Load sources**
   - Read `references/source-map.md`.
   - Prioritize 5-12 sources that match the user request.
   - Use RSS/JSON endpoints when available; otherwise browse/search the listed site pages.

3. **Normalize stories**
   - Deduplicate by topic, company, ticker, country, technology, and event.
   - Group near-duplicates across Reuters/Bloomberg/FT/WSJ/BBC/Google News/TopHub/NewsNow.
   - Record the first source, repeated sources, and newest source.

4. **Score narrative heat**
   - Frequency: how many sources mention it?
   - Freshness: how recent is it?
   - Credibility: primary/source quality versus aggregator-only heat.
   - Market linkage: which stocks, sectors, commodities, policies, or crypto assets can be affected?
   - Novelty: is this old consensus or a new narrative?

5. **Map to opportunities and risks**
   - For stock research, map news to supply-chain layers, revenue exposure, cost exposure, sentiment, and event timing.
   - For crypto or internet narratives, map to attention velocity, community overlap, exchange/listing risk, and reflexivity.
   - For macro/policy, map to rates, FX, commodities, tariffs, sanctions, subsidies, and sector rotation.

6. **Output**
   - Give a ranked radar, not a raw link dump.
   - Cite source URLs used.
   - Mark evidence strength: `Strong`, `Medium`, `Weak`, or `Needs checking`.
   - State what would invalidate the narrative.

## Output Template

```text
新闻/叙事雷达：

1. [主题]
- 热度：
- 主要来源：
- 新鲜度：
- 市场映射：
- 相关股票/行业/资产：
- 证据强度：
- 反方理由：
- 下一步验证：

Top signals:
Noise to ignore:
Watch next:
```

## Safety

- Do not republish paywalled article text; summarize briefly and cite the link.
- Treat aggregators as discovery tools. Confirm important claims with original reporting, filings, official announcements, or primary data.
- For investment tasks, provide research priorities and catalysts, not direct buy/sell instructions.
