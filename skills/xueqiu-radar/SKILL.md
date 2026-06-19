---
name: xueqiu-radar
description: 每日深度学习并汇总7个雪球(xueqiu.com)财经/A股账号的最新观点、研报与持仓动态,映射到A股/港股/美股板块、题材与事件催化。覆盖账号(uid):5124430882、5672579962、1034624503、4086512744、7251377368、1301600236、4168622038。Use this skill whenever the user asks to monitor these 雪球 accounts, 学习/汇总它们当天的内容, 比较观点, 提取最新题材/热股/研报, 或把它们发言映射到具体股票、板块、催化。⚠️雪球有WAF反爬,抓取需登录态cookie(xq_a_token)。每日任务 daily-xueqiu-radar 把当天内容写入 references/daily/。回答前先读 references/daily/ 最新日期与 references/accounts.md。
---

# xueqiu-radar — 7个雪球账号每日深度学习雷达

每天深度学习这7个雪球账号(主帖/长文/调仓),提炼题材/热股/研报/持仓逻辑,映射到可交易标的。**这是观点与线索雷达,不是投资建议**;务必用 expectation_gap_monitor / run_integrated(龙虎榜机构席位) / a-stock-data 二次过滤。

## ⚠️ 重要:雪球需要 cookie 才能抓取
雪球(xueqiu.com)有 WAF 反爬,**匿名访问被拦截**(只返回JS挑战页/403),连昵称都解析不了。必须提供**登录态 cookie(含 xq_a_token)**:
- 方式1:环境变量 `XUEQIU_COOKIE="整段cookie"`
- 方式2:文件 `%USERPROFILE%\.xueqiu_cookie.txt`(内容为整段cookie)
- 如何拿:浏览器登录 xueqiu.com → F12 → Network → 任一 xueqiu 请求 → 复制 Request Headers 里的 `Cookie` 整段。
> cookie 会过期(通常数天~数周),失效后需重新复制。脚本在无cookie时会优雅提示,不会编造数据。

## 抓取
```bash
python scripts/fetch_xueqiu.py     # 读 cookie → 抓7账号 users/show + user_timeline
```
若脚本提示"未找到cookie"或返回WAF错误 → 在当日记录里标注"雪球未取到(需cookie/cookie失效)",并可改用 WebSearch 检索这些账号公开转载内容(注明来源/置信)。

## 每日处理流程
1. 跑 `fetch_xueqiu.py`(需cookie)拿原始帖。
2. 归纳:每个账号今天的主题、点的**个股/板块/题材/研报**、持仓/调仓动向、有无**事件催化**、有无**海外映射**。
3. 去伪存真:多账号共振题材优先;识别荐股/诱导并标注;长文研报提炼核心论点与"预期差点"。
4. 写入 [references/daily/](references/daily/) 的 `YYYY-MM-DD.md`(最新在前)。
5. 映射到标的后用 run_integrated.py 二次验证。

## 账号清单
见 [references/accounts.md](references/accounts.md)(uid + 主页链接;昵称待首次带cookie运行后回填)。

> 免责:公开社媒信息汇总与研究,不构成投资建议。
