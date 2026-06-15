#!/usr/bin/env python3
"""Update the local six-account X market radar skill memory."""

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
from pathlib import Path
from typing import Any


ACCOUNTS = {
    "duangu888": "https://x.com/duangu888?s=21",
    "xiaoyeyeeey": "https://x.com/xiaoyeyeeey?s=21",
    "cnfinancewatch": "https://x.com/cnfinancewatch?s=21",
    "kugo_a10": "https://x.com/kugo_a10?s=21",
    "bianmian96608": "https://x.com/bianmian96608?s=21",
    "oldk_gillis": "https://x.com/oldk_gillis?s=21",
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
    "CPO",
    "光模块",
    "PCB",
    "铜",
    "铝",
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
]


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def http_get(url: str, headers: dict[str, str] | None = None, timeout: int = 20) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 six-x-market-radar/1.0",
            **(headers or {}),
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def parse_time(value: str | None) -> str:
    if not value:
        return now_utc().isoformat()
    value = value.strip()
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).isoformat()
    except ValueError:
        pass
    try:
        return email.utils.parsedate_to_datetime(value).isoformat()
    except Exception:
        return value


def stable_id(handle: str, text: str, created_at: str | None = None) -> str:
    seed = f"{handle}|{created_at or ''}|{text}".encode("utf-8", errors="ignore")
    return hashlib.sha256(seed).hexdigest()[:20]


def clean_rss_text(value: str) -> str:
    value = html.unescape(re.sub(r"<[^>]+>", " ", value or ""))
    return re.sub(r"\s+", " ", value).strip()


