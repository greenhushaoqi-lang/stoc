# Source Policy

This skill monitors `https://x.com/livermoerr?s=21` for local research use.

## Preferred Sources

1. Official X API v2 with `X_BEARER_TOKEN` or `TWITTER_BEARER_TOKEN`.
2. User-provided exports through `--import-json` or `--import-jsonl`.
3. Public RSS/Nitter-style mirrors only when they are accessible and lawful for personal research.
4. Browser/manual review when X blocks unauthenticated access.

## Storage Rules

- Store raw post text only in the local skill folder.
- Keep compact summaries in `references/latest.md`.
- Do not publish raw archives to public repositories without the user's explicit request.
- Do not quote long X posts in user-facing reports.

## Failure Handling

If all public sources fail, write a status block to `references/latest.md` explaining:

- Which sources were attempted.
- Whether credentials are missing.
- The command the user can run after adding credentials.

This is still a valid daily update because it preserves monitoring state and makes the next action explicit.
