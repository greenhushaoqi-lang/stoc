---
name: china-quant-platforms
description: How to use three major Chinese quant platforms — 聚宽 JoinQuant (joinquant.com, jqdatasdk/JQData data + research/backtest), 果仁网 Guorn (guorn.com, wizard factor stock-picking + backtest), and 迅投 ThinkTrader/QMT (thinktrader.net, miniQMT/xtquant live auto-trading). Use this skill whenever the user mentions JoinQuant/聚宽/jqdatasdk/JQData, 果仁/Guorn/果仁网, 迅投/QMT/miniQMT/xtquant/xtdata/xttrader/ThinkTrader, or asks how to get A-share data, build/backtest a factor or stock-selection strategy, follow strategies, or run live/automated A-share trading on these platforms — even if they don't name the platform explicitly but describe "A股量化数据/选股/回测/实盘自动交易". A daily task keeps references/updates.md current; consult it for the latest platform changes.
---

# 中国量化平台 (JoinQuant / Guorn / ThinkTrader-QMT)

这三个平台覆盖量化交易的完整链条。最有用的心智模型是**分工**：

| 平台 | 定位 | 强项 | 编程要求 |
|---|---|---|---|
| **聚宽 JoinQuant** | 在线研究/回测 + 数据SDK | Python策略研究、因子、JQData数据 | 需 Python |
| **果仁网 Guorn** | 网页向导式选股/回测 | 海量A股因子库、零代码、策略广场跟单 | 零门槛 |
| **迅投 ThinkTrader/QMT** | 实盘交易终端 | miniQMT/xtquant 实盘自动下单 | 需 Python(实盘) |

**典型工作流**:用**果仁**或**聚宽**做因子选股与回测验证 → 在**迅投QMT**用 xtquant 把策略落地为实盘自动交易。本技能帮助在三者之间选型、取数、回测、并把研究结果接到实盘。

> ⚠️ 三个平台的深度内容(会员策略、完整文档、实盘接口密钥)多在登录后；公开可取的是文档要点、产品介绍与社区精华。涉及账户、密钥、下单的操作务必由用户自己确认执行。本技能仅作研究与使用指引，不构成投资建议。

## 选哪个？快速决策

- 想**用 Python 做策略研究/回测、要干净的A股数据** → 聚宽 (JoinQuant + jqdatasdk)。见 [references/joinquant.md](references/joinquant.md)。
- **不想写代码**，想用因子筛选/排名/轮动选股并秒级回测、跟单 → 果仁网。见 [references/guorn.md](references/guorn.md)。
- 研究好了要**实盘自动交易A股/期货/ETF/可转债** → 迅投 QMT / miniQMT (xtquant)。见 [references/thinktrader-qmt.md](references/thinktrader-qmt.md)。

## 三平台速用要点

### 聚宽 JoinQuant
- 在线研究环境(Jupyter式) + 回测IDE(`initialize` / `handle_data` / `before_trading_start` / `run_daily`)。
- 本地取数用 **jqdatasdk**：`auth('账号','密码')` 后 `get_price / get_fundamentals / get_factor_values / get_bars / get_all_securities / get_index_stocks`。
- 适合多因子选股、择时、组合回测。完整函数清单与示例见 references/joinquant.md。

### 果仁网 Guorn
- 网页向导：选**因子条件 + 排序 + 自定义公式** → 选股池 → 10年历史秒级回测 → 自动调仓/实盘跟踪。
- "策略广场"可跟随他人**实盘收益**验证过的策略。
- 适合不编程的因子/轮动策略与快速验证。详见 references/guorn.md。

### 迅投 ThinkTrader / QMT
- QMT(完整终端) 与 **miniQMT**(Python 直连，最常用)。核心库 **xtquant**：
  - `xtdata`：行情/历史数据下载(`download_history_data` / `get_market_data`)。
  - `xttrader` (`XtQuantTrader`)：连接交易端、下单、查持仓/委托/成交。
- 覆盖A股/期货/期权/ETF/债券，数据自2005年。可从聚宽迁移策略。详见 references/thinktrader-qmt.md。

## 每日更新（重要）
本技能由定时任务 `daily-quant-sites-learn` 每天抓取三站公开更新(文档/公告/产品/社区精华)，把当日要点追加到 [references/updates.md](references/updates.md)。**回答平台用法或"最近有什么新功能/变化"前，先读 references/updates.md 获取最新信息**；若该文件的最新日期较旧，提示用户更新任务可能未运行。

## 引用与免责
平台官网：joinquant.com / guorn.com / thinktrader.net（QMT文档 dict.thinktrader.net）。本技能为使用指引，涉及资金/下单/密钥的操作由用户自行确认；不构成投资建议。
