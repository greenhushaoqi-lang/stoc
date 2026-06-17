---
name: daily-market-summary-radar
description: "Daily learning radar for local A-share market summary notes and screenshot-derived frameworks in C:\\Users\\lixue\\Desktop\\st总结. Use when the user asks to learn, update, summarize, or apply daily market summaries, blogger/X notes, sector rotations, stock watchlists, index levels, catalysts, expectation gaps, risk warnings, or screenshot/article thinking frameworks."
---

# Daily Market Summary Radar

Use this skill to maintain and apply a daily local knowledge base from:

- Text notes: `C:\Users\lixue\Desktop\st总结\每日总结.txt`
- Images/screenshots in: `C:\Users\lixue\Desktop\st总结\`
- Manual image reading notes: `references/manual-image-notes.jsonl`

Local memory:

- Latest learned state: `references/latest.md`
- Compact daily archive: `references/daily/YYYY-MM-DD.jsonl`
- Source and storage rules: `references/source-policy.md`

## Update Workflow

Run the updater before analysis when the user asks for the newest view:

```powershell
python C:\Users\lixue\.codex\skills\daily-market-summary-radar\scripts\update_daily_market_summary_radar.py --skill-dir C:\Users\lixue\.codex\skills\daily-market-summary-radar --source-dir C:\Users\lixue\Desktop\st总结
```

The updater reads text files, indexes image files, merges manual image notes when available, extracts dates, themes, stock names, index levels, source/person mentions, action verbs, and risk warnings, then rebuilds `references/latest.md`.

Image OCR is optional. If OCR dependencies are unavailable, the updater records images as pending visual review and uses `references/manual-image-notes.jsonl` for manually learned image content.

## Analysis Workflow

When applying this skill to stock or sector research:

1. Read `references/latest.md`.
2. Separate signal layers:
   - `market framework`: article or long-form thinking method;
   - `daily notes`: user's daily summary text;
   - `source chatter`: blogger, X, Snowball, Douyin, or other informal recommendations;
   - `confirmed market data`: only after separate verification.
3. Treat all stock mentions as leads, not conclusions.
4. Map each stock to:
   - sector/theme;
   - catalyst;
   - expectation-gap source;
   - technical confirmation or invalidation level;
   - overseas mapping if relevant;
   - risk and crowding warning.
5. Give more weight to signals repeated across dates or across independent sources, but downgrade copied or purely emotional repetition.

## Current Framework Learned From The Provided Image

The 2026-06-17 screenshot article emphasizes:

- Avoid blindly applying the previous stage's logic to the next stage.
- Macro pressure may shift from inventory and oil to Fed communication, liquidity structure, and policy path.
- AI should be judged by actual productivity, order, revenue, margin, EPS, and cash-flow improvement, not only by narrative.
- Prefer sectors where price hikes and demand persist long enough to repair earnings.
- In A-share ecology, long-term holding needs both fundamentals and chip/flow structure.
- The next stage may favor AI upstream scarce metals/materials, semiconductor equipment/materials, MLCC upstream, PCB/CCL, optical module equipment, and CPU/GPU/storage supply-chain expansion.
- Risk control should track index levels, moving averages, crowding, high-open selloff, and failure to confirm EPS.

## Output Style

For user-facing reports, provide:

- `Today learned`: newest themes and changes from the local summary.
- `Framework takeaways`: reusable logic from long-form notes/images.
- `Stock map`: stock -> concept -> catalyst -> confirmation -> risk.
- `Consensus vs noise`: repeated signals versus isolated chatter.
- `Expectation-gap ranking`: research priority only, not investment advice.
- `Invalidation`: index levels, moving averages, sector cooling, or earnings failure.

Do not repost long article text or full third-party content. Summarize compactly.
