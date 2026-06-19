# -*- coding: utf-8 -*-
"""
预期差日度监控 (Expectation-Gap Daily Monitor)
------------------------------------------------
数据源: 腾讯行情(qt.gtimg.cn, 不封IP) + 东财资金流/机构一致预期(eastmoney)
功能:   每日收盘后拉取自选股的 量价 + 主力资金 + 机构一致预期(EPS/目标价/评级),
        计算 前瞻PE / 预测增速 / PEG / 目标价空间, 合成"预期差分"并排序输出。

用法:   python expectation_gap_monitor.py
        - 只需在下面 WATCHLIST 里按"名称"维护, 代码自动解析(缓存到 codes.json)
        - 结果存到 ./reports/expectation_gap_YYYYMMDD.csv 和 .txt

免责:   公开数据, 仅供研究, 不构成投资建议。机构覆盖为0的标的无EPS/PEG, 仅供参考。
"""
import urllib.request as u, urllib.parse as up, json, statistics as st, os, time, csv, datetime as dt

# ============ 1. 自选股 (只填名称即可) ============
WATCHLIST = [
    "赛伍技术","方邦股份","泰晶科技","中富电路","世运电路","德科立","江丰电子","铜冠铜箔",
    "德福科技","帝尔激光","富创精密","源杰科技","长川科技","云南锗业","江南新材","海亮股份",
    "赛腾股份","晶丰明源",
]
# 可选: 赛道标签(仅用于展示, 不影响打分)
SECTOR = {
    "世运电路":"高端PCB","中富电路":"高端PCB","江南新材":"PCB铜基材料","方邦股份":"FCCL/屏蔽膜",
    "铜冠铜箔":"铜箔","德福科技":"铜箔","海亮股份":"铜箔/铜加工","源杰科技":"CPO光芯片","德科立":"光模块",
    "江丰电子":"靶材","富创精密":"半导体零件","长川科技":"测试设备","晶丰明源":"AI电源芯片",
    "帝尔激光":"激光设备","泰晶科技":"石英晶振","赛腾股份":"消费电子设备","云南锗业":"锗/红外","赛伍技术":"光伏背板",
}

HDRS = {"User-Agent": "Mozilla/5.0", "Referer": "https://data.eastmoney.com/"}
HERE = os.path.dirname(os.path.abspath(__file__))
CODE_CACHE = os.path.join(HERE, "codes.json")


def _get(url, timeout=12):
    return u.urlopen(u.Request(url, headers=HDRS), timeout=timeout).read()


def fnum(x):
    try:
        return float(x)
    except Exception:
        return None


# ============ 2. 名称 -> 代码 (带缓存) ============
def load_cache():
    if os.path.exists(CODE_CACHE):
        try:
            return json.load(open(CODE_CACHE, encoding="utf-8"))
        except Exception:
            return {}
    return {}


def resolve_code(name, cache):
    if name in cache:
        return cache[name]
    url = ("https://searchapi.eastmoney.com/api/suggest/get?input=" + up.quote(name) +
           "&type=14&token=D43BF722C8E33BDC906FB84D85E326E8&count=5")
    try:
        d = json.loads(_get(url).decode())
        for it in d.get("QuotationCodeTable", {}).get("Data", []) or []:
            mkt = it.get("MktNum")           # 1=沪 0=深
            code = it.get("Code")
            if mkt in ("1", "0") and code and code.isdigit() and len(code) == 6:
                full = ("sh" if mkt == "1" else "sz") + code
                cache[name] = full
                return full
    except Exception as e:
        print(f"[警告] 解析代码失败 {name}: {e}")
    return None


# ============ 3. 行情 (腾讯, 批量) ============
def fetch_quotes(codes):
    raw = _get("http://qt.gtimg.cn/q=" + ",".join(codes)).decode("gbk")
    q = {}
    for ln in raw.split(";"):
        if "~" in ln and len(ln.split('"')) > 1:
            f = ln.split('"')[1].split("~")
            if len(f) > 40:
                q[f[2]] = f
    return q


# ============ 4. 主力净流入 (东财日线资金流) ============
def fetch_flow(code):
    secid = ("1." if code.startswith("sh") else "0.") + code[2:]
    url = (f"https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?secid={secid}"
           f"&fields1=f1,f2,f3,f7&fields2=f51,f52&klt=101&lmt=1")
    try:
        kl = json.loads(_get(url, 8).decode())["data"]["klines"]
        return float(kl[-1].split(",")[1]) / 1e8      # 亿元
    except Exception:
        return None


