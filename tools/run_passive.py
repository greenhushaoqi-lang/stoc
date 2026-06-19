# -*- coding: utf-8 -*-
"""被动元件板块 预期差扫描 (复用 expectation_gap_monitor)。
输出 reports/passive_components_YYYYMMDD.txt / .csv"""
import os, csv, time, datetime as dt
import expectation_gap_monitor as m

WATCHLIST = [
    "三环集团", "风华高科", "火炬电子", "宏达电子", "鸿远电子",      # MLCC/电容
    "顺络电子", "麦捷科技", "铂科新材",                              # 电感
    "法拉电子", "艾华集团", "江海股份",                              # 薄膜/铝电解/超容
    "振华科技",                                                     # 军工被动平台
    "国瓷材料", "洁美科技",                                         # 上游材料
]
SECTOR = {
    "三环集团": "MLCC龙头", "风华高科": "MLCC/电阻", "火炬电子": "MLCC/钽电容",
    "宏达电子": "军工钽/MLCC", "鸿远电子": "军工MLCC", "顺络电子": "电感龙头",
    "麦捷科技": "电感/滤波器", "铂科新材": "金属软磁电感", "法拉电子": "薄膜电容",
    "艾华集团": "铝电解电容", "江海股份": "铝电解/超容", "振华科技": "军工被动平台",
    "国瓷材料": "MLCC材料(上游)", "洁美科技": "载带/离型膜(上游)",
}


def main():
    cache = m.load_cache()
    today = dt.date.today()
    begin = (today - dt.timedelta(days=120)).isoformat(); end = today.isoformat()
    pairs = [(n, m.resolve_code(n, cache)) for n in WATCHLIST]
    import json; json.dump(cache, open(m.CODE_CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    quotes = m.fetch_quotes([c for _, c in pairs if c])
    rows = []
    for name, code in pairs:
        f = quotes.get(code[2:]) if code else None
        if not f:
            print(f"[跳过] 无行情: {name}/{code}"); continue
        price = m.fnum(f[3])
        c = m.fetch_consensus(code, begin, end); fin = m.fetch_financials(code)
        E1, E2 = c["E1"], c["E2"]
        fpe = price / E1 if E1 and E1 > 0 else None
        g = (E2 / E1 - 1) * 100 if E1 and E2 and E1 > 0 else None
        peg = fpe / g if fpe and g and g > 0 else None
        tup = (c["target"] / price - 1) * 100 if c["target"] else None
        r = {"name": name, "code": code[2:], "sector": SECTOR.get(name, ""), "price": price,
             "pct": m.fnum(f[32]), "amt": m.fnum(f[37]) / 1e4, "hs": m.fnum(f[38]),
             "lb": m.fnum(f[49]) or 0.0, "nf": m.fetch_flow(code), "cov": c["cov"],
             "E1": E1, "E2": E2, "g": g, "fpe": fpe, "peg": peg, "tup": tup,
             "up_cnt": c["up_cnt"], "rev_yoy": fin["rev_yoy"], "np_yoy": fin["np_yoy"],
             "ded_yoy": fin["ded_yoy"], "fin_date": fin["fin_date"]}
        r["score"] = m.score(r); r["conf"] = m.confidence(c["cov"])
        rows.append(r); time.sleep(0.15)
    rows.sort(key=lambda r: r["score"], reverse=True)

    def sv(v, p=1): return ("%.*f" % (p, v)) if isinstance(v, (int, float)) else "-"
    stamp = quotes.get(pairs[0][1][2:], [""] * 31)[30] if pairs else ""
    head = (f"{'排名':<4}{'股票':<7}{'代码':<7}{'赛道':<14}{'分':>6}{'置信':>5}"
            f"{'现价':>9}{'涨%':>7}{'额亿':>6}{'量比':>5}{'研报':>4}{'预测增速%':>8}{'PEG':>6}{'目标%':>7}{'营收同比%':>8}{'净利同比%':>9}")
    L = [f"被动元件 预期差扫描  收盘: {stamp}   标的数: {len(rows)}", "", head]
    for i, r in enumerate(rows, 1):
        L.append(f"{i:<4}{r['name']:<7}{r['code']:<7}{r['sector']:<14}{r['score']:>6}{r['conf']:>5}"
                 f"{r['price']:>9.2f}{sv(r['pct']):>7}{sv(r['amt']):>6}{sv(r['lb']):>5}{r['cov']:>4}"
                 f"{sv(r['g']):>8}{sv(r['peg'],2):>6}{sv(r['tup']):>7}{sv(r['rev_yoy']):>8}{sv(r['np_yoy']):>9}")
    report = "\n".join(L); print(report)
    out_dir = os.path.join(m.HERE, "reports"); os.makedirs(out_dir, exist_ok=True)
    ds = today.strftime("%Y%m%d")
    open(os.path.join(out_dir, f"passive_components_{ds}.txt"), "w", encoding="utf-8").write(
        report + "\n\n免责: 公开数据仅供研究, 不构成投资建议。")
    cols = ["name", "code", "sector", "score", "conf", "price", "pct", "amt", "hs", "lb",
            "nf", "cov", "E1", "E2", "g", "fpe", "peg", "tup", "up_cnt", "rev_yoy", "np_yoy", "ded_yoy", "fin_date"]
    with open(os.path.join(out_dir, f"passive_components_{ds}.csv"), "w", newline="", encoding="utf-8-sig") as fp:
        w = csv.DictWriter(fp, fieldnames=["rank"] + cols); w.writeheader()
        for i, r in enumerate(rows, 1):
            w.writerow({"rank": i, **{k: r.get(k) for k in cols}})
    print(f"\n已保存: reports/passive_components_{ds}.csv / .txt")


if __name__ == "__main__":
    main()
