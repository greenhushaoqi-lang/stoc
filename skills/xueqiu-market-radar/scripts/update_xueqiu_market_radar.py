#!/usr/bin/env python3
"""Update the local Xueqiu market radar skill memory."""

from __future__ import annotations

import argparse
import datetime as dt
import email.utils
import hashlib
import html
import json
import os
import re
import textwrap
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Any


ACCOUNTS = {
    "5124430882": "https://xueqiu.com/u/5124430882",
    "5672579962": "https://xueqiu.com/u/5672579962",
    "1034624503": "https://xueqiu.com/u/1034624503",
    "4086512744": "https://xueqiu.com/u/4086512744",
    "7251377368": "https://xueqiu.com/u/7251377368",
    "1301600236": "https://xueqiu.com/u/1301600236",
    "4168622038": "https://xueqiu.com/u/4168622038",
}

DEFAULT_LIMIT_PER_ACCOUNT = 25

THEME_KEYWORDS = [
    "AI",
    "GPU",
    "算力",
    "半导体",
    "芯片",
    "存储",
    "HBM",
    "DRAM",
    "CPO",
    "光模块",
    "光芯片",
    "PCB",
    "CCL",
    "MLCC",
    "铜箔",
    "钨",
    "锗",
    "稀土",
    "黄金",
    "机器人",
    "人形机器人",
    "电池",
    "固态电池",
    "军工",
    "券商",
    "并购",
    "重组",
    "涨价",
    "供需",
    "出口管制",
    "关税",
    "政策",
    "美股",
    "日股",
    "韩股",
    "英伟达",
    "AMD",
    "台积电",
    "三星",
    "海力士",
    "美光",
]


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def default_headers(extra: dict[str, str] | None = None) -> dict[str, str]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "https://xueqiu.com/",
    }
    cookie = os.getenv("XUEQIU_COOKIE", "").strip()
    token = os.getenv("XQ_A_TOKEN", "").strip()
    if cookie:
        headers["Cookie"] = cookie
    elif token:
        headers["Cookie"] = f"xq_a_token={token}"
    if extra:
        headers.update(extra)
    return headers


def http_get(url: str, headers: dict[str, str] | None = None, timeout: int = 20, opener=None) -> bytes:
    req = urllib.request.Request(url, headers=default_headers(headers))
    if opener:
        with opener.open(req, timeout=timeout) as resp:
            return resp.read()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def parse_time(value: Any) -> str:
    if not value:
        return now_utc().isoformat()
    if isinstance(value, (int, float)):
        # Xueqiu commonly uses millisecond timestamps.
        if value > 10_000_000_000:
            value = value / 1000
        return dt.datetime.fromtimestamp(value, tz=dt.timezone.utc).isoformat()
    value = str(value).strip()
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).isoformat()
    except ValueError:
        pass
    try:
        return email.utils.parsedate_to_datetime(value).isoformat()
    except Exception:
        return value


def stable_id(uid: str, text: str, created_at: str | None = None) -> str:
    seed = f"{uid}|{created_at or ''}|{text}".encode("utf-8", errors="ignore")
    return hashlib.sha256(seed).hexdigest()[:20]


def clean_text(value: str) -> str:
    value = html.unescape(re.sub(r"<[^>]+>", " ", value or ""))
    return re.sub(r"\s+", " ", value).strip()


def normalize_item(item: dict[str, Any], uid: str, source: str) -> dict[str, Any]:
    text = clean_text(str(item.get("text") or item.get("description") or item.get("title") or item.get("content") or ""))
    created_at = parse_time(item.get("created_at") or item.get("timeBefore") or item.get("created") or item.get("published"))
    post_id = str(item.get("id") or item.get("status_id") or stable_id(uid, text, created_at))
    user = item.get("user") if isinstance(item.get("user"), dict) else {}
    screen_name = str(user.get("screen_name") or item.get("screen_name") or "")
    url = item.get("target") or item.get("url") or item.get("link") or f"https://xueqiu.com/{uid}/{post_id}"
    if isinstance(url, str) and url.startswith("/"):
        url = f"https://xueqiu.com{url}"
    return {
        "id": post_id,
        "uid": uid,
        "screen_name": screen_name,
        "profile_url": ACCOUNTS.get(uid, f"https://xueqiu.com/u/{uid}"),
        "source": source,
        "url": str(url),
        "created_at": created_at,
        "collected_at": now_utc().isoformat(),
        "text": text,
        "metrics": {
            "reply_count": item.get("reply_count"),
            "retweet_count": item.get("retweet_count"),
            "fav_count": item.get("fav_count"),
            "view_count": item.get("view_count"),
        },
    }


