# Source Policy

This skill learns from local user-provided files under:

- `C:\Users\lixue\Desktop\st总结`

## Storage Rules

- Store compact summaries, extracted entities, and short snippets only.
- Do not upload original screenshots or full third-party long articles unless the user explicitly asks and has rights to publish them.
- Keep original files in the user's local folder as the source of truth.
- Treat blogger, X, Snowball, Douyin, WeChat article, and chat notes as market leads, not verified facts.

## Verification Rules

- Verify stock catalysts with market data, exchange filings, company announcements, credible news, or research reports before presenting conclusions.
- Clearly distinguish:
  - confirmed fact;
  - source chatter;
  - reasonable inference;
  - unverified rumor.
- Do not provide guaranteed buy/sell instructions or promise returns.

## Image Handling

- If OCR is unavailable, record image filenames as pending visual review.
- Use `references/manual-image-notes.jsonl` for human/Codex-read image summaries.
- Do not claim that an image was fully machine-read unless OCR or visual review was actually performed.
