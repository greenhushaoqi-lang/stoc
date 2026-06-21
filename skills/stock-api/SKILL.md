---
name: stock-api
category: data-source
description: 零依赖股票行情工具 stock-api（npm 包，by zhangxiangliang）。免费、无需 API key，查询 A 股 / 港股 / 美股的实时行情、批量行情、K 线（日/周/月，支持前复权后复权）、股票搜索、数据源诊断。内置腾讯/新浪/东方财富三数据源自动兜底。提供 CLI（npx）、Node.js/浏览器 API、MCP server 三种用法。Use when 用户要查个股实时价/涨跌幅/最高最低、批量报价、画 K 线、按名称搜代码，或想接入一个轻量级行情数据源（无需 Python，纯 Node）。
---

## Overview

`stock-api` 是一个**零运行时依赖**的 TypeScript 股票行情工具，支持 Node.js / 浏览器 / CLI / MCP 四种用法。默认 `auto` 模式按 `tencent -> sina -> eastmoney` 顺序自动兜底，单源失败自动切换。

- GitHub: https://github.com/zhangxiangliang/stock-api
- npm: `stock-api`（要求 Node.js >= 18）
- License: MIT
- 数据来源：腾讯、新浪、东方财富的公开行情接口（第三方，不保证准确性/实时性，仅供参考，非投资建议）

**本机环境注意**：在 Windows 上请用 **PowerShell** 运行 `npx`，Git Bash 下 npx 有路径 bug 会报 `ENOENT`。若遇 npx 缓存损坏报 ENOENT，先 `Remove-Item -Recurse -Force "$env:LOCALAPPDATA\npm-cache\_npx"` 再重试。

## 股票代码格式

统一用前缀 + 数字：

| 市场 | 前缀 | 示例 |
| --- | --- | --- |
| 上海 A 股 / ETF | `SH` | `SH600519`（贵州茅台）、`SH510500`（中证500ETF） |
| 深圳 A 股 | `SZ` | `SZ000651`（格力电器） |
| 港股 | `HK` | `HK02020`（安踏体育） |
| 美股 / 指数 | `US` | `USDJI`（道指）、`USAAPL` |

数据源可选：`auto`(默认) / `tencent` / `sina` / `eastmoney`。注意东方财富(`eastmoney`)仅支持 A 股。

## 用法一：CLI（最常用，零安装）

```powershell
# 单只行情
npx -y stock-api get-stock SH600519
npx -y stock-api get-stock SH510500 --source sina

# 批量行情
npx -y stock-api get-stocks SH600519 SZ000651 HK02020

# K 线（period: day|week|month；count 条数；adjust: none|qfq|hfq 前/后复权）
npx -y stock-api get-klines SH600519 --period day --count 120
npx -y stock-api get-klines SH600519 -p week -c 60 --adjust qfq

# 按关键词搜索股票（返回带行情的列表）
npx -y stock-api search-stocks 格力电器

# 帮助
npx -y stock-api --help
```

参数：`--source/-s`、`--period/-p`(默认 day)、`--count/-c`(默认 120)、`--adjust`(默认 none)。

### get-stock 输出示例

```json
{
  "code": "SH600519",
  "name": "贵州茅台",
  "percent": -0.0201,
  "now": 1215,
  "low": 1211.22,
  "high": 1238.87,
  "yesterday": 1240,
  "source": "tencent"
}
```

`percent` 是涨跌幅小数（0.01 = 1%）；`source` 是最终命中的数据源。

## 用法二：Node.js / 浏览器 API

```typescript
import { stocks } from "stock-api";

const stock   = await stocks.auto.getStock("SH600519");
const list    = await stocks.auto.getStocks(["SH510500", "SZ000651"]);
const klines  = await stocks.auto.getKlines("SH600519", { period: "day", count: 120, adjust: "qfq" });
const results = await stocks.auto.searchStocks("格力电器");
// 指定数据源：stocks.tencent / stocks.sina / stocks.eastmoney
```

浏览器 CDN：`<script src="https://cdn.jsdelivr.net/npm/stock-api/dist/browser/stock-api.iife.min.js"></script>`，全局对象 `StockApi.stocks.auto....`。

## 用法三：MCP server（接入 Claude / AI 客户端）

把 stock-api 作为 MCP server，AI 可直接调用 5 个工具。配置（写入 `.mcp.json` 或客户端 settings）：

```json
{
  "mcpServers": {
    "stock-api": { "command": "npx", "args": ["-y", "stock-api", "mcp"] }
  }
}
```

MCP 工具及入参：

| 工具 | 必填 | 可选 | 说明 |
| --- | --- | --- | --- |
| `get_stock` | `code` | `source` | 单只规范化行情 |
| `get_stocks` | `codes`(数组,≥1) | `source` | 批量行情 |
| `get_klines` | `code` | `period`(day/week/month), `count`(1-500), `adjust`(none/qfq/hfq), `source` | K 线 |
| `search_stocks` | `query` | `source` | 关键词搜代码 |
| `inspect_stock` | `code` | `source` | 诊断行情可用性与各数据源兜底详情 |

## 数据结构

**Stock**（行情）：`name, code, now(现价), low, high, percent(涨跌幅小数), yesterday(昨收), source`

**Kline**（K 线行）：`date(如 2026-05-22), open, close, high, low, volume?, source?`

## 选择建议

- 临时查 1~2 只 / shell 脚本 / CI 校验 → **CLI**。
- 网页或 Node 应用集成 → **API**。
- 让 Claude 自己反复取数 → **MCP**。
- 只要 A 股且想最稳 → 显式 `--source eastmoney` 或 `tencent`；跨市场用默认 `auto`。

## 免责声明

数据来自第三方公开接口，不保证准确/完整/实时，不构成投资建议。商用/高频前请自行确认数据源服务条款与合规。