# ============ 5. 机构一致预期 (东财研报) ============
def fetch_consensus(code, begin, end):
    url = (f"https://reportapi.eastmoney.com/report/list?pageSize=60&beginTime={begin}&endTime={end}"
           f"&qType=0&code={code[2:]}&pageNo=1&p=1&pageNumber=1")
    try:
        rep = json.loads(_get(url).decode("utf-8", "ignore")).get("data", []) or []
    except Exception:
        rep = []
    e1 = [fnum(r.get("predictThisYearEps")) for r in rep]; e1 = [x for x in e1 if x]
    e2 = [fnum(r.get("predictNextYearEps")) for r in rep]; e2 = [x for x in e2 if x]
    tg = [fnum(r.get("indvAimPriceT")) for r in rep]; tg = [x for x in tg if x and x > 0]
    # 评级上调家数
    up_cnt = sum(1 for r in rep if str(r.get("ratingChange")) in ("1", "2"))
    return {
        "cov": len(rep),
        "E1": st.median(e1) if e1 else None,
        "E2": st.median(e2) if e2 else None,
        "target": st.mean(tg) if tg else None,
        "tn": len(tg),
        "up_cnt": up_cnt,
    }


# ============ 5b. 实际财报增速 (营收/净利同比, 给无覆盖标的兜底) ============
def fetch_financials(code):
    """返回最新报告期的 营收同比% / 归母净利同比% / 扣非净利同比% / 报告期。"""
    secu = code[2:] + "." + code[:2].upper()      # 603920 + .SH
    url = ("https://datacenter-web.eastmoney.com/api/data/v1/get?"
           "sortColumns=REPORT_DATE&sortTypes=-1&pageSize=1&pageNumber=1"
           "&reportName=RPT_F10_FINANCE_MAINFINADATA&columns=ALL&source=HSF10&client=PC"
           "&filter=" + up.quote(f'(SECUCODE="{secu}")'))
    try:
        d = json.loads(_get(url).decode("utf-8", "ignore"))
        r = (d.get("result") or {}).get("data") or []
        if not r:
            return {"rev_yoy": None, "np_yoy": None, "ded_yoy": None, "fin_date": None}
        r = r[0]
        rd = (r.get("REPORT_DATE") or "")[:10]
        return {
            "rev_yoy": fnum(r.get("TOTALOPERATEREVETZ")),
            "np_yoy": fnum(r.get("PARENTNETPROFITTZ")),
            "ded_yoy": fnum(r.get("KCFJCXSYJLRTZ")),
            "fin_date": rd,
        }
    except Exception:
        return {"rev_yoy": None, "np_yoy": None, "ded_yoy": None, "fin_date": None}


# ============ 6. 预期差打分 (透明, 各分项可见) ============
def score(row):
    """合成预期差分。两条腿:
       (A)一致预期腿(有机构覆盖): 低PEG/高预测增速/目标价有空间;
       (B)实际财报腿(始终计算, 给无覆盖标的兜底): 归母净利/营收同比增速。
       叠加资金确认, 扣高位透支(涨停/超高PE/已过目标价)。"""
    peg, g, fpe, tup, pct, lb, cov, rev, npr = (row[k] for k in
        ("peg", "g", "fpe", "tup", "pct", "lb", "cov", "rev_yoy", "np_yoy"))
    s = 0.0
    # --- A. 一致预期腿 ---
    if peg is not None:
        s += max(0.0, min(40.0, (2.0 - peg) * 20.0))   # PEG 0->+40, 1->+20, 2->0
    if g is not None:
        s += max(0.0, min(20.0, g / 80.0 * 20.0))      # 预测增速 封顶+20
    if tup is not None:
        s += max(-15.0, min(15.0, tup / 50.0 * 15.0))  # 目标价空间 ±15
    # --- B. 实际财报腿 (始终计) ---
    if npr is not None:
        s += max(-10.0, min(20.0, npr / 100.0 * 20.0)) # 归母净利同比 +100%->+20, 负值最多-10
    if rev is not None:
        s += max(-5.0, min(10.0, rev / 50.0 * 10.0))   # 营收同比 +50%->+10
    # 无覆盖标的: 给实际财报腿加权(×1.4), 避免只吃惩罚被压到垫底
    if cov < 2 and (npr is not None or rev is not None):
        bonus = 0.0
        if npr is not None:
            bonus += max(-10.0, min(20.0, npr / 100.0 * 20.0)) * 0.4
        if rev is not None:
            bonus += max(-5.0, min(10.0, rev / 50.0 * 10.0)) * 0.4
        s += bonus
    # --- 资金确认 ---
    if lb:
        s += min(10.0, lb / 3.0 * 10.0)
    if pct is not None and 0 < pct < 9.8:
        s += min(5.0, pct / 8.0 * 5.0)
    # --- 透支惩罚 ---
    if pct is not None and pct >= 9.8:
        s -= 6.0
    if fpe is not None and fpe > 200:
        s -= 10.0
    if tup is not None and tup < 0:
        s -= 10.0
    return round(s, 1)


