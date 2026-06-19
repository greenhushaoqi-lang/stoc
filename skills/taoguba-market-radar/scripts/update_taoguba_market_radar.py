#!/usr/bin/env python3
"""Update the local Taoguba market radar skill memory."""

from __future__ import annotations

import argparse
import datetime as dt
import email.utils
import hashlib
import html
import json
import re
import textwrap
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ACCOUNTS = {
    "3485724": {
        "name": "快乐糖糖",
        "blog_url": "https://www.tgb.cn/blog/3485724",
        "mobile_url": "https://m.tgb.cn/blog/3485724",
    }
}

DEFAULT_LIMIT_PER_ACCOUNT = 20

THEME_KEYWORDS = [
    "AI",
    "硅基",
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
    "玻璃基板",
    "铜箔",
    "电子布",
    "液冷",
    "六氟化钨",
    "电子气体",
    "钨",
    "锗",
    "稀土",
    "黄金",
    "机器人",
    "电池",
    "固态电池",
    "军工",
    "券商",
    "并购",
    "重组",
    "涨价",
    "供需",
    "出口管制",
    "政策",
    "美股",
    "英伟达",
    "台积电",
    "三星",
    "海力士",
    "美光",
]

KNOWN_STOCK_NAMES = [
    "中船特气",
    "中际旭创",
    "长信科技",
    "江丰电子",
    "逸豪新材",
    "太辰光",
    "富信科技",
    "美迪凯",
    "炬光科技",
    "光华科技",
    "圣泉集团",
    "中巨芯",
    "兴福电子",
    "欧莱新材",
    "方邦股份",
    "沃格光电",
    "生益科技",
    "神工股份",
    "联瑞新材",
    "昀冢科技",
    "凌玮科技",
    "同宇新材",
    "天承科技",
    "悦安新材",
    "彩客新能源",
    "索辰科技",
    "晶丰明源",
    "德科立",
    "源杰科技",
    "富创精密",
    "长川科技",
    "云南锗业",
    "三环集团",
    "洁美科技",
]


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def http_get(url: str, headers: dict[str, str] | None = None, timeout: int = 20) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            ),
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "https://www.tgb.cn/",
            **(headers or {}),
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def parse_time(value: Any) -> str:
    if not value:
        return now_utc().isoformat()
    if isinstance(value, (int, float)):
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


def stable_id(account_id: str, url: str, text: str) -> str:
    seed = f"{account_id}|{url}|{text}".encode("utf-8", errors="ignore")
    return hashlib.sha256(seed).hexdigest()[:20]


