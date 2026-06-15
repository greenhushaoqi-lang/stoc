---
name: livermoerr-x-radar
description: Daily learning and market-narrative radar for the X/Twitter account @livermoerr. Use when the user asks to monitor, learn from, summarize, update, or apply livermoerr's daily X posts to stock, macro, AI, semiconductor, crypto, or market sentiment analysis.
---

# Livermoerr X Radar

Use this skill to maintain and apply a daily knowledge base for the X account:

- Profile URL: `https://x.com/livermoerr?s=21`
- Canonical handle: `livermoerr`
- Local raw archive: `references/daily/`
- Latest learned state: `references/latest.md`
- Source and compliance rules: `references/source-policy.md`

## Update Workflow

1. Run the updater before analysis when the user asks for the newest view:

```powershell
python C:\Users\lixue\.codex\skills\livermoerr-x-radar\scripts\update_livermoerr_x_skill.py --skill-dir C:\Users\lixue\.codex\skills\livermoerr-x-radar
```

2. If the script reports an authentication or source-access failure, ask the user for one of:
   - `X_BEARER_TOKEN` or `TWITTER_BEARER_TOKEN` for official X API access.
   - A readable export file through `--import-json` or `--import-jsonl`.
   - Permission to use a logged-in browser session if available.

3. Read `references/latest.md` after every successful update. It is the compact skill memory that should be loaded for analysis.

4. For deeper review, inspect the matching file under `references/daily/YYYY-MM-DD.jsonl`.

## Analysis Workflow

When applying this account to market research:

1. Separate direct post evidence from inference.
2. Extract repeated themes, tickers, cashtags, sectors, macro variables, and event timing.
3. Score each theme:
   - `freshness`: today / this week / stale.
   - `conviction`: repeated, explicit, or passing mention.
   - `market mapping`: ticker, sector, A-share mapping, overseas mapping, commodity, or macro asset.
   - `risk`: rumor, low evidence, consensus crowdedness, or post-facto commentary.
4. Combine with existing finance skills for price, volume, news, fundamentals, and catalyst verification.
5. Never treat one X account as a buy/sell signal by itself.

## Output Style

For user-facing reports, provide:

- `Today learned`: concise themes from the latest posts.
- `Market mapping`: related stocks, sectors, or assets.
- `Catalyst watch`: events or data that can confirm/deny the narrative.
- `Signal quality`: Strong / Medium / Weak / Needs login/source check.
- `What changed`: new themes versus prior daily summaries.

Avoid reposting long X content. Use short snippets only when necessary and prefer summaries.
