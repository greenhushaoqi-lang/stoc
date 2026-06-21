---
name: stock-api
category: data-source
description: 零依赖股票行情工具 stock-api（npm 包，by zhangxiangliang）。免费、无需 API key，查询 A 股 / 港股 / 美股的实时行情、批量行情、K 线（日/周/月，支持前复权后复权）、股票搜索、数据源诊断。内置腾讯/新浪/东方财富三数据源自动兜底。提供 CLI（npx）、Node.js/浏览器 API、MCP server 三种用法。Use when 用户要查个股实时价/涨跌幅/最高最低、批量报价、画 K 线、按名称搜代码，或想接入一个轻量级行情数据源（无需 Python，纯 Node）。Research support only; no trade execution.
source: https://github.com/zhangxiangliang/stock-api
source_snapshot_date: 2026-06-21
---

# Stock API

`stock-api` 是一个零运行时依赖的 TypeScript 股票行情工具，支持 Node.js / 浏览器 / CLI / MCP 四种用法。默认 `auto` 模式按 `tencent -> sina -> eastmoney` 顺序自动兜底，单源失败自动切换。

源项目在检查时没有原生 Codex `SKILL.md` 或 `agents/` 目录，所以本 skill 将其 API、MCP 工具、数据源兜底逻辑和 agent 使用剧本整理成可复用资产。

非简单查询前先读：

- `references/stock-api-source-map.md`
- `references/stock-api-agent-playbook.md`
- `agents/stock-api-market-data-suite.yaml`

## Overview

- GitHub: https://github.com/zhangxiangliang/stock-api
- npm: `stock-api`（要求 Node.js >= 18）
- License: MIT
- 数据来源：腾讯、新浪、东方财富的公开行情接口（第三方，不保证准确性/实时性，仅供参考，非投资建议）

本机环境注意：在 Windows 上请用 PowerShell 运行 `npx`。若遇 npx 缓存损坏报 `ENOENT`，先执行：

```powershell
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\npm-cache\_npx"
```

## 股票代码格式

统一用前缀 + 数字：

| 市场 | 前缀 | 示例 |
| --- | --- | --- |
| 上海 A 股 / ETF | `SH` | `SH600519`（贵州茅台）、`SH510500`（中证500ETF） |
| 深圳 A 股 | `SZ` | `SZ000651`（格力电器） |
| 港股 | `HK` | `HK02020`（安踏体育） |
| 美股 / 指数 | `US` | `USDJI`（道指）、`USAAPL` |

数据源可选：`auto`（默认）/ `tencent` / `sina` / `eastmoney`。东方财富 `eastmoney` 主要支持 A 股。

## Data Sources

优先使用 `stocks.auto`，除非用户明确要求指定数据源。

自动兜底顺序：

```text
tencent -> sina -> eastmoney
```

直接 provider：

- `stocks.tencent`
- `stocks.sina`
- `stocks.eastmoney`

需要确认数据可靠性时，先使用 `inspectStock` 或 MCP `inspect_stock`，因为它会返回每个 provider 的 `success` / `empty` / `error` 状态，并标明最终来源。

## 用法一：CLI

```powershell
# 单只行情
npx -y stock-api get-stock SH600519
npx -y stock-api get-stock SH510500 --source sina

# 批量行情
npx -y stock-api get-stocks SH600519 SZ000651 HK02020

# K 线（period: day|week|month；count 条数；adjust: none|qfq|hfq）
npx -y stock-api get-klines SH600519 --period day --count 120
npx -y stock-api get-klines SH600519 -p week -c 60 --adjust qfq

# 按关键词搜索股票
npx -y stock-api search-stocks 格力电器

# 帮助
npx -y stock-api --help
```

参数：`--source/-s`、`--period/-p`（默认 day）、`--count/-c`（默认 120）、`--adjust`（默认 none）。

## 用法二：Node.js / 浏览器 API

```typescript
import { stocks } from "stock-api";

const stock = await stocks.auto.getStock("SH600519");
const list = await stocks.auto.getStocks(["SH510500", "SZ000651"]);
const klines = await stocks.auto.getKlines("SH600519", {
  period: "day",
  count: 120,
  adjust: "qfq",
});
const results = await stocks.auto.searchStocks("格力电器");
const inspection = await stocks.auto.inspectStock("SH510500");
```

浏览器 CDN：

```html
<script src="https://cdn.jsdelivr.net/npm/stock-api/dist/browser/stock-api.iife.min.js"></script>
```

全局对象：`StockApi.stocks.auto...`

## 用法三：MCP Server

把 `stock-api` 作为 MCP server，AI 客户端可直接调用 5 个工具：

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

MCP 工具及入参：

| 工具 | 必填 | 可选 | 说明 |
| --- | --- | --- | --- |
| `get_stock` | `code` | `source` | 单只规范化行情 |
| `get_stocks` | `codes`（数组，>=1） | `source` | 批量行情 |
| `get_klines` | `code` | `period`（day/week/month）, `count`（1-500）, `adjust`（none/qfq/hfq）, `source` | K 线 |
| `search_stocks` | `query` | `source` | 关键词搜代码 |
| `inspect_stock` | `code` | `source` | 诊断行情可用性与各数据源兜底详情 |

## 数据结构

Stock（行情）：

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

Kline（K 线行）：

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

## Workflow

1. 先明确代码、市场前缀、时间窗口、provider 偏好，以及用户要 quote / batch quote / K-line / search / inspection。
2. 高准确度任务先跑 `inspectStock` 或 MCP `inspect_stock`。
3. 常规查询用 `auto`；调试数据源差异时指定 `tencent`、`sina` 或 `eastmoney`。
4. 输出时标明最终 `source`；若来源是 `base`，标为低置信度。
5. 将结果限定为研究数据，不给直接交易指令。

## Output Shape

单只行情：

```text
代码：
名称：
现价：
涨跌幅：
区间：
昨收：
来源：
Provider check：
备注：
```

K 线：

```text
代码：
周期：
行数：
来源：
首末日期：
数据注意事项：
```

诊断：

```text
Selected source:
Provider statuses:
Fallback behavior:
Recommended next check:
```

## 选择建议

- 临时查 1-2 只 / shell 脚本 / CI 校验：CLI。
- 网页或 Node 应用集成：API。
- 让 AI 客户端自己反复取数：MCP。
- 只要 A 股且想指定源：可试 `eastmoney` 或 `tencent`；跨市场用默认 `auto`。

## Safety Boundary

- 不要把返回结果表述成保证实时、保证准确或保证完整。
- 不要仅基于 `stock-api` 输出给投资建议。
- 当前市场决策需交叉验证交易所、公告、券商行情或其他市场数据源。
- 商用、高频或生产使用前，请自行确认第三方数据源服务条款与合规要求。
