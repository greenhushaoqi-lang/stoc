# Source Policy

This skill monitors twelve X accounts for local market-research use:

- `ariston_macro`
- `hoyooyoo`
- `off_thetarget`
- `lixon236`
- `xiaoyeyeeey`
- `ueutrt`
- `xzzzjpl`
- `twikejin`
- `techflowpost`
- `chaoxiangooo`
- `dacefupan`
- `andrew_fdwt`

## Preferred Sources

1. Official X API v2 with `X_BEARER_TOKEN` or `TWITTER_BEARER_TOKEN`.
2. User-provided exports through `--import-json` or `--import-jsonl`.
3. Public RSS/Nitter-style mirrors only when accessible and lawful for personal research.
4. Browser/manual review when X blocks unauthenticated access.

## Storage Rules

- Store raw post text only in the local skill folder unless the user explicitly asks to upload the generated skill and its learning state.
- Keep compact summaries in `references/latest.md`.
- Do not quote long X posts in user-facing reports.
- Preserve original post URLs so claims can be checked.

## Market-Research Safety

- Treat social posts as leads, not proof.
- Verify claims with market data, exchange filings, company announcements, credible news, and primary sources.
- Mark account consensus separately from independent evidence.
- Flag rumor/valuation/price-target claims as unverified until checked.
