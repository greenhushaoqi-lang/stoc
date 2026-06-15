---
name: nine-x-market-radar
description: "Daily learning and market-narrative radar for nine Chinese finance/stock X accounts: @xm597760789, @dzqinxng160469, @111_114390, @astocklink, @simu6668888, @ariston_macro, @sixpanny159920, @jizhongying123, and @0xrandle. Use when the user asks to monitor these X accounts, learn their daily content, summarize new market themes, compare account views, or map their posts to A-share/HK/US/Japan/Korea stocks, sectors, catalysts, AI, semiconductor, commodity, macro, or sentiment analysis."
---

# Nine X Market Radar

Use this skill to maintain and apply a daily knowledge base for nine tracked X accounts:

- `xm597760789`: `https://x.com/xm597760789?s=21`
- `dzqinxng160469`: `https://x.com/dzqinxng160469?s=21`
- `111_114390`: `https://x.com/111_114390?s=21`
- `astocklink`: `https://x.com/astocklink?s=21`
- `simu6668888`: `https://x.com/simu6668888?s=21`
- `ariston_macro`: `https://x.com/ariston_macro?s=21`
- `sixpanny159920`: `https://x.com/sixpanny159920?s=21`
- `jizhongying123`: `https://x.com/jizhongying123?s=21`
- `0xrandle`: `https://x.com/0xrandle?s=21`

Local memory:

- Latest learned state: `references/latest.md`
- Raw daily archive: `references/daily/YYYY-MM-DD.jsonl`
- Source and compliance rules: `references/source-policy.md`

## Update Workflow

Run the updater before analysis when the user asks for the newest view:

```powershell
python C:\Users\lixue\.codex\skills\nine-x-market-radar\scripts\update_nine_x_market_radar.py --skill-dir C:\Users\lixue\.codex\skills\nine-x-market-radar
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
