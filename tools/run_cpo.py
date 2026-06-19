# -*- coding: utf-8 -*-
"""CPO/光引擎(OE)/光通信篮子 预期差扫描(对应freearkshaw文章论点)。输出 reports/cpo_YYYYMMDD.txt"""
import os, time, datetime as dt
import expectation_gap_monitor as m

WATCHLIST = ["中际旭创","新易盛","天孚通信","太辰光","仕佳光子","光库科技","源杰科技",
             "德科立","长光华芯","光迅科技","华工科技","罗博特科"]
CONCEPT = {
    "中际旭创":"光模块龙头(800G/1.6T/CPO)","新易盛":"光模块(高速/CPO)","天孚通信":"无源光器件/CPO封装",
    "太辰光":"光器件/MPO/CPO","仕佳光子":"光芯片/AWG/光引擎","光库科技":"光器件/铌酸锂/CPO",
    "源杰科技":"光芯片(激光器)","德科立":"光模块/光器件/CPO","长光华芯":"光芯片(激光器)",
    "光迅科技":"光模块/光器件IDM","华工科技":"光模块/激光","罗博特科":"CPO封装设备",
}


def main():
    cache = m.load_cache(); today = dt.date.today()
    begin = (today - dt.timedelta(days=120)).isoformat(); end = today.isoformat()
    pairs = [(n, m.resolve_code(n, cache)) for n in WATCHLIST]
    import json; json.dump(cache, open(m.CODE_CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    quotes = m.fetch_quotes([c for _, c in pairs if c])
    rows = []
    for name, code in pairs:
        f = quotes.get(code[2:]) if code else None
        if not f:
            print("跳过", name, code); continue
        price = m.fnum(f[3])
        c = m.fetch_consensus(code, begin, end); fin = m.fetch_financials(code)
        E1, E2 = c["E1"], c["E2"]
        fpe = price / E1 if E1 and E1 > 0 else None
        g = (E2 / E1 - 1) * 100 if E1 and E2 and E1 > 0 else None
        peg = fpe / g if fpe and g and g > 0 else None
        tup = (c["target"] / price - 1) * 100 if c["target"] else None
        r = {"name": name, "code": code[2:], "concept": CONCEPT.get(name, ""), "price": price,
             "pct": m.fnum(f[32]), "amt": m.fnum(f[37]) / 1e4, "lb": m.fnum(f[49]) or 0.0,
             "hs": m.fnum(f[38]), "cov": c["cov"], "g": g, "fpe": fpe, "peg": peg, "tup": tup,
             "rev_yoy": fin["rev_yoy"], "np_yoy": fin["np_yoy"]}
        r["score"] = m.score(r); r["conf"] = m.confidence(c["cov"])
        rows.append(r); time.sleep(0.15)
    rows.sort(key=lambda r: r["score"], reverse=True)

    def sv(v, p=1): return ("%.*f" % (p, v)) if isinstance(v, (int, float)) else "-"
    stamp = quotes.get(pairs[0][1][2:], [""] * 31)[30] if pairs else ""
    head = (f"{'排名':<4}{'股票':<7}{'代码':<7}{'概念':<22}{'分':>6}{'置信':>5}{'现价':>9}{'涨%':>7}"
            f"{'量比':>5}{'研报':>4}{'增速%':>7}{'PEG':>6}{'目标%':>7}{'营收%':>7}{'净利%':>8}")
    L = [f"CPO/光引擎篮子 预期差扫描  时间: {stamp}", "", head]
    for i, r in enumerate(rows, 1):
        L.append(f"{i:<4}{r['name']:<7}{r['code']:<7}{r['concept']:<22}{r['score']:>6}{r['conf']:>5}"
                 f"{r['price']:>9.2f}{sv(r['pct']):>7}{sv(r['lb']):>5}{r['cov']:>4}{sv(r['g']):>7}"
                 f"{sv(r['peg'],2):>6}{sv(r['tup']):>7}{sv(r['rev_yoy']):>7}{sv(r['np_yoy']):>8}")
    report = "\n".join(L); print(report)
    out = os.path.join(m.HERE, "reports", f"cpo_{today.strftime('%Y%m%d')}.txt")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(report + "\n\n免责: 公开数据仅供研究, 不构成投资建议。")
    print("saved", out)


if __name__ == "__main__":
    main()