def load_import_file(path: Path) -> list[dict[str, Any]]:
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".jsonl":
        rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
    else:
        obj = json.loads(raw)
        rows = obj if isinstance(obj, list) else obj.get("data", obj.get("items", []))
    out = []
    for row in rows:
        uid = str(row.get("uid") or row.get("user_id") or row.get("account") or "").strip()
        if uid not in ACCOUNTS:
            continue
        out.append(normalize_item(row, uid, f"import:{path.name}"))
    return out


def build_opener_with_cookie() -> urllib.request.OpenerDirector:
    cookie_jar = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
    if not (os.getenv("XUEQIU_COOKIE") or os.getenv("XQ_A_TOKEN")):
        try:
            http_get("https://xueqiu.com/", opener=opener, timeout=15)
        except Exception:
            pass
    return opener


def fetch_xueqiu_api(uid: str, limit: int, opener) -> tuple[list[dict[str, Any]], str]:
    endpoints = [
        "https://xueqiu.com/statuses/original/timeline.json",
        "https://xueqiu.com/v4/statuses/user_timeline.json",
        "https://xueqiu.com/statuses/user_timeline.json",
    ]
    errors: list[str] = []
    for endpoint in endpoints:
        params = urllib.parse.urlencode({"user_id": uid, "page": 1, "count": max(5, min(limit, 50))})
        url = f"{endpoint}?{params}"
        try:
            raw = http_get(url, opener=opener, timeout=20).decode("utf-8", errors="replace")
            if raw.lstrip().startswith("<"):
                if "aliyun_waf" in raw or "_waf" in raw:
                    errors.append(f"{endpoint}: blocked by Xueqiu/Aliyun WAF; provide XUEQIU_COOKIE")
                else:
                    errors.append(f"{endpoint}: returned HTML instead of JSON")
                continue
            data = json.loads(raw)
            items = data.get("list") or data.get("statuses") or data.get("items") or data.get("data") or []
            if isinstance(items, dict):
                items = items.get("list") or items.get("items") or []
            rows = [normalize_item(item, uid, f"xueqiu-api:{endpoint}") for item in items[:limit] if isinstance(item, dict)]
            if rows:
                return rows, f"{uid}: ok {endpoint}"
            errors.append(f"{endpoint}: empty JSON")
        except Exception as exc:
            errors.append(f"{endpoint}: {type(exc).__name__}: {exc}")
    return [], f"{uid}: " + " | ".join(errors[:3])


def fetch_rsshub(uid: str, limit: int) -> tuple[list[dict[str, Any]], list[str]]:
    routes = [
        f"https://rsshub.app/xueqiu/user/{uid}/2",
        f"https://rsshub.app/xueqiu/user/{uid}",
        f"https://rsshub.app/xueqiu/favorite/{uid}",
    ]
    errors: list[str] = []
    for url in routes:
        try:
            content = http_get(url, timeout=20).decode("utf-8", errors="replace")
            root = ET.fromstring(content)
            items = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")
            rows: list[dict[str, Any]] = []
            for item in items[:limit]:
                title = item.findtext("title") or item.findtext("{http://www.w3.org/2005/Atom}title") or ""
                desc = item.findtext("description") or item.findtext("{http://www.w3.org/2005/Atom}summary") or ""
                link = item.findtext("link") or ""
                if not link:
                    link_node = item.find("{http://www.w3.org/2005/Atom}link")
                    link = link_node.attrib.get("href", "") if link_node is not None else ""
                published = (
                    item.findtext("pubDate")
                    or item.findtext("published")
                    or item.findtext("{http://www.w3.org/2005/Atom}published")
                    or item.findtext("{http://www.w3.org/2005/Atom}updated")
                )
                text = clean_text(desc or title)
                if text:
                    rows.append(normalize_item({"text": text, "published": published, "link": link}, uid, f"rsshub:{url}"))
            if rows:
                return rows, [f"{uid}: ok {url}"]
            errors.append(f"{uid}: empty {url}")
        except Exception as exc:
            errors.append(f"{uid}: {url}: {type(exc).__name__}: {exc}")
    return [], errors


