# Source Policy

This skill monitors configured Xueqiu accounts for local market-research use.

## Preferred Sources

1. Xueqiu timeline APIs with a valid `XUEQIU_COOKIE` or `XQ_A_TOKEN`.
2. User-provided exports through `--import-json` or `--import-jsonl`.
3. RSSHub Xueqiu routes only when accessible.
4. Browser/manual review when Xueqiu blocks unauthenticated access.

## Storage Rules

- Store raw post text only in the local skill folder unless the user explicitly asks to upload the generated skill and learning state.
- Keep compact summaries in `references/latest.md`.
- Do not quote long Xueqiu posts in user-facing reports.
- Preserve original post URLs so claims can be checked.

## Market-Research Safety

- Treat Xueqiu posts as leads, not proof.
- Verify claims with market data, exchange filings, company announcements, credible news, and primary sources.
- Mark account consensus separately from independent evidence.
- Flag rumor/valuation/price-target claims as unverified until checked.