def confidence(cov):
    return "高" if cov >= 5 else ("中" if cov >= 2 else ("低" if cov == 1 else "无覆盖"))


# ============ 7. 主流程 ============
def main():
    cache = load_cache()
    today = dt.date.today()
    begin = (today - dt.timedelta(days=120)).isoformat()
    end = today.isoformat()

    pairs = []                         # (name, code)
    for name in WATCHLIST:
        code = resolve_code(name, cache)
        if code:
            pairs.append((name, code))
        else:
            print(f"[跳过] 无法解析: {name}")
    json.dump(cache, open(CODE_CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    quotes = fetch_quotes([c for _, c in pairs])
    rows = []
    for name, code in pairs:
        f = quotes.get(code[2:])
        if not f:
            print(f"[跳过] 无行情: {name}/{code}")
            continue
        price = fnum(f[3])
        c = fetch_consensus(code, begin, end)
        fin = fetch_financials(code)
        E1, E2 = c["E1"], c["E2"]
        fpe = price / E1 if E1 and E1 > 0 else None
        g = (E2 / E1 - 1) * 100 if E1 and E2 and E1 > 0 else None
        peg = fpe / g if fpe and g and g > 0 else None
        tup = (c["target"] / price - 1) * 100 if c["target"] else None
        row = {
            "name": name, "code": code[2:], "sector": SECTOR.get(name, ""),
            "price": price, "pct": fnum(f[32]), "amt": fnum(f[37]) / 1e4,
            "hs": fnum(f[38]), "lb": fnum(f[49]) or 0.0, "nf": fetch_flow(code),
            "cov": c["cov"], "E1": E1, "E2": E2, "g": g, "fpe": fpe, "peg": peg,
            "tup": tup, "up_cnt": c["up_cnt"],
            "rev_yoy": fin["rev_yoy"], "np_yoy": fin["np_yoy"],
            "ded_yoy": fin["ded_yoy"], "fin_date": fin["fin_date"],
        }
        row["score"] = score(row)
        row["conf"] = confidence(c["cov"])
        rows.append(row)
        time.sleep(0.15)               # 礼貌限速

    rows.sort(key=lambda r: r["score"], reverse=True)

    # ---- 输出 ----
    def sv(v, p=2):
        return ("%.*f" % (p, v)) if isinstance(v, (int, float)) else "-"

    stamp = quotes.get(pairs[0][1][2:], [""] * 31)[30] if pairs else ""
    head = (f"{'排名':<4}{'股票':<7}{'代码':<7}{'赛道':<10}{'分':>6}{'置信':>5}"
            f"{'现价':>9}{'涨%':>7}{'额亿':>6}{'量比':>5}"
            f"{'研报':>4}{'预测增速%':>8}{'PEG':>6}{'目标%':>7}{'营收同比%':>8}{'净利同比%':>8}")
    lines = [f"预期差日度监控  数据时间(收盘): {stamp}   标的数: {len(rows)}", "", head]
    for i, r in enumerate(rows, 1):
        lines.append(
            f"{i:<4}{r['name']:<7}{r['code']:<7}{r['sector']:<10}{r['score']:>6}{r['conf']:>5}"
            f"{r['price']:>9.2f}{sv(r['pct']):>7}{sv(r['amt'],1):>6}{sv(r['lb']):>5}"
            f"{r['cov']:>4}{sv(r['g'],1):>8}{sv(r['peg']):>6}{sv(r['tup'],1):>7}"
            f"{sv(r['rev_yoy'],1):>8}{sv(r['np_yoy'],1):>8}")
    report = "\n".join(lines)
    print(report)

    # ---- 落盘 ----
    out_dir = os.path.join(HERE, "reports")
    os.makedirs(out_dir, exist_ok=True)
    ds = today.strftime("%Y%m%d")
    with open(os.path.join(out_dir, f"expectation_gap_{ds}.txt"), "w", encoding="utf-8") as fp:
        fp.write(report + "\n\n免责: 公开数据仅供研究, 不构成投资建议。")
    cols = ["name", "code", "sector", "score", "conf", "price", "pct", "amt", "hs", "lb",
            "nf", "cov", "E1", "E2", "g", "fpe", "peg", "tup", "up_cnt",
            "rev_yoy", "np_yoy", "ded_yoy", "fin_date"]
    with open(os.path.join(out_dir, f"expectation_gap_{ds}.csv"), "w", newline="", encoding="utf-8-sig") as fp:
        w = csv.DictWriter(fp, fieldnames=["rank"] + cols)
        w.writeheader()
        for i, r in enumerate(rows, 1):
            w.writerow({"rank": i, **{k: r.get(k) for k in cols}})
    print(f"\n已保存: reports/expectation_gap_{ds}.csv / .txt")


if __name__ == "__main__":
    main()
