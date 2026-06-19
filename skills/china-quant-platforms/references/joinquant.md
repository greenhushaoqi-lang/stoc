# 聚宽 JoinQuant 使用参考

官网: https://www.joinquant.com  | API文档: joinquant.com/help/api/help | 数据SDK: jqdatasdk (JQData)

## 是什么
在线量化平台：研究环境(Jupyter式notebook) + 策略回测IDE + 模拟/实盘交易 + JQData数据服务。面向A股、期货、基金等的量化策略研究。

## 两种使用方式
1. **平台内回测**（策略框架）——在网站IDE里写策略，结构固定：
   - `initialize(context)`：设置基准、手续费、universe、`run_daily(func, time)`。
   - `before_trading_start(context)`：盘前选股/计算因子。
   - `handle_data(context, data)`：逐bar逻辑（或用 run_daily 定时函数）。
   - 下单：`order(security, amount)` / `order_target(security, amount)` / `order_value` / `order_target_value`。
   - 取数(回测内)：`attribute_history` / `history` / `get_current_data` / `get_fundamentals` / `get_factor_values`。
2. **本地取数 jqdatasdk**（把聚宽数据拉到本地分析/喂给别的工具）：
   ```python
   from jqdatasdk import *
   auth('手机号', '密码')              # 需开通JQData权限
   get_price('000001.XSHE', start_date='2026-01-01', end_date='2026-06-16',
             frequency='daily', fields=['open','close','high','low','volume'])
   get_fundamentals(query(valuation.code, valuation.pe_ratio, valuation.pb_ratio,
                          indicator.roe).filter(valuation.code=='000001.XSHE'), date='2026-06-15')
   get_factor_values('000001.XSHE', ['roe_ttm','pe_ratio'], end_date='2026-06-15', count=1)
   get_index_stocks('000300.XSHG')     # 沪深300成分
   get_all_securities(types=['stock'])
   get_trade_days(start_date='2026-01-01', end_date='2026-06-16')
   ```
   注意代码后缀：上交所 `.XSHG`，深交所 `.XSHE`。

## 常用数据/函数
- 行情：`get_price`, `get_bars`, `attribute_history`, `history`
- 基本面：`get_fundamentals`(valuation/income/balance/cash_flow/indicator 表), `get_fundamentals_continuously`
- 因子：`get_factor_values`(内置数百因子), 也可自建
- 成分/分类：`get_index_stocks`, `get_industry_stocks`, `get_concept_stocks`
- 交易：`order` / `order_target` / `order_value` 系列；`run_daily` 定时调度

## 典型用途
多因子选股、行业轮动、择时、组合回测、绩效归因。研究→回测→模拟→实盘的闭环。

## 与本地工具衔接
jqdatasdk 取到的数据可直接喂给本仓库 expectation_gap_monitor.py 之外的分析，或与 akshare/tushare 互为数据源(见仓库 data-routing 技能的取数优先级)。

## 限制/注意
- JQData 数据权限需账号开通(有免费额度/付费档)；调用有频次限制。
- 网站页面多为JS渲染，自动抓取正文困难；本参考基于公开文档与通用知识，细节以官网最新文档为准。
