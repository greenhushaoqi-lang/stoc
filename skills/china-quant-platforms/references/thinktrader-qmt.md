# 迅投 ThinkTrader / QMT 使用参考

官网: http://thinktrader.net  | 文档: https://dict.thinktrader.net  | 口号: "连接全球交易"

## 是什么
迅投科技的量化交易终端。两种形态：
- **QMT**：完整图形终端，含策略编辑、回测、实盘。
- **miniQMT**：精简版，**用本地 Python 通过 xtquant 库直连**做行情+实盘下单——量化最常用。
覆盖A股/期货(CFFEX/SHFE/CZCE/DCE)/期权/ETF/债券/指数/板块概念，行情数据自2005年。支持内置Python、XtQuant原生API、VBA，并可从聚宽迁移策略。

## xtquant 三大模块
- **xtdata**：行情与历史数据。
  - `download_history_data(stock_code, period, start, end)` 先下载到本地。
  - `get_market_data(field_list, stock_list, period, start, end)` 取数据。
  - 订阅实时行情 `subscribe_quote`。
- **xttrader / XtQuantTrader**：交易。
  - 连接：`XtQuantTrader(path, session_id)` → `start()` → `connect()` → `subscribe(account)`。
  - 账户：`StockAccount('资金账号')`。
  - 下单：`order_stock(account, code, order_type, volume, price_type, price)`（如限价/市价、买/卖）。
  - 查询：`query_stock_asset / query_stock_positions / query_stock_orders / query_stock_trades`。
  - 回调：实现 `XtQuantTraderCallback` 接收委托/成交/账户变动推送。

## 典型实盘流程
1. 启动券商QMT客户端（迅投内核，需券商开通QMT/miniQMT权限）。
2. Python 用 xtdata 取行情、算信号（信号可来自聚宽/果仁的研究结论）。
3. 用 xttrader 连接交易端 → 按信号 `order_stock` 下单 → 回调里跟踪成交、管理持仓与风控。

## 在三平台分工中的位置
**研究在聚宽/果仁，落地在QMT**。把选股/择时信号接到 xttrader 即可实现A股全自动交易，这是散户能拿到的、最接近机构的实盘自动化通道之一。

## 限制/风险（务必重视）
- 需券商开通 QMT/miniQMT 权限，并有资金门槛；不同券商接口细节略有差异。
- **实盘下单是真金白银**：涉及下单、撤单、资金划转的代码必须由用户本人确认后运行；先用模拟/极小资金验证。
- 自动交易需做好风控（最大持仓、单笔上限、断线重连、异常停机），避免程序失控连续下单。
- 文档细节以 dict.thinktrader.net 最新版为准（接口会更新）。
