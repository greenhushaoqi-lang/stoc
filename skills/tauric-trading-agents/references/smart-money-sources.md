# Smart-Money Source Monitor

Use these sources as alternative-data inputs for US-listed stocks, AI/tech/chip names, and cross-market theme scans. They are signal sources, not standalone buy/sell evidence.

## Required Sources

1. **Quiver Quantitative - Donald Trump Stock Trade Tracker**
   - URL: `https://www.quiverquant.com/Donald-Trump-Stock-Trades/`
   - Use for: Trump-related executive/political trade disclosures and post-disclosure performance.
   - Treat as: medium evidence after cross-checking the underlying filing or disclosure.
   - Watch fields: ticker, transaction type, reported/traded date, size range, sector, excess return after transaction.

2. **Capitol Trades - Congress trading**
   - URL: `https://www.capitoltrades.com/`
   - Pelosi profile: `https://www.capitoltrades.com/politicians/P000197`
   - Use for: congressional and spouse trading disclosures, especially Pelosi and high-signal committee members.
   - Treat as: medium evidence for disclosure existence, weak-to-medium evidence for investment merit.
   - Watch fields: politician, owner, transaction type, filed date, traded date, delay, size range, issuer, sector.

3. **WhaleWisdom - ARK/13F institutional holdings**
   - URL: `https://whalewisdom.com/filer/ark-investment-management-llc`
   - Use for: ARK Investment Management 13F changes, top holdings, sector exposure, new/added/reduced positions.
   - Treat as: medium evidence for institutional positioning, stale for real-time trading because 13F reports are delayed.
   - Watch fields: quarter, filing date, new buys, adds, reductions, exits, concentration, top holdings.

4. **Dataroma - Buffett and superinvestors**
   - URL: `https://www.dataroma.com/`
   - Buffett/Berkshire example: `https://www.dataroma.com/m/holdings.php?m=BRK`
   - Use for: Berkshire Hathaway and other superinvestor holdings, activity, buys, sells, and concentration.
   - Treat as: medium evidence for long-term ownership signal, stale for real-time timing.
   - Watch fields: portfolio date, reported price, activity label, portfolio weight, new buys, reductions, exits.

## Monitoring Routine

When asked to analyze a stock or scan opportunities:

1. Search the four sources for the ticker and close peers.
2. Record whether the signal is:
   - `fresh disclosure`: recent political/congressional disclosure or newly imported filing;
   - `stale positioning`: 13F/superinvestor data from a prior quarter;
   - `copy-trade momentum`: strong post-disclosure performance or social attention;
   - `no signal`: no relevant activity found.
3. Cross-check high-impact signals against original filings where possible:
   - SEC 13F, 13D/G, Form 4, or company filings;
   - congressional periodic transaction reports;
   - official company announcements and earnings materials.
4. Add a `Smart-money signal` line to the final answer:
   - `Who traded or held it`
   - `When it was reported`
   - `Whether it was buy/add/reduce/sell`
   - `How stale the signal is`
   - `Whether fundamentals support or contradict the signal`

## Caveats

- Political and congressional trades are often disclosed after the trade date; do not treat them as real-time order flow.
- 13F data is quarterly and delayed; use it for institutional thesis discovery, not precise timing.
- High post-disclosure return can mean the edge is already gone.
- Position size ranges can be broad, and owner/spouse/entity details matter.
- Quiver, Capitol Trades, WhaleWisdom, and Dataroma are aggregators. Prefer original filings for high-conviction claims.
- Never recommend copying a trade without fundamental, news, technical, and risk-adjusted confirmation.

## Signal Grading

- **Strong**: source signal plus original filing plus matching fundamental/news catalyst.
- **Medium**: reliable aggregator signal with clear dates and matching price/volume confirmation.
- **Weak**: social attention, unexplained post-disclosure rally, old 13F activity, or isolated copy-trade signal.
- **Needs checking**: aggregator shows activity but original disclosure or filing has not been verified.
