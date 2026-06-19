# -*- coding: utf-8 -*-
"""tgb-tangtang-radar 数据层:抓取淘股吧博客"快乐糖糖"(blog 3485724)最新文章。
免登录可抓(公开博客)。用法: python fetch_tgb.py [最多正文篇数,默认4]
输出: 帖子列表(标题/日期/浏览回复) + 最近N篇正文摘要。"""
import urllib.request as u, re, html, sys

BLOG_ID = "3485724"
NICK = "快乐糖糖"
BASE = "https://www.tgb.cn"


def get(url):
    req = u.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                                  "Referer": f"{BASE}/blog/{BLOG_ID}"})
    return u.urlopen(req, timeout=15).read().decode("utf-8", "ignore")


def list_posts():
    h = get(f"{BASE}/blog/{BLOG_ID}")
    # 列表块: <a href='a/{id}' title='标题'> ... tittle_llhf>浏览/回复 ... tittle_fbshijian>日期
    posts = []
    for m in re.finditer(r"<a href='(a/[A-Za-z0-9]+)' title='([^']+)'[^>]*>.*?tittle_llhf left\">([^<]*)</div>\s*<div class=\"tittle_fbshijian left\">(\d{4}-\d\d-\d\d)", h, re.S):
        href, title, llhf, date = m.groups()
        posts.append({"url": f"{BASE}/{href}", "title": html.unescape(title).replace("\xa0", " ").strip(),
                      "llhf": llhf.strip(), "date": date})
    return posts


def article_body(url):
    try:
        h = get(url)
    except Exception as e:
        return f"__ERR__ {type(e).__name__}"
    i = h.find('class="article_bd"')
    if i < 0:
        i = h.find('id="first"')
    if i < 0:
        return ""
    seg = h[i:i + 12000]
    # 截到正文结束标志
    for end in ['article_ft', 'class="zan_box"', 'class="blog_xgyd"', 'fenxiang', '相关阅读']:
        j = seg.find(end)
        if j > 200:
            seg = seg[:j]
            break
    txt = html.unescape(re.sub(r'<[^>]+>', ' ', seg))
    return re.sub(r'\s+', ' ', txt).strip()


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # 防GBK控制台崩溃
    except Exception:
        pass
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    posts = list_posts()
    print(f"# 淘股吧雷达 · {NICK} (blog {BLOG_ID})  共解析 {len(posts)} 篇")
    print("\n## 最近帖子列表")
    for p in posts[:12]:
        print(f"  - [{p['date']}] {p['title']}  (浏览/回复 {p['llhf']})  {p['url']}")
    print(f"\n## 最近 {n} 篇正文摘要")
    for p in posts[:n]:
        body = article_body(p["url"])
        print(f"\n### [{p['date']}] {p['title']}")
        print(f"{body[:700]}")


if __name__ == "__main__":
    main()