def normalize_item(item: dict[str, Any], handle: str, source: str) -> dict[str, Any]:
    text = str(item.get("text") or item.get("content") or item.get("full_text") or "").strip()
    created_at = parse_time(str(item.get("created_at") or item.get("date") or item.get("published") or ""))
    post_id = str(item.get("id") or item.get("post_id") or stable_id(handle, text, created_at))
    url = item.get("url") or item.get("link") or f"https://x.com/{handle}/status/{post_id}"
    metrics = item.get("public_metrics") or item.get("metrics") or {}
    return {
        "id": post_id,
        "handle": handle,
        "profile_url": ACCOUNTS.get(handle, f"https://x.com/{handle}"),
        "source": source,
        "url": str(url),
        "created_at": created_at,
        "collected_at": now_utc().isoformat(),
        "text": text,
        "metrics": metrics,
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
        handle = str(row.get("handle") or row.get("username") or row.get("account") or "").lstrip("@")
        if handle not in ACCOUNTS:
            continue
        out.append(normalize_item(row, handle, f"import:{path.name}"))
    return out


def fetch_x_api_handle(handle: str, limit: int) -> tuple[list[dict[str, Any]], str]:
    token = os.getenv("X_BEARER_TOKEN") or os.getenv("TWITTER_BEARER_TOKEN")
    if not token:
        return [], "missing X_BEARER_TOKEN/TWITTER_BEARER_TOKEN"

    headers = {"Authorization": f"Bearer {token}"}
    user_url = f"https://api.twitter.com/2/users/by/username/{handle}"
    user = json.loads(http_get(user_url, headers=headers).decode("utf-8"))
    user_id = user.get("data", {}).get("id")
    if not user_id:
        return [], f"could not resolve @{handle}: {user}"

    params = urllib.parse.urlencode(
        {
            "max_results": max(5, min(limit, 100)),
            "tweet.fields": "created_at,public_metrics,entities,lang,referenced_tweets",
            "exclude": "retweets",
        }
    )
    timeline_url = f"https://api.twitter.com/2/users/{user_id}/tweets?{params}"
    data = json.loads(http_get(timeline_url, headers=headers).decode("utf-8"))
    rows = []
    for item in data.get("data", []) or []:
        rows.append(
            normalize_item(
                {
                    "id": item.get("id"),
                    "text": item.get("text", ""),
                    "created_at": item.get("created_at"),
                    "url": f"https://x.com/{handle}/status/{item.get('id')}",
                    "public_metrics": item.get("public_metrics", {}),
                },
                handle,
                "x-api-v2",
            )
        )
    return rows, "ok"


def fetch_rss_handle(handle: str, limit: int) -> tuple[list[dict[str, Any]], list[str]]:
    urls = [
        f"https://rsshub.app/twitter/user/{handle}",
        f"https://nitter.net/{handle}/rss",
        f"https://xcancel.com/{handle}/rss",
        f"https://nitter.poast.org/{handle}/rss",
    ]
    errors: list[str] = []
    for url in urls:
        try:
            content = http_get(url).decode("utf-8", errors="replace")
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
                text = clean_rss_text(desc or title)
                rows.append(normalize_item({"text": text, "published": published, "link": link}, handle, f"rss:{url}"))
            if rows:
                return rows, [f"{handle}: ok {url}"]
            errors.append(f"{handle}: empty {url}")
        except Exception as exc:
            errors.append(f"{handle}: {url}: {type(exc).__name__}: {exc}")
    return [], errors


def dedupe(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for row in sorted(rows, key=lambda x: (x.get("created_at", ""), x.get("handle", "")), reverse=True):
        key = f"{row.get('handle')}:{row.get('id') or stable_id(row.get('handle', ''), row.get('text', ''), row.get('created_at'))}"
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def fetch_all(limit: int) -> tuple[list[dict[str, Any]], list[str]]:
    all_rows: list[dict[str, Any]] = []
    status: list[str] = []
    token_present = bool(os.getenv("X_BEARER_TOKEN") or os.getenv("TWITTER_BEARER_TOKEN"))
    for handle in ACCOUNTS:
        rows: list[dict[str, Any]] = []
        if token_present:
            api_rows, api_status = fetch_x_api_handle(handle, limit)
            status.append(f"{handle}: official X API {api_status}")
            rows.extend(api_rows)
        else:
            status.append(f"{handle}: official X API missing token")
        if not rows:
            rss_rows, rss_status = fetch_rss_handle(handle, limit)
            status.extend(rss_status)
            rows.extend(rss_rows)
        all_rows.extend(rows)
    return dedupe(all_rows), status


def extract_terms(rows: list[dict[str, Any]]) -> dict[str, Any]:
    text = "\n".join(row.get("text", "") for row in rows)
    cashtags = sorted(set(re.findall(r"\$[A-Za-z][A-Za-z0-9._-]{0,12}", text)), key=str.upper)
    hashtags = sorted(set(re.findall(r"#[\w\u4e00-\u9fff-]+", text)), key=str.upper)
    stock_codes = sorted(set(re.findall(r"(?<!\d)(?:00|30|60|68|83|87)\d{4}(?!\d)", text)))
    lower = text.lower()
    keywords = [kw for kw in THEME_KEYWORDS if kw.lower() in lower]
    return {
        "cashtags": cashtags,
        "hashtags": hashtags,
        "stock_codes": stock_codes,
        "keywords": keywords,
    }


def build_latest_markdown(rows: list[dict[str, Any]], source_status: list[str]) -> str:
    stamp = now_utc().astimezone().isoformat(timespec="seconds")
    by_handle: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_handle[row.get("handle", "")].append(row)

    global_terms = extract_terms(rows)
    keyword_counter = Counter()
    for handle_rows in by_handle.values():
        for kw in extract_terms(handle_rows)["keywords"]:
            keyword_counter[kw] += 1

    lines = [
        "# Six X Market Radar - Latest Learned State",
        "",
        f"Last update: {stamp}",
        f"Status: updated with {len(rows)} archived posts across {len(by_handle)} accounts" if rows else "Status: no posts archived; source access needs attention",
        "",
        "## Tracked Accounts",
        "",
    ]
    for handle, url in ACCOUNTS.items():
        lines.append(f"- `{handle}`: {url}")

    lines += ["", "## Current Cross-Account Themes", ""]
    if rows:
        for key in ("cashtags", "hashtags", "stock_codes", "keywords"):
            values = global_terms.get(key, [])
            lines.append(f"- {key}: {', '.join(values[:40]) if values else 'none detected'}")
        consensus = [kw for kw, count in keyword_counter.items() if count >= 2]
        lines.append(f"- consensus keywords across 2+ accounts: {', '.join(consensus) if consensus else 'none detected'}")
    else:
        lines.append("- No readable posts were fetched in this run.")

    lines += ["", "## Account Deltas", ""]
    for handle in ACCOUNTS:
        handle_rows = by_handle.get(handle, [])
        terms = extract_terms(handle_rows)
        lines.append(f"### @{handle}")
        lines.append("")
        lines.append(f"- posts archived today: {len(handle_rows)}")
        lines.append(f"- keywords: {', '.join(terms['keywords'][:20]) if terms['keywords'] else 'none detected'}")
        lines.append(f"- stock_codes: {', '.join(terms['stock_codes'][:20]) if terms['stock_codes'] else 'none detected'}")
        recent = handle_rows[:5]
        if recent:
            lines.append("- recent index:")
            for row in recent:
                text = textwrap.shorten(row.get("text", "").replace("\n", " "), width=170, placeholder="...")
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
    parser = argparse.ArgumentParser(description="Update six tracked X accounts for market narrative research.")
    parser.add_argument("--skill-dir", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT_PER_ACCOUNT)
    parser.add_argument("--import-json", help="Import a local JSON file containing posts with handle fields.")
    parser.add_argument("--import-jsonl", help="Import a local JSONL file containing posts with handle fields.")
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
    return 0 if rows else 2


if __name__ == "__main__":
    raise SystemExit(main())
