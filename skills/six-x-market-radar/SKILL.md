---
name: six-x-market-radar
description: "Daily learning and market-narrative radar for six Chinese finance/stock X accounts: @duangu888, @xiaoyeyeeey, @cnfinancewatch, @kugo_a10, @bianmian96608, and @oldk_gillis. Use when the user asks to monitor these X accounts, learn their daily content, summarize new market themes, compare account views, or map their posts to A-share/HK/US/Japan/Korea stocks, sectors, catalysts, AI, semiconductor, commodity, macro, or sentiment analysis."
---

# Six X Market Radar

Use this skill to maintain and apply a daily knowledge base for six tracked X accounts:

- `duangu888`: `https://x.com/duangu888?s=21`
- `xiaoyeyeeey`: `https://x.com/xiaoyeyeeey?s=21`
- `cnfinancewatch`: `https://x.com/cnfinancewatch?s=21`
- `kugo_a10`: `https://x.com/kugo_a10?s=21`
- `bianmian96608`: `https://x.com/bianmian96608?s=21`
- `oldk_gillis`: `https://x.com/oldk_gillis?s=21`

Local memory:

- Latest learned state: `references/latest.md`
- Raw daily archive: `references/daily/YYYY-MM-DD.jsonl`
- Source and compliance rules: `references/source-policy.md`

## Update Workflow

Run the updater before analysis when the user asks for the newest view:

```powershell
python C:\Users\lixue\.codex\skills\six-x-market-radar\scripts\update_six_x_market_radar.py --skill-dir C:\Users\lixue\.codex\skills\six-x-market-radar
```

The updater tries official X API if `X_BEARER_TOKEN` or `TWITTER_BEARER_TOKEN` exists, falls back to public RSS frontends account by account, writes deduped raw posts to `references/daily/`, and rebuilds `references/latest.md`.

If all sources fail, ask the user for an official API bearer token, a readable JSON/JSONL export, or permission to use a logged-in browser session if available.

## Analysis Workflow

When applying these accounts to market research:

1. Read `references/latest.md`.
2. Separate direct post evidence from inference.
3. Compare accounts:
   - `consensus themes`: repeated across 2+ accounts;
   - `isolated alpha`: one account posts a specific, checkable clue;
   - `noisy repetition`: vague hot-topic reposting without new evidence.
4. Map themes to A-share/HK/US/Japan/Korea tickers, supply-chain layer, event catalyst, price/volume confirmation, and invalidation signal.
5. Combine with existing finance and news skills for verification before drawing investment conclusions.

## Output Style

For user-facing reports, provide:

- `Today learned`: latest cross-account themes.
- `Account deltas`: what each account emphasized.
- `Market mapping`: stocks, sectors, and overseas-A-share mapping.
- `Catalyst watch`: events, filings, products, policy, earnings, or price changes to verify.
- `Signal quality`: Strong / Medium / Weak / Needs source check.
- `What changed`: new themes versus prior daily summaries.

Avoid reposting long X content. Summarize and cite local archive links or original post URLs.
