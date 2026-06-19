---
name: xueqiu-market-radar
description: "Daily deep-learning and market-narrative radar for tracked Xueqiu accounts. Use when the user asks to monitor, learn, update, summarize, or apply daily content from Xueqiu users to A-share/HK/US market analysis, sector themes, catalysts, sentiment, stocks, fund flows, research notes, or TradingAgents/Trading-R1-style reports. Supports Xueqiu cookie/API collection, RSSHub fallback, and user-provided JSON/JSONL exports."
---

# Xueqiu Market Radar

Use this skill to maintain and apply a daily knowledge base for the tracked Xueqiu accounts:

- `5124430882`: `https://xueqiu.com/u/5124430882`
- `5672579962`: `https://xueqiu.com/u/5672579962`
- `1034624503`: `https://xueqiu.com/u/1034624503`
- `4086512744`: `https://xueqiu.com/u/4086512744`
- `7251377368`: `https://xueqiu.com/u/7251377368`
- `1301600236`: `https://xueqiu.com/u/1301600236`
- `4168622038`: `https://xueqiu.com/u/4168622038`

The user mentioned 12 accounts, but only 7 URLs are currently configured. Add new account IDs to `scripts/update_xueqiu_market_radar.py` when more URLs are provided.

Local memory:

- Latest learned state: `references/latest.md`
- Raw daily archive: `references/daily/YYYY-MM-DD.jsonl`
- Source and compliance rules: `references/source-policy.md`

## Update Workflow

Run the updater before analysis when the user asks for the newest Xueqiu view:

```powershell
python C:\Users\lixue\.codex\skills\xueqiu-market-radar\scripts\update_xueqiu_market_radar.py --skill-dir C:\Users\lixue\.codex\skills\xueqiu-market-radar
```

The updater tries:

1. Xueqiu public timeline APIs using `XUEQIU_COOKIE` or `XQ_A_TOKEN` when available.
2. RSSHub Xueqiu routes as fallback.
3. User-provided local JSON/JSONL exports through `--import-json` or `--import-jsonl`.

Xueqiu often blocks unauthenticated requests with WAF. If collection fails, keep the source-health section in `references/latest.md` and ask for a readable export or a valid `XUEQIU_COOKIE`.

## Analysis Workflow

When applying this skill to market research:

1. Read `references/latest.md`.
2. Separate Xueqiu post evidence from inference.
3. Compare accounts:
   - `consensus themes`: repeated across 2+ accounts;
   - `isolated alpha`: one account posts a specific, checkable clue;
   - `market regime`: index, volume, risk appetite, liquidity, policy, or overseas mapping;
   - `noise`: emotional posts, unverified price targets, vague slogans, or copy-paste rumors.
4. Map themes to A-share/HK/US/Japan/Korea tickers, supply-chain layers, event catalysts, price/volume confirmation, and invalidation signals.
5. Combine with market-data, announcements, news, and existing X radar skills before drawing conclusions.

## Output Style

For user-facing reports, provide:

- `Today learned`: latest themes from Xueqiu.
- `Account deltas`: what each account emphasized.
- `Consensus vs isolated signal`: repeated themes versus one-off ideas.
- `Market mapping`: stocks, sectors, overseas-A-share mapping, and supply-chain layer.
- `Catalyst watch`: events, filings, products, policy, earnings, price changes, or conference dates to verify.
- `Signal quality`: Strong / Medium / Weak / Needs source check.
- `What changed`: new themes versus prior daily summaries.

Do not repost long Xueqiu content. Summarize and cite local archive links or original post URLs.
