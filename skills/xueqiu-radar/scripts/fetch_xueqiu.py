# -*- coding: utf-8 -*-
"""xueqiu-radar 数据层:抓取7个雪球账号最新动态。
⚠️ 雪球有WAF反爬,匿名取不到数据——必须提供登录态 cookie(含 xq_a_token)。
cookie 来源(任选其一):
  1) 环境变量 XUEQIU_COOKIE = "整段cookie字符串"
  2) 文件 %USERPROFILE%\.xueqiu_cookie.txt (内容为整段cookie)
如何拿cookie:浏览器登录 xueqiu.com → F12 → Network → 任一xueqiu请求 → 复制 Request Headers 里的 Cookie 整段。
用法: python fetch_xueqiu.py
"""
import urllib.request as u, http.cookiejar as cj, json, os, time

UIDS = [  # (uid, 备注名-待cookie解析后回填)
    ("5124430882", ""), ("5672579962", ""), ("1034624503", ""),
    ("4086512744", ""), ("7251377368", ""), ("1301600236", ""), ("4168622038", ""),
]
COOKIE_FILE = os.path.join(os.path.expanduser("~"), ".xueqiu_cookie.txt")


def load_cookie():
    c = os.getenv("XUEQIU_COOKIE")
    if c:
        return c.strip()
    if os.path.isfile(COOKIE_FILE):
        return open(COOKIE_FILE, encoding="utf-8").read().strip()
    return None


def make_opener(cookie):
    op = u.build_opener(u.HTTPCookieProcessor(cj.CookieJar()))
    hdr = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"),
           ("Referer", "https://xueqiu.com/")]
    if cookie:
        hdr.append(("Cookie", cookie))
    op.addheaders = hdr
    return op


def fetch_user(op, uid, count=10):
    # 用户资料(取昵称)
    name = uid
    try:
        d = json.loads(op.open(f"https://xueqiu.com/users/show.json?id={uid}", timeout=12).read().decode("utf-8", "ignore"))
        name = d.get("screen_name") or uid
    except Exception:
        pass
    # 用户时间线(最近帖)
    posts = []
    try:
        raw = op.open(f"https://xueqiu.com/v4/statuses/user_timeline.json?user_id={uid}&page=1", timeout=12).read().decode("utf-8", "ignore")
        d = json.loads(raw)
        import re
        for st in (d.get("statuses") or [])[:count]:
            t = st.get("text") or st.get("description") or ""
            t = re.sub(r"<[^>]+>", "", t)
            t = re.sub(r"\s+", " ", t).strip()
            ct = st.get("created_at")
            posts.append((ct, t))
    except Exception as e:
        posts = [("", f"__ERR__ {type(e).__name__}")]
    return name, posts


def main():
    cookie = load_cookie()
    print(f"# 雪球雷达抓取  {time.strftime('%Y-%m-%d %H:%M')}")
    if not cookie:
        print("\n⚠️ 未找到雪球cookie(XUEQIU_COOKIE 环境变量 或 ~/.xueqiu_cookie.txt)。")
        print("雪球WAF拦截匿名访问,无法抓取。请按脚本顶部说明提供cookie后重试。")
        return
    op = make_opener(cookie)
    # 预热拿 acw_tc
    try:
        op.open("https://xueqiu.com/", timeout=12).read()
    except Exception:
        pass
    for uid, _ in UIDS:
        name, posts = fetch_user(op, uid)
        print(f"\n## {name} (uid={uid})  https://xueqiu.com/u/{uid}")
        for ct, t in posts[:8]:
            if t:
                print(f"  - {t[:300]}")
        time.sleep(1.0)  # 礼貌限速,防WAF


if __name__ == "__main__":
    main()