def clean_text(value: str) -> str:
    value = re.sub(r"<script\b.*?</script>", " ", value or "", flags=re.S | re.I)
    value = re.sub(r"<style\b.*?</style>", " ", value, flags=re.S | re.I)
    value = re.sub(r"<br\s*/?>", "\n", value, flags=re.I)
    value = re.sub(r"</p>|</div>|</li>", "\n", value, flags=re.I)
    value = html.unescape(re.sub(r"<[^>]+>", " ", value))
    value = value.replace("\xa0", " ")
    value = re.sub(r"[ \t\r\f\v]+", " ", value)
    value = re.sub(r"\n\s+", "\n", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def extract_linked_stock_names(html_text: str) -> list[str]:
    names = set()
    for value in re.findall(r"name=['\"]T([^'\"]+)['\"]", html_text or ""):
        value = clean_text(value)
        if 2 <= len(value) <= 12:
            names.add(value)
    return sorted(names)


def absolute_url(url: str) -> str:
    if url.startswith("http"):
        return url
    if url.startswith("//"):
        return "https:" + url
    if url.startswith("/"):
        return "https://m.tgb.cn" + url
    return urllib.parse.urljoin("https://m.tgb.cn/", url)


def extract_title(html_text: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html_text, re.S | re.I)
    if not m:
        return ""
    title = clean_text(m.group(1))
    return re.sub(r"_快乐糖糖_淘股吧|_淘股吧|_博客_淘股吧|_快乐糖糖的微博客观点_掌上淘股吧", "", title).strip()


def fetch_article(url: str, account_id: str) -> dict[str, Any]:
    raw = http_get(url, timeout=20).decode("utf-8", errors="ignore")
    title = extract_title(raw)
    linked_stock_names = extract_linked_stock_names(raw)
    release = ""
    m = re.search(r'<meta\s+property=["\']og:release_date["\']\s+content=["\'](.*?)["\']', raw, re.S | re.I)
    if m:
        release = m.group(1).strip()
    subject = ""
    m = re.search(r'<span[^>]+id=["\']ztgioMsg["\'][^>]+subject=["\'](.*?)["\']', raw, re.S | re.I)
    if m:
        subject = html.unescape(m.group(1)).strip()
    if subject and not title:
        title = subject
    body = ""
    m = re.search(r'<div\s+class=["\']tzitem_text\s+hideText["\'][^>]*>(.*?)<div\s+class=["\']isover["\']', raw, re.S | re.I)
    if m:
        body = clean_text(m.group(1))
    if not body:
        m = re.search(r'<meta\s+http-equiv=["\']description["\']\s+content=["\'](.*?)["\']', raw, re.S | re.I)
        if m:
            body = clean_text(m.group(1))
    return {
        "id": stable_id(account_id, url, title + body[:500]),
        "account_id": account_id,
        "account_name": ACCOUNTS[account_id]["name"],
        "source": "taoguba-mobile-article",
        "url": url,
        "created_at": parse_time(release),
        "collected_at": now_utc().isoformat(),
        "title": title,
        "summary": textwrap.shorten(body, width=260, placeholder="...") if body else "",
        "text": body,
        "stock_names": linked_stock_names,
        "metrics": {},
    }


def parse_blog_articles(html_text: str, account_id: str, limit: int) -> list[dict[str, Any]]:
    links = re.findall(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html_text, flags=re.S | re.I)
    grouped: dict[str, dict[str, str]] = {}
    order: list[str] = []
    for href, raw_text in links:
        if not re.search(r"^/a/[A-Za-z0-9]+", href):
            continue
        url = absolute_url(href)
        text = clean_text(raw_text)
        if not text or text.startswith("'+") or text.startswith("' str"):
            continue
        if url not in grouped:
            grouped[url] = {"title": "", "summary": ""}
            order.append(url)
        if text.startswith("[摘要]") or text.startswith("【摘要】"):
            grouped[url]["summary"] = text.replace("[摘要]", "").replace("【摘要】", "").strip()
        elif not grouped[url]["title"]:
            grouped[url]["title"] = text

    rows: list[dict[str, Any]] = []
    for url in order[:limit]:
        title = grouped[url]["title"]
        summary = grouped[url]["summary"]
        try:
            article = fetch_article(url, account_id)
            if title and not article.get("title"):
                article["title"] = title
            if summary and not article.get("summary"):
                article["summary"] = summary
            rows.append(article)
        except Exception as exc:
            rows.append(
                {
                    "id": stable_id(account_id, url, title + summary),
                    "account_id": account_id,
                    "account_name": ACCOUNTS[account_id]["name"],
                    "source": f"taoguba-blog-list-only:{type(exc).__name__}: {exc}",
                    "url": url,
                    "created_at": now_utc().isoformat(),
                    "collected_at": now_utc().isoformat(),
                    "title": title,
                    "summary": summary,
                    "text": summary,
                    "metrics": {},
                }
            )
    return rows


def load_import_file(path: Path) -> list[dict[str, Any]]:
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".jsonl":
        rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
    else:
        obj = json.loads(raw)
        rows = obj if isinstance(obj, list) else obj.get("data", obj.get("items", []))
    out = []
    for row in rows:
        account_id = str(row.get("account_id") or row.get("user_id") or "3485724").strip()
        if account_id not in ACCOUNTS:
            continue
        text = str(row.get("text") or row.get("content") or row.get("summary") or "")
        title = str(row.get("title") or row.get("subject") or "")
        url = str(row.get("url") or ACCOUNTS[account_id]["blog_url"])
        out.append(
            {
                "id": str(row.get("id") or stable_id(account_id, url, title + text)),
                "account_id": account_id,
                "account_name": ACCOUNTS[account_id]["name"],
                "source": f"import:{path.name}",
                "url": url,
                "created_at": parse_time(row.get("created_at") or row.get("date") or row.get("published")),
                "collected_at": now_utc().isoformat(),
                "title": title,
                "summary": str(row.get("summary") or textwrap.shorten(text, width=260, placeholder="...")),
                "text": text,
                "metrics": row.get("metrics") or {},
            }
        )
    return out


def dedupe(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for row in sorted(rows, key=lambda x: (x.get("created_at", ""), x.get("url", "")), reverse=True):
        key = f"{row.get('account_id')}:{row.get('url') or row.get('id')}"
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def fetch_all(limit: int) -> tuple[list[dict[str, Any]], list[str]]:
    all_rows: list[dict[str, Any]] = []
    status: list[str] = []
    for account_id, account in ACCOUNTS.items():
        try:
            raw = http_get(account["mobile_url"], timeout=20).decode("utf-8", errors="ignore")
            rows = parse_blog_articles(raw, account_id, limit)
            if rows:
                status.append(f"{account_id}: ok {account['mobile_url']} rows={len(rows)}")
            else:
                status.append(f"{account_id}: no article links parsed from {account['mobile_url']}")
            all_rows.extend(rows)
        except Exception as exc:
            status.append(f"{account_id}: {type(exc).__name__}: {exc}")
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
    text = "\n".join(f"{row.get('title', '')}\n{row.get('text', '')}\n{row.get('summary', '')}" for row in rows)
    stock_codes = sorted(set(re.findall(r"(?<!\d)(?:00|30|60|68|83|87)\d{4}(?!\d)", text)))
    stock_name_map = fetch_stock_names(stock_codes)
    stock_names = [stock_name_map.get(code, code) for code in stock_codes]
    linked_names = sorted(
        {
            str(name).strip()
            for row in rows
            for name in (row.get("stock_names") or [])
            if str(name).strip()
        }
    )
    # Common Chinese stock-name shape, used only as weak extraction.
    weak_candidates = set(re.findall(r"[\u4e00-\u9fff]{2,8}(?:科技|股份|电子|光电|精密|新材|材料|电路|特气|芯|集团)", text))
    noisy_fragments = (
        "就是",
        "各种",
        "其它",
        "其实",
        "最近",
        "记住",
        "说的",
        "对应",
        "首先",
        "起来",
        "没有",
        "下午",
        "主要",
        "最好",
        "上游",
        "材料材料",
        "全球",
        "每次",
        "会是",
        "但它",
        "就算",
        "半导体材料",
        "金属材料",
        "气体半导体材料",
        "设备铜箔电子",
        "那光材料",
        "和中船",
        "想中船",
        "还未上市",
    )
    known_names = [name for name in KNOWN_STOCK_NAMES if name in text]
    weak_names = sorted(
        name
        for name in weak_candidates
        if 2 <= len(name) <= 8
        and not any(fragment in name for fragment in noisy_fragments)
        and (name in KNOWN_STOCK_NAMES or name.endswith(("科技", "股份", "电子", "光电", "精密", "新材", "电路", "特气", "集团")))
    )
    lower = text.lower()
    keywords = [kw for kw in THEME_KEYWORDS if kw.lower() in lower]
    return {
        "stock_codes": stock_codes,
        "stock_names": sorted(set(stock_names + linked_names + known_names + weak_names))[:80],
        "keywords": keywords,
    }


def build_latest_markdown(rows: list[dict[str, Any]], source_status: list[str]) -> str:
    stamp = now_utc().astimezone().isoformat(timespec="seconds")
    by_account: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_account[row.get("account_id", "")].append(row)

    global_terms = extract_terms(rows)
    keyword_counter = Counter()
    for account_rows in by_account.values():
        for kw in extract_terms(account_rows)["keywords"]:
            keyword_counter[kw] += 1

    lines = [
        "# Taoguba Market Radar - Latest Learned State",
        "",
        f"Last update: {stamp}",
        f"Status: updated with {len(rows)} archived articles across {len(by_account)} accounts" if rows else "Status: no articles archived; source access needs attention",
        "",
        "## Tracked Accounts",
        "",
    ]
    for account_id, account in ACCOUNTS.items():
        lines.append(f"- `{account['name']}` ({account_id}): {account['blog_url']}")

    lines += ["", "## Current Themes", ""]
    if rows:
        for key in ("stock_names", "keywords"):
            values = global_terms.get(key, [])
            lines.append(f"- {key}: {', '.join(values[:80]) if values else 'none detected'}")
        consensus = [kw for kw, count in keyword_counter.items() if count >= 1]
        lines.append(f"- repeated/active keywords: {', '.join(consensus) if consensus else 'none detected'}")
    else:
        lines.append("- No readable articles were fetched in this run.")

    lines += ["", "## Account Deltas", ""]
    for account_id, account in ACCOUNTS.items():
        account_rows = by_account.get(account_id, [])
        terms = extract_terms(account_rows)
        lines.append(f"### {account['name']} ({account_id})")
        lines.append("")
        lines.append(f"- articles archived today: {len(account_rows)}")
        lines.append(f"- keywords: {', '.join(terms['keywords'][:40]) if terms['keywords'] else 'none detected'}")
        lines.append(f"- stock_names: {', '.join(terms['stock_names'][:40]) if terms['stock_names'] else 'none detected'}")
        if account_rows:
            lines.append("- recent index:")
            for row in account_rows[:8]:
                summary = row.get("summary") or textwrap.shorten(row.get("text", ""), width=180, placeholder="...")
                summary = textwrap.shorten(summary.replace("\n", " "), width=180, placeholder="...")
                lines.append(f"  - {row.get('created_at', '')} | {row.get('title', '')} | {row.get('url', '')} | {summary}")
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
        "- Compare with prior files under `references/daily/` to identify what changed.",
        "- Treat profit claims, targets, and emotional language as weak social signals.",
        "- Map repeated stock names and concepts to A-share market data before ranking ideas.",
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
    parser = argparse.ArgumentParser(description="Update tracked Taoguba accounts for market narrative research.")
    parser.add_argument("--skill-dir", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT_PER_ACCOUNT)
    parser.add_argument("--import-json", help="Import a local JSON file containing articles.")
    parser.add_argument("--import-jsonl", help="Import a local JSONL file containing articles.")
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
