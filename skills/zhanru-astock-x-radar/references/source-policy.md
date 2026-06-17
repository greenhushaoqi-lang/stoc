# Source Policy

This skill monitors selected X accounts for local research use:

- `zhanru188`
- `astocklink`
- `ueueueuwn`
- `xm597760789`
- `sanchesssmith`

## Preferred Sources

1. Official X API v2 with `X_BEARER_TOKEN` or `TWITTER_BEARER_TOKEN`.
2. User-provided exports through `--import-json` or `--import-jsonl`.
3. Public RSS/Nitter-style mirrors only when accessible and lawful for personal research.
4. Browser/manual review when X blocks unauthenticated access.

## Storage Rules

- Store raw post text only in the local skill folder and user-requested repository copy.
- Keep compact summaries in `references/latest.md`.
- Do not quote long X posts in user-facing reports.
- Do not treat social posts as verified facts.

## Market-Research Safety

- Treat social posts as leads, not proof.
- Verify claims with market data, exchange filings, company announcements, credible news, and primary sources.
- Mark account consensus separately from independent evidence.
- Flag rumor, valuation, and price-target claims as unverified until checked.
