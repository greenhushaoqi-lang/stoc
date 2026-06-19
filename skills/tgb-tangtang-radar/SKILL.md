---
name: tgb-tangtang-radar
description: 每日深度学习并汇总淘股吧(tgb.cn)博客"快乐糖糖"(blog/3485724)的最新文章——短线游资风格的题材方向、热股、盘面观点与情绪。提炼其主线(AI科技/硅基/玻璃基板/MLCC/铜箔/CPO/AI金属等)并映射到A股个股、板块与事件催化。Use this skill whenever the user asks to monitor 快乐糖糖/淘股吧/tgb 这个博客、学习/汇总它当天文章、提取其题材方向与点的票、或把它的观点映射到具体股票、板块、催化。免登录可抓。每日任务 daily-tgb-tangtang 把当天内容写入 references/daily/。回答前先读 references/daily/ 最新日期与 references/accounts.md。
---

# tgb-tangtang-radar — 淘股吧"快乐糖糖"每日雷达

每天深度学习淘股吧博客"快乐糖糖"(https://www.tgb.cn/blog/3485724)的文章,提炼其**题材方向/热股/盘面情绪**,映射到可交易标的。**这是短线游资风格的方向与情绪线索,不是投资建议**;务必用 expectation_gap_monitor / run_integrated(龙虎榜机构席位) 二次过滤。

## 风格与质量（重要）
- **快乐糖糖** = 短线/游资风格、题材敏锐(常第一时间点新细分方向),但**自我营销极强**("跟着我2天30个点""喂到嘴里"),且**个股常不明说**(让你跟感觉/抢竞价)。
- **正确用法**:取其**方向/题材**(玻璃基板、MLCC、铜箔、AI金属、CPO/MPO、中巨芯/中船特气等)作线索,**不把其个股喊单当依据**;识别并忽略自我吹嘘。

## 抓取（免登录）
```bash
python scripts/fetch_tgb.py 4      # 列表(标题/日期/浏览回复) + 最近4篇正文
```
抓取自公开博客页(`tgb.cn/blog/3485724`),解析文章 `a/{id}` + 日期,再取正文。

## 每日处理流程
1. 跑 `fetch_tgb.py` 拿最新文章列表 + 正文。
2. 归纳:今天糖糖在讲哪些**主线/细分方向**、点了哪些**个股/题材**、对**盘面/大盘**的看法、有无**事件催化/海外映射**。
3. 去伪存真:**只提炼方向与题材**,个股喊单仅作线索;标注其自我营销;多与其它雷达(X/雪球)共振的方向更可信。
4. 写入 [references/daily/](references/daily/) 的 `YYYY-MM-DD.md`(最新在前)。
5. 映射到标的后用 run_integrated.py 二次验证。

## 账号
见 [references/accounts.md](references/accounts.md)。

> 免责:公开社媒/论坛信息汇总与研究,不构成投资建议;警惕自我营销与短线追高。
