---
name: taoguba-market-radar
description: "Daily deep-learning and market-narrative radar for tracked Taoguba/TGB accounts and blogs. Use when the user asks to monitor, learn, update, summarize, or apply daily content from 淘股吧 users to A-share market analysis, hot themes, stocks, catalysts, sentiment, short-term narratives, sector rotation, or TradingAgents/Trading-R1-style reports."
---

# Taoguba Market Radar

Use this skill to maintain and apply a daily knowledge base for the tracked Taoguba account:

- `快乐糖糖`: `https://www.tgb.cn/blog/3485724`
- Mobile source: `https://m.tgb.cn/blog/3485724`

Local memory:

- Latest learned state: `references/latest.md`
- Raw daily archive: `references/daily/YYYY-MM-DD.jsonl`
- Source and compliance rules: `references/source-policy.md`

## Update Workflow

Run the updater before analysis when the user asks for the newest Taoguba view:

```powershell
python C:\Users\lixue\.codex\skills\taoguba-market-radar\scripts\update_taoguba_market_radar.py --skill-dir C:\Users\lixue\.codex\skills\taoguba-market-radar
```

The updater fetches the public mobile blog page, extracts recent article links and summaries, fetches each article page for full text when accessible, writes deduped raw records to `references/daily/`, and rebuilds `references/latest.md`.

If the site blocks access or changes HTML structure, keep the source-health section in `references/latest.md` and fall back to a user-provided JSON/JSONL export with `--import-json` or `--import-jsonl`.

## Analysis Workflow

When applying this skill to market research:

1. Read `references/latest.md`.
2. Separate Taoguba post evidence from inference.
3. Compare with other local X/Xueqiu/news radars:
   - `consensus themes`: repeated across multiple sources;
   - `isolated alpha`: a specific, checkable stock or catalyst from this account;
   - `market regime`: index, volume, risk appetite, liquidity, policy, or overseas mapping;
   - `noise`: emotional posts, unverified price targets, exaggerated profit claims, or copy-paste rumors.
4. Map themes to A-share stocks, supply-chain layers, event catalysts, price/volume confirmation, and invalidation signals.
5. Combine with market data, announcements, credible news, and existing finance skills before drawing conclusions.

## Output Style

For user-facing reports, provide:

- `Today learned`: latest themes from Taoguba.
- `Post deltas`: article titles, key stocks, and repeated concepts.
- `Consensus vs isolated signal`: repeated themes versus one-off ideas.
- `Market mapping`: stocks, sectors, overseas-A-share mapping, and supply-chain layer.
- `Catalyst watch`: events, filings, products, policy, earnings, price changes, or conference dates to verify.
- `Signal quality`: Strong / Medium / Weak / Needs source check.
- `What changed`: new themes versus prior daily summaries.

Do not repost long Taoguba articles. Summarize and cite local archive links or original URLs.
