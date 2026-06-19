# -*- coding: utf-8 -*-
"""twelve-x-radar 数据层:抓取12个X账号最新推文(nitter RSS,免登录,nitter.net优先)。
用法: python fetch_x_radar.py
输出: 纯文本(账号→最近推文),供上层LLM归纳成每日雷达。"""
import urllib.request as u, re, html, datetime as dt

HANDLES = [
    ("ariston_macro", "Ariston/宏观"),
    ("hoyooyoo", "秋生trader/交易复盘"),
    ("off_thetarget", "pepper花椒(赚钱版)/短线"),
    ("lixon236", "Lixon/个股题材"),
    ("xiaoyeyeeey", "小D和小T的投研日记/AI算力·半导体投研"),
    ("ueutrt", "蓝筹-追梦人-备用号/⚠️疑似喊单导流,仅情绪"),
    ("xzzzjpl", "政经鲁社长/政经·宏观"),
    ("twikejin", "老法师(laofs.cn)/盘面情绪"),
    ("techflowpost", "TechFlow深潮/⚠️偏加密·科技媒体,非纯A股"),
    ("chaoxiangooo", "潮向研究/产业研究"),
    ("dacefupan", "大策复盘/A股复盘(亦在four-x雷达)"),
    ("andrew_fdwt", "A股证券交易员/交易视角(亦在four-x雷达)"),
]
NITTER_HOSTS = ["nitter.net", "xcancel.com", "nitter.privacydev.net", "nitter.poast.org"]


def fetch_rss(handle):
    for host in NITTER_HOSTS:
        try:
            req = u.Request(f"https://{host}/{handle}/rss", headers={"User-Agent": "Mozilla/5.0"})
            xml = u.urlopen(req, timeout=12).read().decode("utf-8", "ignore")
            if "<item>" in xml:
                return xml, host
        except Exception:
            continue
    return None, None


def parse(xml, limit=12):
    items = re.findall(r"<item>(.*?)</item>", xml, re.S)
    out = []
    for it in items[:limit]:
        t = re.search(r"<title>(.*?)</title>", it, re.S)
        d = re.search(r"<pubDate>(.*?)</pubDate>", it, re.S)
        text = html.unescape(re.sub("<.*?>", "", t.group(1))).strip() if t else ""
        out.append((d.group(1)[:16] if d else "", text))
    return out


def main():
    print(f"# 12-X雷达原始抓取  {dt.datetime.now():%Y-%m-%d %H:%M}")
    for handle, desc in HANDLES:
        xml, host = fetch_rss(handle)
        print(f"\n## @{handle}  ({desc})  [{host or '抓取失败'}]")
        if not xml:
            print("  - 未取到(所有nitter镜像失败,可改用WebSearch补)")
            continue
        for date, text in parse(xml):
            if text:
                print(f"  - [{date}] {text[:300]}")


if __name__ == "__main__":
    main()
