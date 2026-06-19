# -*- coding: utf-8 -*-
"""
功率半导体板块 预期差扫描 (复用 expectation_gap_monitor 的数据/打分逻辑)
输出: reports/power_semi_YYYYMMDD.txt / .csv  (不覆盖默认自选股报告)
"""
import os, json, csv, time, datetime as dt
import expectation_gap_monitor as m

# 功率半导体板块成分 (按名称, 代码自动解析)
WATCHLIST = [
    "斯达半导", "时代电气", "士兰微", "华润微", "新洁能", "东微半导", "扬杰科技",
    "捷捷微电", "宏微科技", "闻泰科技", "三安光电", "天岳先进", "露笑科技", "纳芯微",
    "思瑞浦", "银河微电", "芯导科技", "立昂微", "东尼电子",
]
SECTOR = {
    "斯达半导": "IGBT龙头", "时代电气": "IGBT/牵引", "士兰微": "IDM/IGBT/SiC", "华润微": "IDM/MOSFET",
    "新洁能": "MOSFET/IGBT", "东微半导": "高压MOSFET", "扬杰科技": "二极管/MOS/SiC", "捷捷微电": "晶闸管/MOS",
    "宏微科技": "IGBT模块", "闻泰科技": "Nexperia功率", "三安光电": "SiC衬底/器件", "天岳先进": "SiC衬底",
    "露笑科技": "SiC衬底", "纳芯微": "隔离驱动/车规", "思瑞浦": "模拟/驱动", "银河微电": "功率二极管",
    "芯导科技": "功率/ESD", "立昂微": "硅片/功率", "东尼电子": "SiC",
}


def main():
    cache = m.load_cache()
    today = dt.date.today()
    begin = (today - dt.timedelta(days=120)).isoformat()
    end = today.isoformat()

    pairs = []
    for name in WATCHLIST:
        code = m.resolve_code(name, cache)
        if code:
            pairs.append((name, code))
        else:
            print(f"[跳过] 无法解析: {name}")
    json.dump(cache, open(m.CODE_CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    quotes = m.fetch_quotes([c for _, c in pairs])
    rows = []
    for name, code in pairs:
        f = quotes.get(code[2:])
        if not f:
            print(f"[跳过] 无行情: {name}/{code}")
            continue
        price = m.fnum(f[3])
        c = m.fetch_consensus(code, begin, end)
        fin = m.fetch_financials(code)
        E1, E2 = c["E1"], c["E2"]
        fpe = price / E1 if E1 and E1 > 0 else None
        g = (E2 / E1 - 1) * 100 if E1 and E2 and E1 > 0 else None
        peg = fpe / g if fpe and g and g > 0 else None
        tup = (c["target"] / price - 1) * 100 if c["target"] else None
        row = {
            "name": name, "code": code[2:], "sector": SECTOR.get(name, ""),
            "price": price, "pct": m.fnum(f[32]), "amt": m.fnum(f[37]) / 1e4,
            "hs": m.fnum(f[38]), "lb": m.fnum(f[49]) or 0.0, "nf": m.fetch_flow(code),
            "cov": c["cov"], "E1": E1, "E2": E2, "g": g, "fpe": fpe, "peg": peg,
            "tup": tup, "up_cnt": c["up_cnt"],
            "rev_yoy": fin["rev_yoy"], "np_yoy": fin["np_yoy"],
            "ded_yoy": fin["ded_yoy"], "fin_date": fin["fin_date"],
        }
        row["score"] = m.score(row)
        row["conf"] = m.confidence(c["cov"])
        rows.append(row)
        time.sleep(0.15)

    rows.sort(key=lambda r: r["score"], reverse=True)

    def sv(v, p=2):
        return ("%.*f" % (p, v)) if isinstance(v, (int, float)) else "-"

    stamp = quotes.get(pairs[0][1][2:], [""] * 31)[30] if pairs else ""
    head = (f"{'排名':<4}{'股票':<7}{'代码':<7}{'赛道':<13}{'分':>6}{'置信':>5}"
            f"{'现价':>9}{'涨%':>7}{'额亿':>6}{'量比':>5}"
            f"{'研报':>4}{'预测增速%':>8}{'PEG':>6}{'目标%':>7}{'营收同比%':>8}{'净利同比%':>9}")
    lines = [f"功率半导体 预期差扫描  收盘: {stamp}   标的数: {len(rows)}", "", head]
    for i, r in enumerate(rows, 1):
        lines.append(
            f"{i:<4}{r['name']:<7}{r['code']:<7}{r['sector']:<13}{r['score']:>6}{r['conf']:>5}"
            f"{r['price']:>9.2f}{sv(r['pct']):>7}{sv(r['amt'],1):>6}{sv(r['lb']):>5}"
            f"{r['cov']:>4}{sv(r['g'],1):>8}{sv(r['peg']):>6}{sv(r['tup'],1):>7}"
            f"{sv(r['rev_yoy'],1):>8}{sv(r['np_yoy'],1):>9}")
    report = "\n".join(lines)
    print(report)

    out_dir = os.path.join(m.HERE, "reports")
    os.makedirs(out_dir, exist_ok=True)
    ds = today.strftime("%Y%m%d")
    open(os.path.join(out_dir, f"power_semi_{ds}.txt"), "w", encoding="utf-8").write(
        report + "\n\n免责: 公开数据仅供研究, 不构成投资建议。")
    cols = ["name", "code", "sector", "score", "conf", "price", "pct", "amt", "hs", "lb",
            "nf", "cov", "E1", "E2", "g", "fpe", "peg", "tup", "up_cnt",
            "rev_yoy", "np_yoy", "ded_yoy", "fin_date"]
    with open(os.path.join(out_dir, f"power_semi_{ds}.csv"), "w", newline="", encoding="utf-8-sig") as fp:
        w = csv.DictWriter(fp, fieldnames=["rank"] + cols)
        w.writeheader()
        for i, r in enumerate(rows, 1):
            w.writerow({"rank": i, **{k: r.get(k) for k in cols}})
    print(f"\n已保存: reports/power_semi_{ds}.csv / .txt")


if __name__ == "__main__":
    main()