def dedupe(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for row in sorted(rows, key=lambda x: (x.get("created_at", ""), x.get("uid", "")), reverse=True):
        key = f"{row.get('uid')}:{row.get('id') or stable_id(row.get('uid', ''), row.get('text', ''), row.get('created_at'))}"
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def fetch_all(limit: int) -> tuple[list[dict[str, Any]], list[str]]:
    opener = build_opener_with_cookie()
    all_rows: list[dict[str, Any]] = []
    status: list[str] = []
    for uid in ACCOUNTS:
        rows, api_status = fetch_xueqiu_api(uid, limit, opener)
        status.append(api_status)
        if not rows:
            rss_rows, rss_status = fetch_rsshub(uid, limit)
            status.extend(rss_status)
            rows.extend(rss_rows)
        all_rows.extend(rows)
    return dedupe(all_rows), status


def fetch_stock_names(codes: list[str]) -> dict[str, str]:
    unique_codes = sorted({code for code in codes if re.fullmatch(r"\d{6}", code)})
    if not unique_codes:
        return {}
    symbols = [
        f"{'sh' if code.startswith(('5', '6', '9')) else 'bj' if code.startswith(('4', '8')) else 'sz'}{code}"
        for code in unique_codes
    ]
    url = f"https://qt.gtimg.cn/q={','.join(symbols)}"
    try:
        text = http_get(url, headers={"Referer": "https://gu.qq.com/"}, timeout=10).decode("gbk", errors="ignore")
    except Exception:
        return {}
    names: dict[str, str] = {}
    for code, name in re.findall(r'v_[a-z]{2}(\d{6})="[^~]*~([^~]+)~', text):
        if name.strip():
            names[code] = name.strip()
    return names


def extract_terms(rows: list[dict[str, Any]]) -> dict[str, Any]:
    text = "\n".join(row.get("text", "") for row in rows)
    cashtags = sorted(set(re.findall(r"\$[A-Za-z][A-Za-z0-9._-]{0,12}", text)), key=str.upper)
    hashtags = sorted(set(re.findall(r"#[\w\u4e00-\u9fff-]+", text)), key=str.upper)
    stock_codes = sorted(set(re.findall(r"(?<!\d)(?:00|30|60|68|83|87)\d{4}(?!\d)", text)))
    stock_name_map = fetch_stock_names(stock_codes)
    stock_names = [stock_name_map.get(code, code) for code in stock_codes]
    lower = text.lower()
    keywords = [kw for kw in THEME_KEYWORDS if kw.lower() in lower]
    return {
        "cashtags": cashtags,
        "hashtags": hashtags,
        "stock_codes": stock_codes,
        "stock_names": stock_names,
        "keywords": keywords,
    }


def build_latest_markdown(rows: list[dict[str, Any]], source_status: list[str]) -> str:
    stamp = now_utc().astimezone().isoformat(timespec="seconds")
    by_uid: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_uid[row.get("uid", "")].append(row)

    global_terms = extract_terms(rows)
    keyword_counter = Counter()
    for uid_rows in by_uid.values():
        for kw in extract_terms(uid_rows)["keywords"]:
            keyword_counter[kw] += 1

    lines = [
        "# Xueqiu Market Radar - Latest Learned State",
        "",
        f"Last update: {stamp}",
        f"Status: updated with {len(rows)} archived posts across {len(by_uid)} accounts" if rows else "Status: no posts archived; source access needs attention",
        "",
        "## Tracked Accounts",
        "",
    ]
    for uid, url in ACCOUNTS.items():
        lines.append(f"- `{uid}`: {url}")

    lines += ["", "## Current Cross-Account Themes", ""]
    if rows:
        for key in ("cashtags", "hashtags", "stock_names", "keywords"):
            values = global_terms.get(key, [])
            lines.append(f"- {key}: {', '.join(values[:60]) if values else 'none detected'}")
        consensus = [kw for kw, count in keyword_counter.items() if count >= 2]
        lines.append(f"- consensus keywords across 2+ accounts: {', '.join(consensus) if consensus else 'none detected'}")
    else:
        lines.append("- No readable posts were fetched in this run.")

    lines += ["", "## Account Deltas", ""]
    for uid in ACCOUNTS:
        uid_rows = by_uid.get(uid, [])
        terms = extract_terms(uid_rows)
        name = next((row.get("screen_name") for row in uid_rows if row.get("screen_name")), "")
        title = f"### {name} ({uid})" if name else f"### {uid}"
        lines.append(title)
        lines.append("")
        lines.append(f"- posts archived today: {len(uid_rows)}")
        lines.append(f"- keywords: {', '.join(terms['keywords'][:30]) if terms['keywords'] else 'none detected'}")
        lines.append(f"- stock_names: {', '.join(terms['stock_names'][:30]) if terms['stock_names'] else 'none detected'}")
        recent = uid_rows[:5]
        if recent:
            lines.append("- recent index:")
            for row in recent:
                text = textwrap.shorten(row.get("text", "").replace("\n", " "), width=180, placeholder="...")
                lines.append(f"  - {row.get('created_at', '')} | {row.get('url', '')} | {text}")
        else:
            lines.append("- recent index: empty or source unavailable")
        lines.append("")

    lines += ["## Source Health", ""]
    for item in source_status:
        lines.append(f"- {item}")

    lines += [
        "",
        "## Next Analysis Instructions",
        "",
        "- Treat this file as compact memory, not as verified evidence.",
        "- Verify market claims with price, filings, official announcements, and credible news sources.",
        "- If source health shows WAF or cookie errors, ask for `XUEQIU_COOKIE` or use `--import-jsonl`.",
        "- Compare with prior files under `references/daily/` to identify what changed.",
        "- Give more weight to themes repeated across multiple accounts, but still check whether posts are copying the same original source.",
    ]
    return "\n".join(lines) + "\n"


def write_outputs(skill_dir: Path, rows: list[dict[str, Any]], source_status: list[str]) -> None:
    refs = skill_dir / "references"
    daily = refs / "daily"
    daily.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    daily_path = daily / f"{today}.jsonl"
    existing: list[dict[str, Any]] = []
    if daily_path.exists():
        existing = [json.loads(line) for line in daily_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    merged = dedupe(existing + rows)
    daily_path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in merged) + ("\n" if merged else ""),
        encoding="utf-8",
    )
    (refs / "latest.md").write_text(build_latest_markdown(merged, source_status), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Update tracked Xueqiu accounts for market narrative research.")
    parser.add_argument("--skill-dir", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT_PER_ACCOUNT)
    parser.add_argument("--import-json", help="Import a local JSON file containing posts with uid/user_id fields.")
    parser.add_argument("--import-jsonl", help="Import a local JSONL file containing posts with uid/user_id fields.")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    if args.import_json or args.import_jsonl:
        path = Path(args.import_json or args.import_jsonl).resolve()
        rows = load_import_file(path)
        source_status = [f"import ok: {path}"]
    else:
        rows, source_status = fetch_all(args.limit)

    write_outputs(skill_dir, rows, source_status)
    print(json.dumps({"skill_dir": str(skill_dir), "rows": len(rows), "source_status": source_status}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
