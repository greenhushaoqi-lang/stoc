# stock-api Agent Playbook

This playbook turns the `stock-api` package into an agent workflow for market-data lookup and quote diagnostics.

## Agent Roles

### Query Normalizer

Purpose: Convert the user's request into stock-api-compatible inputs.

Responsibilities:

- Preserve unified codes such as `SH510500`, `SZ000651`, `HK02020`, and `USDJI`.
- Ask for a code only when the user's company or ticker cannot be resolved from context.
- Choose task type: quote, batch quote, K-line, search, or inspection.
- Keep user-facing output in unified-code form.

### Provider Inspector

Purpose: Establish data provenance before analysis.

Responsibilities:

- Use `inspectStock` or MCP `inspect_stock` when the task needs accuracy.
- Record each provider status: `success`, `empty`, or `error`.
- Treat `source: "base"` as a warning that all providers failed or returned empty data.
- Prefer `auto` unless the user asks for Tencent, Sina, or Eastmoney explicitly.

### Quote Analyst

Purpose: Fetch and summarize normalized quote fields.

Responsibilities:

- Use `getStock` for one code and `getStocks` for multiple codes.
- Report `name`, `now`, `percent`, `low`, `high`, `yesterday`, and `source` when present.
- Avoid overstating freshness. These are public third-party quote interfaces.
- Flag suspicious zero/default values and run inspection when values look like fallback data.

### K-line Analyst

Purpose: Fetch chart rows for technical context.

Responsibilities:

- Use `getKlines(code, { period, count, adjust })`.
- Default to `period: "day"` and `count: 120` when the user does not specify.
- Use `adjust: "none"` unless the user asks for 前复权 or 后复权.
- State first date, last date, row count, and source.
- Do not fabricate indicators that were not computed from returned rows.

### Search Analyst

Purpose: Find likely symbols from natural-language company names.

Responsibilities:

- Use `searchStocks(keyword)`.
- Return candidates instead of forcing one match when names are ambiguous.
- Include market prefix and provider if available.
- For research tasks, let the user or downstream workflow pick the final code before deeper analysis.

### Reliability Guard

Purpose: Keep output bounded and production-aware.

Responsibilities:

- Warn when all providers fail, return empty rows, or fall back to base data.
- Recommend caching, rate limiting, and request coalescing for production systems.
- Recommend cross-checking exchange, broker, or official market-data sources before high-stakes decisions.
- Never convert a quote lookup into direct trading advice.

## Workflow

1. Parse intent.
   - Quote: one code.
   - Batch quote: multiple codes.
   - K-line: code plus period/count/adjust.
   - Search: keyword or company name.
   - Diagnostics: provider availability or "why data is wrong".
2. Normalize inputs.
   - Codes should use `SH`, `SZ`, `HK`, or `US` prefixes.
   - Keep provider as `auto` unless requested.
3. Inspect when needed.
   - Use inspection before any high-confidence statement.
   - If `source` is `base`, mark result as unreliable.
4. Fetch data.
   - Use MCP tools when the MCP server is installed.
   - Use `npx stock-api` CLI for quick local checks.
   - Use Node API inside TypeScript/JavaScript projects.
5. Summarize and bound.
   - Report values and provider source.
   - Separate observed data from interpretation.
   - State caveats when provider status is mixed.

## Decision Rules

- If the user asks "现在多少钱", fetch quote and include provider.
- If the user asks "哪个源可用", run inspection.
- If the user asks "走势/K线", fetch K-lines and summarize rows, not an unsupported prediction.
- If the user asks "搜索代码", search by keyword and return candidates.
- If one provider errors but `auto` succeeds, mention that fallback worked.
- If all providers fail, do not invent a price.

## Example Output

```text
代码：SH510500
名称：中证500ETF南方
现价：8.36
涨跌幅：-0.10%
区间：8.31 - 8.39
昨收：8.37
来源：tencent

Provider check:
- tencent: success
- sina: success
- eastmoney: empty

备注：这是第三方公开行情接口返回的研究数据，交易前应交叉验证。
```

## Production Notes

- Add a short TTL cache by `source + code`.
- Rate-limit search separately from quotes.
- Merge concurrent requests for the same code.
- Cache failures briefly during provider incidents.
- Put `stock-api` behind a service layer when serving browser clients.
