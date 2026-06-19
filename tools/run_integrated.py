# -*- coding: utf-8 -*-
"""整合扫描 = 量化预期差(expectation_gap_monitor) × 资金确认(astock_confirm:龙虎榜机构席位+解禁)。
一条命令出整合表。用法:
  python run_integrated.py 厦门钨业 奕东电子 富创精密 ...      # 指定名单
  python run_integrated.py                                    # 用内置默认16只
输出: reports/integrated_YYYYMMDD.txt
机构席位净>0=机构买✅ / <0=机构卖⚠️ / 未上榜=中性。能拦下"涨停但机构出货"类陷阱。
"""
import os, sys, time, datetime as dt
import expectation_gap_monitor as m
import astock_confirm as a

DEFAULT = ["日联科技","奕东电子","厦门钨业","微导纳米","中富电路","世运电路","德科立","江丰电子",
           "富创精密","源杰科技","长川科技","云南锗业","江南新材","海亮股份","赛腾股份","晶丰明源"]


def _load_base():
    """无参时优先读 base_watchlist.txt(每行一名称,#为注释),否则用内置DEFAULT。"""
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "base_watchlist.txt")
    if os.path.isfile(p):
        names = [ln.strip() for ln in open(p, encoding="utf-8") if ln.strip() and not ln.strip().startswith("#")]
        if names:
            return names
    return DEFAULT


def main():
    names = sys.argv[1:] or _load_base()
    today = dt.date.today()
    begin = (today - dt.timedelta(days=120)).isoformat(); end = today.isoformat()
    cache = m.load_cache()
    pairs = [(n, m.resolve_code(n, cache)) for n in names]
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
        row = {"name": name, "code": code[2:], "price": price, "pct": m.fnum(f[32]),
               "lb": m.fnum(f[49]) or 0.0, "cov": c["cov"], "g": g, "fpe": fpe, "peg": peg,
               "tup": tup, "rev_yoy": fin["rev_yoy"], "np_yoy": fin["np_yoy"]}
        row["score"] = m.score(row); row["conf"] = m.confidence(c["cov"])
        # 资金确认层
        dg = a.dragon(code[2:], end); lk = a.lockup(code[2:], end)
        row["lhb"] = dg["count"]; row["inst"] = dg["inst_net"]; row["lhb_net"] = dg["net"]
        row["lockup"] = lk
        rows.append(row); time.sleep(0.1)
    rows.sort(key=lambda r: r["score"], reverse=True)

    def sv(v, p=1): return ("%.*f" % (p, v)) if isinstance(v, (int, float)) else "-"
    def flag(r):
        if not r["lhb"]: return "中性"
        if r["inst"] is None: return "上榜"
        return "机构买✅" if r["inst"] > 0.05 else ("机构卖⚠️" if r["inst"] < -0.05 else "机构平")
    stamp = quotes.get(pairs[0][1][2:], [""] * 31)[30] if pairs and pairs[0][1] else ""
    head = (f"{'#':<3}{'股票':<7}{'代码':<7}{'分':>6}{'置信':>5}{'涨%':>7}{'PEG':>6}{'增速%':>7}{'净利%':>8}"
            f"{'龙虎榜':>7}{'机构净亿':>9}{'解禁':>12}{'资金确认':>9}")
    L = [f"整合扫描(量化×龙虎榜机构席位)  时间: {stamp}  ({len(rows)}只)", "", head]
    for i, r in enumerate(rows, 1):
        lk = r["lockup"]; lkd = lk["date"] if lk else "无"
        lhb = f"{r['lhb']}次" if r["lhb"] else "未上榜"
        inst = f"{r['inst']:+.2f}" if r["inst"] is not None else "-"
        L.append(f"{i:<3}{r['name']:<7}{r['code']:<7}{r['score']:>6}{r['conf']:>5}{sv(r['pct']):>7}"
                 f"{sv(r['peg'],2):>6}{sv(r['g']):>7}{sv(r['np_yoy']):>8}{lhb:>7}{inst:>9}{lkd:>12}{flag(r):>9}")
    report = "\n".join(L)
    out = os.path.join(m.HERE, "reports", f"integrated_{today.strftime('%Y%m%d')}.txt")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(report + "\n\n免责: 公开数据仅供研究, 不构成投资建议。机构席位净仅反映机构专用席位动向。")
    print("saved", out)  # 不直接print表格(含emoji,GBK控制台会报错),内容见UTF-8文件


if __name__ == "__main__":
    main()
