# Source Policy

This skill monitors configured Taoguba/TGB public blog pages for local market-research use.

## Preferred Sources

1. Public mobile blog pages, such as `https://m.tgb.cn/blog/3485724`.
2. Public mobile article pages, such as `https://m.tgb.cn/a/<slug>`.
3. User-provided exports through `--import-json` or `--import-jsonl`.

## Storage Rules

- Store raw article text only in the local skill folder unless the user explicitly asks to upload the generated skill and learning state.
- Keep compact summaries in `references/latest.md`.
- Do not quote long Taoguba articles in user-facing reports.
- Preserve original article URLs so claims can be checked.

## Market-Research Safety

- Treat Taoguba posts as leads, not proof.
- Verify claims with market data, exchange filings, company announcements, credible news, and primary sources.
- Mark account consensus separately from independent evidence.
- Flag rumor/valuation/price-target/profit-claim language as unverified until checked.
