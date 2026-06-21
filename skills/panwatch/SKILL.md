---
name: panwatch
category: trading-analysis
description: 盯盘侠 PanWatch（by TNT-Likely）的盯盘分析方法论与部署指南。一个自托管 AI 盯盘 Web 应用（FastAPI + React + Docker，集成 TradingAgents 多 Agent 决策）。本 skill 提炼了它 5 个定时 Agent（盘前展望/盘中监测/盘后日报/新闻速递/K线图分析）的提示词工程、标准化建议分类、ATR% 自适应异动阈值、多指标共振研判原则，以及 TradingAgents 9-Agent 工作流。Use when 用户要对持仓/自选股做盘前盘后复盘、盘中异动判断、新闻面解读、生成结构化操作建议（准备建仓/加仓/减仓/设置预警/观望），或想自托管部署 PanWatch 盯盘系统。
---

## Overview

**盯盘侠 PanWatch** 是一个开源、自托管的 AI 盯盘助手，覆盖 A 股 / 港股 / 美股，做实时监控、持仓管理、智能分析与全渠道推送（Telegram/微信/钉钉）。

- GitHub: https://github.com/TNT-Likely/PanWatch
- Docker: `sunxiao0721/panwatch`
- 技术栈：Python(FastAPI) 后端 + React/TS 前端，Playwright 截图，APScheduler 定时
- License: MIT
- 集成 [TradingAgents](https://github.com/TauricResearch/TradingAgents)（76k★）多 Agent 投资决策框架

**注意**：本 skill 不是把 PanWatch 跑起来才能用——它的核心价值是**盯盘分析方法论**，可直接拿来对用户持仓做分析。同时附部署指南。数据/结论仅供参考，非投资建议。

## 一、五个盯盘 Agent 的方法论（核心可复用资产）

PanWatch 用 5 个提示词驱动的 Agent 覆盖一个交易日。完整提示词见 [references/prompts.md](references/prompts.md)，要点：

| Agent | 触发 | 产出 | 输出格式 |
| --- | --- | --- | --- |
| 盘前展望 premarket_outlook | 开盘前 | 隔夜影响+消息面、每股今日展望(开盘预判/关键价位/操作策略)、重点关注 | Markdown + 末尾 PANWATCH_JSON |
| 盘中监测 intraday_monitor | 交易时段实时 | 异动/技术/量能/风险/机会/止盈信号判断 | 纯 JSON（无需提醒则 action=hold 空字段） |
| 盘后日报 daily_report | 收盘后 | 大盘概览、个股技术/资金/消息/相对强度深度分析、次日计划 | Markdown + PANWATCH_JSON |
| 新闻速递 news_digest | 定时 | 按股票维度合并、利好/利空/中性分类、影响判断 | Markdown + PANWATCH_JSON |
| K线图分析 chart_analyst | 按需 | 趋势/支撑压力/形态/量价/操作建议 | 纯文本（禁 Markdown），「」标注关键词 |

### 标准化操作建议分类（务必沿用这套术语）

- **盘前/盘后**：`准备建仓` / `准备加仓` / `准备减仓` / `设置预警` / `观望`
- **盘中**：`建仓` / `加仓` / `减仓` / `清仓` / `持有` / `观望`
- **新闻**：`设置预警` / `关注` / `继续持有` / `考虑减仓` / `暂时回避`
- 每只自选股**都必须**输出一行建议，即使是"观望/今日无相关资讯"。
- 代码规范：A 股 6 位数字；港股 5 位数字**保留前导 0**；美股 Ticker 大写。

### 结构化输出约定（PANWATCH_JSON）

Markdown 正文末尾追加可机读 JSON（有效 JSON、双引号、**不要**包代码块），用固定标签包裹：

```
<!--PANWATCH_JSON-->
{"suggestions":[{"symbol":"600519","action":"reduce","action_label":"准备减仓","signal":"放量滞涨RSI超买","reason":"...","triggers":["冲高不放量"],"invalidations":["重新放量突破压力"],"risks":["大盘回落带动"]}]}
<!--/PANWATCH_JSON-->
```

`action` 取值：`buy/add/reduce/sell/hold/watch/alert/avoid`。每股一条；`triggers`≤3、`invalidations`≤2、`risks`≤3；标签后不得再有任何输出。

## 二、技术研判核心原则（盘中监测精华）

1. **多指标共振 > 单一指标**。RSI/KDJ 超买超卖须结合趋势；量价配合是确认关键；支撑压力位附近更需关注。
2. **ATR% 自适应异动阈值**（最值得借鉴的一点）：判断"异动 vs 正常波动"用相对个股自身波动率的标准，而非固定百分比。
   - 自适应阈值 = `max(固定阈值, 1.5 × ATR%)`，涨跌幅超过它才算真异动。
   - 高波动股 ±5% 可能是常态，低波动股 ±3% 已属异动 → 避免对高波动股误报。
3. **按交易风格分档**：short(短线)关注 RSI/KDJ+≥2%、swing(波段)关注 MACD+≥3%、long(长线)关注趋势/估值+≥5%（百分比为固定下限，优先用 ATR% 自适应）。
4. 指标速查：MA 多空排列定趋势；MACD 金叉/死叉(高位死叉警惕)；RSI>80 严重超买/<20 严重超卖；KDJ J>100 超买/J<0 超卖；布林带收口蓄势、开口顺势；放量上涨健康、缩量上涨乏力；锤子/吞没/十字星形态。
5. 高权重先验：若某股有近期 TradingAgents 深度分析结论(ta_verdict)或相对大盘强度(relative_strength)，作为重点参考。

## 三、TradingAgents 9-Agent 深度分析工作流

持仓页点 🧠 触发，3-5 分钟一条完整推理链：

```
4 类分析师（技术 / 情绪 / 新闻 / 基本面）
        ↓
看多 vs 看空 多空辩论
        ↓
风控审查（Risk）
        ↓
PM 整合决策书 → 推送到 IM
```

默认 deepseek-chat，单次约 $0.05。本仓库实现见 `src/agents/tradingagents/`（agent / auto_trigger / cost_tracker / backfill）。

## 四、自托管部署

```bash
docker run -d --name panwatch -p 8000:8000 \
  -v panwatch_data:/app/data \
  sunxiao0721/panwatch:latest
```

访问 `http://localhost:8000`，首次设账号密码。首启会下载 Chromium（用于截图），不需要可设 `PLAYWRIGHT_SKIP_BROWSER_INSTALL=1`。

关键环境变量（`.env`）：

| 变量 | 说明 |
| --- | --- |
| `AI_BASE_URL` / `AI_API_KEY` / `AI_MODEL` | LLM 接口（默认智谱 glm-4，可换 deepseek 等 OpenAI 兼容端点） |
| `NOTIFY_TELEGRAM_BOT_TOKEN` / `NOTIFY_TELEGRAM_CHAT_ID` | Telegram 推送 |
| `HTTP_PROXY` | 国内访问 Telegram 代理 |
| `DAILY_REPORT_CRON` | 调度 cron，如 `30 15 * * 1-5`（工作日 15:30 盘后） |

本地开发：`make dev-api`（后端 :8000）、`make dev-web`（前端 :5183）。

## 如何用这个 skill

- 用户给持仓/自选股 → 按对应时段(盘前/盘中/盘后)套用上面的方法论与建议分类生成分析；需要机读时附 PANWATCH_JSON。
- 判断异动 → 用 ATR% 自适应阈值，别用死板百分比。
- 要部署 → 给 Docker 命令 + 环境变量。
- 需要完整原版提示词 → 见 [references/prompts.md](references/prompts.md)。

## 免责声明

方法论与数据均供参考，不构成投资建议。实盘决策自行判断、自负风险。
