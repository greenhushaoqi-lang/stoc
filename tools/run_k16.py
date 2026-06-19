# -*- coding: utf-8 -*-
"""16只 当日K线形态 + 预期差扫描。输出 reports/k16_YYYYMMDD.txt"""
import os, time, datetime as dt
import expectation_gap_monitor as m

WATCHLIST = ["泰晶科技","中富电路","三环集团","世运电路","德科立","江丰电子","铜冠铜箔","德福科技",
             "帝尔激光","富创精密","长川科技","云南锗业","江南新材","海亮股份","赛腾股份","晶丰明源"]


def kshape(f):
    """根据 收盘/昨收/最高/最低 推断当日K线形态。"""
    price = m.fnum(f[3]); pre = m.fnum(f[4]); hi = m.fnum(f[33]); lo = m.fnum(f[34])
    pct = m.fnum(f[32]); lb = m.fnum(f[49]) or 0.0
    up_shadow = (hi - price) / pre * 100 if pre else 0      # 上影%
    amp = (hi - lo) / pre * 100 if pre else 0               # 振幅%
    if pct >= 9.8 and (hi - price) / pre * 100 < 0.3:
        s = "涨停封板"
    elif pct >= 9.8:
        s = "触板未封"
    elif pct > 3 and up_shadow > 3:
        s = "冲高回落(长上影)"
    elif pct > 3 and lb >= 1.5:
        s = "放量长阳"
    elif pct > 0:
        s = "温和上涨" if lb >= 0.8 else "缩量上涨"
    else:
        s = "回调"
    return s, round(up_shadow, 1), round(amp, 1)


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
        price = m.fnum(f[3]); shape, ups, amp = kshape(f)
        c = m.fetch_consensus(code, begin, end); fin = m.fetch_financials(code)
        E1, E2 = c["E1"], c["E2"]
        fpe = price / E1 if E1 and E1 > 0 else None
        g = (E2 / E1 - 1) * 100 if E1 and E2 and E1 > 0 else None
        peg = fpe / g if fpe and g and g > 0 else None
        tup = (c["target"] / price - 1) * 100 if c["target"] else None
        r = {"name": name, "code": code[2:], "price": price, "pct": m.fnum(f[32]),
             "shape": shape, "ups": ups, "amp": amp, "lb": m.fnum(f[49]) or 0.0,
             "hs": m.fnum(f[38]), "cov": c["cov"], "g": g, "fpe": fpe, "peg": peg, "tup": tup,
             "rev_yoy": fin["rev_yoy"], "np_yoy": fin["np_yoy"]}
        r["score"] = m.score(r); r["conf"] = m.confidence(c["cov"])
        rows.append(r); time.sleep(0.15)
    rows.sort(key=lambda r: r["score"], reverse=True)

    def sv(v, p=1): return ("%.*f" % (p, v)) if isinstance(v, (int, float)) else "-"
    stamp = quotes.get(pairs[0][1][2:], [""] * 31)[30] if pairs else ""
    head = (f"{'排名':<4}{'股票':<7}{'代码':<7}{'分':>6}{'置信':>5}{'现价':>9}{'涨%':>7}{'K线形态':<14}"
            f"{'上影%':>6}{'振幅%':>6}{'量比':>5}{'PEG':>6}{'增速%':>7}{'营收%':>7}{'净利%':>8}")
    L = [f"16只 当日K线+预期差  收盘: {stamp}", "", head]
    for i, r in enumerate(rows, 1):
        L.append(f"{i:<4}{r['name']:<7}{r['code']:<7}{r['score']:>6}{r['conf']:>5}{r['price']:>9.2f}"
                 f"{sv(r['pct']):>7}{r['shape']:<14}{sv(r['ups']):>6}{sv(r['amp']):>6}{sv(r['lb']):>5}"
                 f"{sv(r['peg'],2):>6}{sv(r['g']):>7}{sv(r['rev_yoy']):>7}{sv(r['np_yoy']):>8}")
    report = "\n".join(L); print(report)
    out = os.path.join(m.HERE, "reports", f"k16_{today.strftime('%Y%m%d')}.txt")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(report + "\n\n免责: 公开数据仅供研究, 不构成投资建议。")
    print("saved", out)


if __name__ == "__main__":
    main()
