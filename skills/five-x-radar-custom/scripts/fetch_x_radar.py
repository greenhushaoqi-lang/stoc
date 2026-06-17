# -*- coding: utf-8 -*-
"""five-x-radar-custom 数据层:抓取5个X账号最新推文(nitter RSS,免登录)。
用法: python fetch_x_radar.py [--since YYYY-MM-DD]
输出: 纯文本(账号→最近推文),供上层LLM归纳成每日雷达。"""
import urllib.request as u, re, html, sys, datetime as dt

HANDLES = [
    ("zhanru188", "战儒/短线情绪题材"),
    ("astocklink", "海外华人A股资讯/研报映射(质量较高)"),
    ("ueueueuwn", "蓝筹-追梦人/⚠️疑似荐股导流,仅作情绪参考"),
    ("xm597760789", "复利先森/群操作热板复盘"),
    ("sanchesssmith", "joy/复盘技术面"),
]
NITTER_HOSTS = ["nitter.net", "nitter.privacydev.net", "xcancel.com", "nitter.poast.org"]


def fetch_rss(handle):
    for host in NITTER_HOSTS:
        try:
            req = u.Request(f"https://{host}/{handle}/rss", headers={"User-Agent": "Mozilla/5.0"})
            xml = u.urlopen(req, timeout=15).read().decode("utf-8", "ignore")
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
        ln = re.search(r"<link>(.*?)</link>", it, re.S)
        text = html.unescape(re.sub("<.*?>", "", t.group(1))).strip() if t else ""
        out.append((d.group(1)[:16] if d else "", text, ln.group(1) if ln else ""))
    return out


def main():
    since = None
    if "--since" in sys.argv:
        since = sys.argv[sys.argv.index("--since") + 1]
    print(f"# X雷达原始抓取  {dt.datetime.now():%Y-%m-%d %H:%M}")
    for handle, desc in HANDLES:
        xml, host = fetch_rss(handle)
        print(f"\n## @{handle}  ({desc})  [{host or '抓取失败'}]")
        if not xml:
            print("  - 未取到(所有nitter镜像失败,可改用WebSearch补)")
            continue
        for date, text, link in parse(xml):
            if not text:
                continue
            print(f"  - [{date}] {text[:300]}")


if __name__ == "__main__":
    main()
