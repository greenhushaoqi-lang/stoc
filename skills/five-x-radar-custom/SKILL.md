---
name: five-x-radar-custom
description: 每日学习并汇总5个中文A股X(推特)账号的最新观点与荐股,映射到A股/港股/美股/日韩板块、题材与事件催化。覆盖账号:@zhanru188(战儒)、@astocklink(海外华人A股资讯)、@ueueueuwn(蓝筹-追梦人)、@xm597760789(复利先森)、@sanchesssmith(joy)。Use this skill whenever the user asks to monitor these X accounts, 学习/汇总它们当天的内容, 比较各账号观点, 提取最新题材/热板/荐股, 或把它们的发言映射到具体股票、板块、催化与海外映射。每日定时任务 daily-five-x-radar 会把当天内容写入 references/daily/。回答"这几个X博主今天说了啥/在荐什么"前,先读 references/daily/ 最新日期。
---

# five-x-radar-custom — 5个A股X账号每日雷达

每天学习这5个中文股票X账号的内容,提炼题材/热板/荐股,并映射到可交易标的。**这是情绪与线索雷达,不是投资建议**;X荐股噪音大,务必用财报/预期差(见 expectation_gap_monitor.py / china-quant-platforms 等)二次过滤。

## 账号清单与质量分级（重要）

| 账号 | 名称 | 风格 | 可信度 |
|---|---|---|---|
| @zhanru188 | 战儒 | 短线情绪/涨停题材 | 中,偏情绪 |
| @astocklink | 海外华人A股资讯 | 研报/资讯/海外映射 | **较高**(常带研报与海外链) |
| @ueueueuwn | 蓝筹-追梦人 | 喊单/翻倍口号+电报群导流 | ⚠️**低,疑似荐股导流/诱导**,仅作情绪,警惕诈骗链接 |
| @xm597760789 | 复利先森 | 群操作/热板复盘/实盘记录 | 中,短线 |
| @sanchesssmith | joy | 复盘/技术面情绪 | 中 |

详见 [references/accounts.md](references/accounts.md)。

## 怎么抓取（免登录）
X 时间线无法直接登录抓取,本技能用 **nitter RSS** 免登录获取:
```bash
python scripts/fetch_x_radar.py          # 拉5账号最新推文(多镜像容错)
```
镜像全失败时,改用 WebSearch 检索账号近期内容,并在记录里注明来源与置信。

## 每日处理流程
1. 跑 `fetch_x_radar.py` 拿原始推文。
2. 归纳:今天每个账号在说什么主题、点了哪些**个股/板块/题材**、有无**事件催化**、有无**美股/日韩映射**。
3. **去伪存真**:多账号共振的题材优先;@ueueueuwn 等喊单/导流内容只记情绪不当依据;识别"翻倍/跟车/进群"类诱导并标注。
4. 把当天要点写入 [references/daily/](references/daily/) 的 `YYYY-MM-DD.md`(最新在前)。
5. 映射到标的后,建议用预期差工具二次验证再下结论。

## 输出建议
回答用户"今天这几个博主说了啥/在荐什么"时:按账号列要点 + 汇总今日**共振题材TOP** + 对应个股 + 风险/诱导提示。
> 免责:仅为公开社媒信息汇总与研究,不构成投资建议;X荐股风险高,警惕喊单与导流诈骗。
