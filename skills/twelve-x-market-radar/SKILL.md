---
name: twelve-x-market-radar
description: "Daily deep-learning and market-narrative radar for twelve X accounts: @ariston_macro, @hoyooyoo, @off_thetarget, @lixon236, @xiaoyeyeeey, @ueutrt, @xzzzjpl, @twikejin, @techflowpost, @chaoxiangooo, @dacefupan, and @andrew_fdwt. Use when the user asks to monitor these X accounts, learn daily updates, summarize market themes, compare account views, or map their posts to A-share/HK/US/Japan/Korea stocks, sectors, catalysts, AI, semiconductor, macro, crypto, commodities, or sentiment analysis."
---

# Twelve X Market Radar

Use this skill to maintain and apply a daily knowledge base for twelve tracked X accounts:

- `ariston_macro`: `https://x.com/ariston_macro?s=21`
- `hoyooyoo`: `https://x.com/hoyooyoo?s=21`
- `off_thetarget`: `https://x.com/off_thetarget?s=21`
- `lixon236`: `https://x.com/lixon236?s=21`
- `xiaoyeyeeey`: `https://x.com/xiaoyeyeeey?s=21`
- `ueutrt`: `https://x.com/ueutrt?s=21`
- `xzzzjpl`: `https://x.com/xzzzjpl?s=21`
- `twikejin`: `https://x.com/twikejin?s=21`
- `techflowpost`: `https://x.com/techflowpost?s=21`
- `chaoxiangooo`: `https://x.com/chaoxiangooo?s=21`
- `dacefupan`: `https://x.com/dacefupan?s=21`
- `andrew_fdwt`: `https://x.com/andrew_fdwt?s=21`

Local memory:

- Latest learned state: `references/latest.md`
- Raw daily archive: `references/daily/YYYY-MM-DD.jsonl`
- Source and compliance rules: `references/source-policy.md`

## Update Workflow

Run the updater before analysis when the user asks for the newest view:

```powershell
python C:\Users\lixue\.codex\skills\twelve-x-market-radar\scripts\update_twelve_x_market_radar.py --skill-dir C:\Users\lixue\.codex\skills\twelve-x-market-radar
```

The updater tries official X API if `X_BEARER_TOKEN` or `TWITTER_BEARER_TOKEN` exists, falls back to public RSS/Nitter-style frontends account by account, writes deduped raw posts to `references/daily/`, and rebuilds `references/latest.md`.

If all sources fail, ask the user for an official API bearer token, a readable JSON/JSONL export, or permission to use a logged-in browser session if available.

## Deep-Learning Workflow

When applying these accounts to market research:

1. Read `references/latest.md`.
2. Separate direct post evidence from inference.
3. Compare accounts:
   - `consensus themes`: repeated across 2+ accounts;
   - `isolated alpha`: one account posts a specific, checkable clue;
   - `market regime`: macro/risk-on/risk-off, liquidity, index-level, overseas-market mapping;
   - `noisy repetition`: vague hot-topic reposting without new evidence.
4. Map themes to A-share/HK/US/Japan/Korea tickers, supply-chain layers, event catalysts, price/volume confirmation, and invalidation signals.
5. Combine with existing finance and news skills for verification before drawing investment conclusions.

## Output Style

For user-facing reports, provide:

- `Today learned`: latest cross-account themes.
- `Account deltas`: what each account emphasized.
- `Consensus vs isolated signal`: repeated themes versus one-off ideas.
- `Market mapping`: stocks, sectors, overseas-A-share mapping, and supply-chain layer.
- `Catalyst watch`: events, filings, products, policy, earnings, price changes, or conference dates to verify.
- `Signal quality`: Strong / Medium / Weak / Needs source check.
- `What changed`: new themes versus prior daily summaries.

Avoid reposting long X content. Summarize and cite local archive links or original post URLs.
