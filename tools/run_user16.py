# -*- coding: utf-8 -*-
"""用户指定16只 实时预期差扫描。输出 reports/user16_YYYYMMDD.txt"""
import os, time, datetime as dt
import expectation_gap_monitor as m

UNIV = [
    ("日联科技","X射线检测设备"),("奕东电子","光模块液冷/FPC"),("厦门钨业","钨/AI金属"),
    ("微导纳米","ALD半导体设备"),("中富电路","高端PCB"),("世运电路","高端PCB"),
    ("德科立","CPO/光模块"),("江丰电子","靶材"),("富创精密","半导体设备零件"),
    ("源杰科技","光芯片"),("长川科技","半导体测试设备"),("云南锗业","锗/光通信材料"),
    ("江南新材","PCB铜基材料"),("海亮股份","铜/铜箔"),("赛腾股份","半导体/消费电子设备"),
    ("晶丰明源","AI电源芯片"),
]


def main():
    cache = m.load_cache(); today = dt.date.today()
    begin = (today - dt.timedelta(days=120)).isoformat(); end = today.isoformat()
    pairs = [(n, m.resolve_code(n, cache), th) for n, th in UNIV]
    import json; json.dump(cache, open(m.CODE_CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    quotes = m.fetch_quotes([c for _, c, _ in pairs if c])
    rows = []
    for name, code, theme in pairs:
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
        r = {"name": name, "code": code[2:], "theme": theme, "price": price, "pct": m.fnum(f[32]),
             "lb": m.fnum(f[49]) or 0.0, "cov": c["cov"], "g": g, "fpe": fpe, "peg": peg, "tup": tup,
             "rev_yoy": fin["rev_yoy"], "np_yoy": fin["np_yoy"]}
        r["score"] = m.score(r); r["conf"] = m.confidence(c["cov"])
        rows.append(r); time.sleep(0.12)
    rows.sort(key=lambda r: r["score"], reverse=True)

    def sv(v, p=1): return ("%.*f" % (p, v)) if isinstance(v, (int, float)) else "-"
    stamp = quotes.get(pairs[0][1][2:], [""] * 31)[30] if pairs and pairs[0][1] else ""
    head = (f"{'#':<3}{'股票':<7}{'代码':<7}{'主题':<16}{'分':>6}{'置信':>5}{'现价':>9}{'涨%':>7}"
            f"{'量比':>5}{'研报':>4}{'增速%':>7}{'PEG':>6}{'目标%':>7}{'营收%':>7}{'净利%':>8}")
    L = [f"用户16只 预期差扫描  时间: {stamp}  ({len(rows)}只)", "", head]
    for i, r in enumerate(rows, 1):
        L.append(f"{i:<3}{r['name']:<7}{r['code']:<7}{r['theme']:<16}{r['score']:>6}{r['conf']:>5}"
                 f"{r['price']:>9.2f}{sv(r['pct']):>7}{sv(r['lb']):>5}{r['cov']:>4}{sv(r['g']):>7}"
                 f"{sv(r['peg'],2):>6}{sv(r['tup']):>7}{sv(r['rev_yoy']):>7}{sv(r['np_yoy']):>8}")
    report = "\n".join(L); print(report)
    out = os.path.join(m.HERE, "reports", f"user16_{today.strftime('%Y%m%d')}.txt")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(report + "\n\n免责: 公开数据仅供研究, 不构成投资建议。")
    print("saved", out)


if __name__ == "__main__":
    main()
