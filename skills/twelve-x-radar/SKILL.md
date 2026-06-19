---
name: twelve-x-radar
description: 每日深度学习并汇总12个中文财经/A股X(推特)账号的最新观点、研报与荐股,映射到A股/港股/美股/日韩板块、题材与事件催化。覆盖账号:@ariston_macro(宏观)、@hoyooyoo(秋生trader)、@off_thetarget(pepper花椒)、@lixon236、@xiaoyeyeeey(小D和小T投研日记)、@ueutrt(蓝筹追梦人备用号)、@xzzzjpl(政经鲁社长)、@twikejin(老法师)、@techflowpost(深潮)、@chaoxiangooo(潮向研究)、@dacefupan(大策复盘)、@andrew_fdwt(A股交易员)。Use this skill whenever the user asks to monitor these X accounts, 学习/汇总它们当天的内容, 比较各账号观点, 提取最新题材/热板/荐股/研报, 或把它们发言映射到具体股票、板块、催化、宏观与海外映射。每日任务 daily-twelve-x-radar 把当天内容写入 references/daily/。回答"这些X博主今天说了啥/在荐什么"前,先读 references/daily/ 最新日期与 references/accounts.md。
---

# twelve-x-radar — 12个财经X账号每日深度学习雷达

每天深度学习这12个中文财经/A股X账号,提炼宏观/题材/热板/荐股/研报,并映射到可交易标的。**这是情绪与线索雷达,不是投资建议**;X荐股噪音大,务必用 expectation_gap_monitor / run_integrated(龙虎榜机构席位) / a-stock-data 二次过滤。

## 账号清单与质量分级（重要）

| 账号 | 名称 | 风格 | 可信度 |
|---|---|---|---|
| @ariston_macro | Ariston | 宏观/大盘/全球流动性 | 中,宏观视角 |
| @hoyooyoo | 秋生trader | 交易/复盘 | 中 |
| @off_thetarget | pepper花椒(赚钱版) | 短线题材 | 中 |
| @lixon236 | Lixon | 个股/题材 | 中 |
| @xiaoyeyeeey | 小D和小T的投研日记 | **AI算力/半导体/CPO/PCB投研** | 中高,产业链梳理 |
| @ueutrt | 蓝筹-追梦人-备用号 | 喊单+导流(@ueueueuwn备用号) | ⚠️**低,疑似荐股导流**,仅情绪,勿点链接 |
| @xzzzjpl | 政经鲁社长 | 政经/政策/宏观 | 中,政策面 |
| @twikejin | 老法师(laofs.cn) | 盘面/情绪 | 中 |
| @techflowpost | TechFlow深潮 | **加密/Web3/科技媒体** | 中,⚠️**偏crypto非纯A股** |
| @chaoxiangooo | 潮向研究 | 产业/主题研究 | 中高 |
| @dacefupan | 大策复盘 | A股复盘(亦在four-x雷达) | 中 |
| @andrew_fdwt | A股证券交易员 | 交易视角(亦在four-x雷达) | 中 |

详见 [references/accounts.md](references/accounts.md)。

## 抓取（免登录）
```bash
python scripts/fetch_x_radar.py        # 拉12账号最新推文(nitter多镜像,nitter.net优先)
```
镜像全失败时改用 WebSearch 检索账号近期内容,并注明来源与置信。

## 每日处理流程
1. 跑 `fetch_x_radar.py` 拿原始推文。
2. 归纳:每个账号今天的主题、点的**个股/板块/题材/研报**、有无**事件催化**、有无**宏观/政策**信号、有无**美股/日韩映射**。
3. **去伪存真**:多账号共振题材优先;@ueutrt 喊单/导流只记情绪、标注、不作依据、不点链接;@techflowpost 内容多为加密/科技,A股相关才纳入;识别诱导并标注。
4. 把当天要点写入 [references/daily/](references/daily/) 的 `YYYY-MM-DD.md`(最新在前)。
5. 映射到标的后,用预期差/龙虎榜工具(run_integrated.py)二次验证再下结论。

## 输出建议
回答"今天这些博主说了啥/在荐什么":按账号列要点 + 今日共振题材TOP + 对应个股 + 宏观/政策提示 + 风险/诱导提示。
> 免责:公开社媒信息汇总与研究,不构成投资建议;警惕喊单与导流诈骗。
