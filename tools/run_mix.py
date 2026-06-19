# -*- coding: utf-8 -*-
"""AI算力材料混合篮子 预期差扫描(仅A股口径)。HK另行定性处理。
输出 reports/mix_YYYYMMDD.txt/.csv"""
import os, csv, time, datetime as dt
import expectation_gap_monitor as m

WATCHLIST = [
    "厦门钨业", "光华科技", "圣泉集团", "铜陵有色", "富创精密",
    "晶丰明源", "三环集团", "洁美科技", "鸿远电子", "德科立",
]
CONCEPT = {
    "厦门钨业": "钨/稀土/磁材", "光华科技": "PCB化学品/电池材料", "圣泉集团": "电子树脂(CCL上游)/硬碳负极",
    "铜陵有色": "铜/铜箔(铜冠母公司)", "富创精密": "半导体设备零部件", "晶丰明源": "AI电源管理芯片",
    "三环集团": "MLCC龙头", "洁美科技": "MLCC载带/离型膜", "鸿远电子": "军工MLCC", "德科立": "光模块/CPO",
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
        r = {"name": name, "code": code[2:], "concept": CONCEPT.get(name, ""), "price": price,
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
    head = (f"{'排名':<4}{'股票':<7}{'代码':<7}{'概念':<18}{'分':>6}{'置信':>5}"
            f"{'现价':>9}{'涨%':>7}{'额亿':>6}{'量比':>5}{'研报':>4}{'增速%':>7}{'PEG':>6}{'目标%':>7}{'营收同比':>8}{'净利同比':>9}")
    L = [f"AI材料混合篮子 预期差扫描  收盘: {stamp}   标的数: {len(rows)}", "", head]
    for i, r in enumerate(rows, 1):
        L.append(f"{i:<4}{r['name']:<7}{r['code']:<7}{r['concept']:<18}{r['score']:>6}{r['conf']:>5}"
                 f"{r['price']:>9.2f}{sv(r['pct']):>7}{sv(r['amt']):>6}{sv(r['lb']):>5}{r['cov']:>4}"
                 f"{sv(r['g']):>7}{sv(r['peg'],2):>6}{sv(r['tup']):>7}{sv(r['rev_yoy']):>8}{sv(r['np_yoy']):>9}")
    report = "\n".join(L); print(report)
    out_dir = os.path.join(m.HERE, "reports"); os.makedirs(out_dir, exist_ok=True)
    ds = today.strftime("%Y%m%d")
    open(os.path.join(out_dir, f"mix_{ds}.txt"), "w", encoding="utf-8").write(report + "\n\n免责: 公开数据仅供研究, 不构成投资建议。")
    cols = ["name", "code", "concept", "score", "conf", "price", "pct", "amt", "hs", "lb",
            "nf", "cov", "E1", "E2", "g", "fpe", "peg", "tup", "up_cnt", "rev_yoy", "np_yoy", "ded_yoy", "fin_date"]
    with open(os.path.join(out_dir, f"mix_{ds}.csv"), "w", newline="", encoding="utf-8-sig") as fp:
        w = csv.DictWriter(fp, fieldnames=["rank"] + cols); w.writeheader()
        for i, r in enumerate(rows, 1):
            w.writerow({"rank": i, **{k: r.get(k) for k in cols}})
    print(f"\n已保存: reports/mix_{ds}.csv / .txt")


if __name__ == "__main__":
    main()
