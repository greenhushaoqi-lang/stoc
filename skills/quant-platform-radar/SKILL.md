---
name: quant-platform-radar
description: Daily learning and market-narrative radar for public content from JoinQuant, Guorn, and ThinkTrader. Use when the user asks to monitor, learn, summarize, or map these quant platforms' latest strategy, research, community, factor, backtest, A-share, ETF, portfolio, AI quant, or trading-system content into stock/sector analysis.
---

# Quant Platform Radar

Use this skill to monitor and apply public content from:

- JoinQuant: `https://www.joinquant.com/`
- Guorn: `https://guorn.com/`
- ThinkTrader: `http://thinktrader.net/`

Local memory:

- Latest learned state: `references/latest.md`
- Raw daily archive: `references/daily/YYYY-MM-DD.jsonl`
- Source and compliance rules: `references/source-policy.md`

## Update Workflow

Run the updater before analysis when the user asks for the newest view:

```powershell
python C:\Users\lixue\.codex\skills\quant-platform-radar\scripts\update_quant_platform_radar.py --skill-dir C:\Users\lixue\.codex\skills\quant-platform-radar
```

The updater reads public homepages, obvious sitemap/feed endpoints, and public search-result snippets where available. It writes deduplicated items to the daily archive and rebuilds `references/latest.md`.

If a source blocks access or requires login, treat it as unavailable public evidence. Do not bypass logins, paywalls, rate limits, or private APIs.

## Analysis Workflow

When applying this skill to market research:

1. Read `references/latest.md`.
   - On Windows PowerShell, use `Get-Content -Encoding UTF8` for Chinese text.
2. Separate platform evidence from inference:
   - `platform update`: official product, data, platform, or feature content;
   - `community strategy`: strategy/backtest/factor/portfolio posts from public pages;
   - `market clue`: public titles/snippets that point to a sector, ticker, style factor, or trading regime;
   - `weak lead`: search snippets or partial content that need verification.
3. Map themes to A-share/HK/US/Japan/Korea tickers only after checking live market data or credible news when the user asks for current opportunities.
4. Prefer repeated themes across 2+ sources, or one source plus price/volume confirmation.
5. Downgrade signals that are merely platform marketing, old tutorial content, or inaccessible snippets.

## Output Style

For user-facing reports, provide:

- `Today learned`: newest useful themes from the three platforms.
- `Source deltas`: what changed by JoinQuant, Guorn, and ThinkTrader.
- `Market mapping`: sectors, stocks, quant styles, and overseas-to-A-share mappings.
- `Signal quality`: Strong / Medium / Weak / Needs checking.
- `Catalyst watch`: what must be verified with market data, filings, research, news, or volume.

Avoid quoting long website text. Summarize briefly and cite the original URLs.
