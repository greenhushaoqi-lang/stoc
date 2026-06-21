# stock-api Source Map

Source: `https://github.com/zhangxiangliang/stock-api`

Snapshot inspected: 2026-06-21

## Repository Shape

`stock-api` is a TypeScript market-data package with no native Codex `SKILL.md` files and no standalone `agents/` directory in the inspected snapshot.

Main surfaces:

- `src/index.ts`: package entrypoint.
- `src/cli.ts`: CLI entrypoint compiled to `dist/cli.js`.
- `src/mcp/server.ts`: MCP JSON-RPC server and tool definitions.
- `src/stocks/index.ts`: exports `tencent`, `sina`, `eastmoney`, and `auto`.
- `src/stocks/auto/index.ts`: automatic provider fallback.
- `src/stocks/shared/provider.ts`: shared provider factory.
- `src/stocks/shared/code-mapper.ts`: unified-code to provider-code conversion.
- `src/stocks/*/transforms/*.ts`: provider-specific parsers.
- `docs/api.md`: API usage.
- `docs/cli.md`: CLI usage.
- `docs/architecture.md`: provider architecture.
- `docs/monitoring.md`: provider availability monitoring.

## Package Identity

From `package.json` in the inspected snapshot:

- npm name: `stock-api`
- version: `2.7.2`
- Node engine: `>=18`
- license: MIT
- bin: `stock-api`
- main module: `dist/index.js`
- browser module: `dist/browser/stock-api.esm.mjs`

## Provider Model

The package exposes:

```typescript
stocks.tencent
stocks.sina
stocks.eastmoney
stocks.auto
stocks.getSources()
stocks.getProviderCapabilities()
```

Each provider follows the same public shape:

```typescript
type StockApi = {
  getStock(code: string): Promise<Stock>;
  getStocks(codes: string[]): Promise<Stock[]>;
  getKlines(code: string, options?: KlineOptions): Promise<Kline[]>;
  searchStocks(keyword: string): Promise<Stock[]>;
  inspectStock(code: string): Promise<AutoStockInspection | StockProviderInspection>;
};
```

`stocks.auto` tries providers in this order:

```text
tencent -> sina -> eastmoney
```

For quote inspection, it records every provider result and picks the first successful stock. If all fail or return empty data, it returns a normalized base fallback stock.

## MCP Surface

`src/mcp/server.ts` exposes these MCP tools:

| Tool | Purpose | Required input |
| --- | --- | --- |
| `get_stock` | Fetch one normalized quote | `code` |
| `get_stocks` | Fetch multiple normalized quotes | `codes` |
| `get_klines` | Fetch K-line rows | `code` |
| `search_stocks` | Search symbols by keyword | `query` |
| `inspect_stock` | Inspect provider availability and fallback details | `code` |

Common optional input:

- `source`: `auto`, `tencent`, `sina`, or `eastmoney`

`get_klines` optional input:

- `period`: `day`, `week`, or `month`
- `count`: positive number, tool schema caps at 500
- `adjust`: `none`, `qfq`, or `hfq`

MCP configuration:

```json
{
  "mcpServers": {
    "stock-api": {
      "command": "npx",
      "args": ["-y", "stock-api", "mcp"]
    }
  }
}
```

## Data Contracts

Quote shape:

```typescript
type Stock = {
  code: string;
  name: string;
  percent: number;
  now: number;
  low: number;
  high: number;
  yesterday: number;
  source?: "base" | "tencent" | "sina" | "eastmoney";
};
```

K-line options:

```typescript
type KlineOptions = {
  period?: "day" | "week" | "month";
  count?: number;
  adjust?: "none" | "qfq" | "hfq";
};
```

K-line row:

```typescript
type Kline = {
  date: string;
  open: number;
  close: number;
  high: number;
  low: number;
  volume?: number;
  source?: "tencent" | "sina" | "eastmoney";
};
```

Inspection shape:

```typescript
type StockProviderInspection = {
  code: string;
  source: "tencent" | "sina" | "eastmoney";
  status: "success" | "empty" | "error";
  stock?: Stock;
  error?: string;
};

type AutoStockInspection = {
  code: string;
  source: "base" | "tencent" | "sina" | "eastmoney";
  stock: Stock;
  sources: StockProviderInspection[];
};
```

## Practical Caveats

- `stock-api` does not implement caching, queueing, or rate limiting.
- Unit tests avoid external network; integration tests hit real providers.
- Browser direct use is intended for low-frequency tools and demos. Production frontends should call a server-side wrapper for caching, throttling, and provider policy control.
- Sina browser access has limitations because the upstream service expects referer behavior that browsers cannot freely spoof.
- Eastmoney coverage is primarily A-share focused in this package.
- Public third-party quote APIs can change or throttle without notice.
