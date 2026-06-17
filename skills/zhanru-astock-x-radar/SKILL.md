---
name: zhanru-astock-x-radar
description: "Daily learning and market-narrative radar for selected Chinese finance/stock X accounts: @zhanru188, @astocklink, @ueueueuwn, @xm597760789, and @sanchesssmith. Use when the user asks to monitor these X accounts, learn their daily content, update the corresponding skill memory, summarize new A-share/HK/US/Japan/Korea market themes, or map posts to stocks, sectors, catalysts, AI, semiconductor, materials, macro, policy, or sentiment analysis."
---

# Zhanru AStock X Radar

Use this skill to maintain and apply a daily local knowledge base for these tracked X accounts:

- `zhanru188`: `https://x.com/zhanru188?s=21`
- `astocklink`: `https://x.com/astocklink?s=21`
- `ueueueuwn`: `https://x.com/ueueueuwn?s=21`
- `xm597760789`: `https://x.com/xm597760789?s=21`
- `sanchesssmith`: `https://x.com/sanchesssmith?s=21`

Local memory:

- Latest learned state: `references/latest.md`
- Raw daily archive: `references/daily/YYYY-MM-DD.jsonl`
- Source and compliance rules: `references/source-policy.md`

## Update Workflow

Run the updater before analysis when the user asks for the newest view:

```powershell
python C:\Users\lixue\.codex\skills\zhanru-astock-x-radar\scripts\update_zhanru_astock_x_radar.py --skill-dir C:\Users\lixue\.codex\skills\zhanru-astock-x-radar
```

The updater tries the official X API when `X_BEARER_TOKEN` or `TWITTER_BEARER_TOKEN` exists, then falls back to public RSS/Nitter-style frontends account by account. It writes deduplicated raw posts to `references/daily/` and rebuilds `references/latest.md`.

If all sources fail, ask the user for one of:

- an official X API bearer token;
- a readable JSON/JSONL export with `handle` and `text` fields;
- permission to use a logged-in browser session if available.

## Analysis Workflow

When applying these accounts to market research:

1. Read `references/latest.md`.
2. Separate direct post evidence from inference.
3. Compare accounts:
   - `consensus themes`: repeated across 2+ accounts;
   - `isolated alpha`: one account posts a specific, checkable clue;
   - `noisy repetition`: vague hot-topic reposting without new evidence.
4. Map themes to A-share/HK/US/Japan/Korea tickers, supply-chain layer, event catalyst, price/volume confirmation, and invalidation signal.
5. Combine with existing finance, news, X-radar, and market-data skills before drawing conclusions.

## Output Style

For user-facing reports, provide:

- `Today learned`: latest cross-account themes.
- `Account deltas`: what each account emphasized.
- `Market mapping`: stocks, sectors, and overseas-to-A-share mapping.
- `Catalyst watch`: events, filings, products, policy, earnings, or price changes to verify.
- `Signal quality`: Strong / Medium / Weak / Needs source check.
- `What changed`: new themes versus prior daily summaries.

Avoid reposting long X content. Summarize and cite local archive links or original post URLs.
