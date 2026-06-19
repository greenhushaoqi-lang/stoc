# -*- coding: utf-8 -*-
"""资金确认层 — 基于 a-stock-data 技能逻辑(东财datacenter),给个股补:
  ① 主力近5日净流入(亿)  ② 龙虎榜(近30日上榜次数+最近净额+机构席位净额)  ③ 未来90天解禁(日期/比例)
零依赖(urllib),内置东财限流。供每日早盘报告对Top10做资金面二次确认。
用法: python astock_confirm.py 海亮股份 厦门钨业 富创精密 ...
"""
import urllib.request as u, urllib.parse as up, json, time, sys, datetime as dt
import expectation_gap_monitor as m

DC = "https://datacenter-web.eastmoney.com/api/data/v1/get"
_last = [0.0]
def _throttle():
    w = 1.1 - (time.time() - _last[0])
    if w > 0: time.sleep(w)
    _last[0] = time.time()

def _dc(report, filt, cols="ALL", size=50, sortc="", sortt="-1"):
    _throttle()
    qs = up.urlencode({"reportName": report, "columns": cols, "filter": filt,
                       "pageNumber": "1", "pageSize": str(size), "sortColumns": sortc,
                       "sortTypes": sortt, "source": "WEB", "client": "WEB"})
    req = u.Request(DC + "?" + qs, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://data.eastmoney.com/"})
    try:
        d = json.loads(u.urlopen(req, timeout=15).read().decode("utf-8", "ignore"))
        return ((d.get("result") or {}).get("data")) or []
    except Exception:
        return []

def dragon(code6, date, look_back=30):
    """龙虎榜: 近look_back日上榜次数 + 最近一次净额(亿) + 机构席位净额(亿)。"""
    start = (dt.date.fromisoformat(date) - dt.timedelta(days=look_back)).isoformat()
    recs = _dc("RPT_DAILYBILLBOARD_DETAILSNEW",
               f"(TRADE_DATE>='{start}')(TRADE_DATE<='{date}')(SECURITY_CODE=\"{code6}\")",
               sortc="TRADE_DATE", sortt="-1")
    if not recs:
        return {"count": 0, "latest": None, "net": None, "inst_net": None, "reason": None}
    latest = str(recs[0].get("TRADE_DATE", ""))[:10]
    net = round((recs[0].get("BILLBOARD_NET_AMT") or 0) / 1e8, 2)
    inst = 0.0
    for rpt, sgn in [("RPT_BILLBOARD_DAILYDETAILSBUY", 1), ("RPT_BILLBOARD_DAILYDETAILSSELL", -1)]:
        for row in _dc(rpt, f"(TRADE_DATE='{latest}')(SECURITY_CODE=\"{code6}\")", size=10):
            if str(row.get("OPERATEDEPT_CODE", "")) == "0":  # 机构专用席位
                inst += sgn * ((row.get("BUY") or 0) if sgn > 0 else (row.get("SELL") or 0))
    return {"count": len(recs), "latest": latest, "net": net,
            "inst_net": round(inst / 1e8, 2), "reason": (recs[0].get("EXPLANATION", "") or "")[:18]}

def lockup(code6, date, days=90):
    """未来days天最近一次解禁: 日期 + 占总股本比例%。"""
    end = (dt.date.fromisoformat(date) + dt.timedelta(days=days)).isoformat()
    rows = _dc("RPT_LIFT_STAGE",
               f"(SECURITY_CODE=\"{code6}\")(FREE_DATE>='{date}')(FREE_DATE<='{end}')",
               sortc="FREE_DATE", sortt="1")
    if not rows:
        return None
    r = rows[0]
    return {"date": str(r.get("FREE_DATE", ""))[:10], "ratio": round(float(r.get("FREE_RATIO") or 0), 1)}

def flow5(code_full):
    """主力近5日净流入合计(亿)。code_full 形如 sh600549。"""
    secid = ("1." if code_full.startswith("sh") else "0.") + code_full[2:]
    url = (f"https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?secid={secid}"
           f"&fields1=f1,f2,f3,f7&fields2=f51,f52&klt=101&lmt=5")
    try:
        kl = json.loads(u.urlopen(u.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=10).read().decode())["data"]["klines"]
        return round(sum(float(x.split(",")[1]) for x in kl) / 1e8, 2)
    except Exception:
        return None

def confirm(name, date=None):
    date = date or dt.date.today().isoformat()
    code = m.resolve_code(name, m.load_cache())
    if not code:
        return {"name": name, "err": "代码未解析"}
    c6 = code[2:]
    return {"name": name, "code": c6, "flow5": flow5(code),
            "dragon": dragon(c6, date), "lockup": lockup(c6, date)}


def main():
    names = sys.argv[1:]
    if not names:
        print("用法: python astock_confirm.py 海亮股份 厦门钨业 ..."); return
    print(f"{'股票':<7}{'主力5日亿':>9}{'龙虎榜30日':>10}{'最近净亿':>9}{'机构净亿':>9}{'最近解禁':>12}{'解禁%':>7}")
    for n in names:
        r = confirm(n)
        if r.get("err"):
            print(f"{n:<7} {r['err']}"); continue
        d = r["dragon"]; lk = r["lockup"]
        f5 = f"{r['flow5']:+.2f}" if r["flow5"] is not None else "-"
        dgn = f"{d['count']}次" if d["count"] else "未上榜"
        net = f"{d['net']:+.2f}" if d["net"] is not None else "-"
        inet = f"{d['inst_net']:+.2f}" if d["inst_net"] is not None else "-"
        lkd = lk["date"] if lk else "无"
        lkr = f"{lk['ratio']:.1f}" if lk else "-"
        print(f"{n:<7}{f5:>9}{dgn:>10}{net:>9}{inet:>9}{lkd:>12}{lkr:>7}")


if __name__ == "__main__":
    main()
