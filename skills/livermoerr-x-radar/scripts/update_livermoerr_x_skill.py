#!/usr/bin/env python3
"""Update the local @livermoerr X radar skill memory.

The updater prefers the official X API when X_BEARER_TOKEN or
TWITTER_BEARER_TOKEN is available. Without credentials, it tries public RSS
frontends that expose Twitter/X user feeds. It can also import local JSON or
JSONL exports.
"""

from __future__ import annotations

import argparse
import datetime as dt
import email.utils
import hashlib
import html
import json
import os
import re
import sys
import textwrap
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


HANDLE = "livermoerr"
PROFILE_URL = "https://x.com/livermoerr?s=21"
DEFAULT_LIMIT = 30


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def http_get(url: str, headers: dict[str, str] | None = None, timeout: int = 20) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 livermoerr-x-radar/1.0",
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


def stable_id(text: str, created_at: str | None = None) -> str:
    seed = f"{created_at or ''}|{text}".encode("utf-8", errors="ignore")
    return hashlib.sha256(seed).hexdigest()[:20]


def normalize_item(item: dict[str, Any], source: str) -> dict[str, Any]:
    text = str(item.get("text") or item.get("content") or item.get("full_text") or "").strip()
    created_at = parse_time(str(item.get("created_at") or item.get("date") or item.get("published") or ""))
    post_id = str(item.get("id") or item.get("post_id") or stable_id(text, created_at))
    url = item.get("url") or item.get("link") or f"https://x.com/{HANDLE}/status/{post_id}"
    metrics = item.get("public_metrics") or item.get("metrics") or {}
    return {
        "id": post_id,
        "handle": HANDLE,
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
    return [normalize_item(row, f"import:{path.name}") for row in rows]


def fetch_x_api(limit: int) -> tuple[list[dict[str, Any]], str]:
    token = os.getenv("X_BEARER_TOKEN") or os.getenv("TWITTER_BEARER_TOKEN")
    if not token:
        return [], "missing X_BEARER_TOKEN/TWITTER_BEARER_TOKEN"

    headers = {"Authorization": f"Bearer {token}"}
    user_url = f"https://api.twitter.com/2/users/by/username/{HANDLE}"
    user = json.loads(http_get(user_url, headers=headers).decode("utf-8"))
    user_id = user.get("data", {}).get("id")
    if not user_id:
        return [], f"could not resolve @{HANDLE}: {user}"

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
                    "url": f"https://x.com/{HANDLE}/status/{item.get('id')}",
                    "public_metrics": item.get("public_metrics", {}),
                },
                "x-api-v2",
            )
        )
    return rows, "ok"


def fetch_rss_frontends(limit: int) -> tuple[list[dict[str, Any]], list[str]]:
    urls = [
        f"https://rsshub.app/twitter/user/{HANDLE}",
        f"https://nitter.net/{HANDLE}/rss",
        f"https://xcancel.com/{HANDLE}/rss",
        f"https://nitter.poast.org/{HANDLE}/rss",
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
                text = html.unescape(re.sub(r"<[^>]+>", " ", desc or title))
                text = re.sub(r"\s+", " ", text).strip()
                rows.append(
                    normalize_item(
                        {"text": text, "published": published, "link": link},
                        f"rss:{url}",
                    )
                )
            if rows:
                return rows, [f"ok: {url}"]
            errors.append(f"empty: {url}")
        except Exception as exc:
            errors.append(f"{url}: {type(exc).__name__}: {exc}")
    return [], errors


def dedupe(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for row in sorted(rows, key=lambda x: x.get("created_at", ""), reverse=True):
        key = row.get("id") or stable_id(row.get("text", ""), row.get("created_at"))
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def extract_terms(rows: list[dict[str, Any]]) -> dict[str, list[str]]:
    text = "\n".join(row.get("text", "") for row in rows)
    cashtags = sorted(set(re.findall(r"\$[A-Za-z][A-Za-z0-9._-]{0,12}", text)), key=str.upper)
    hashtags = sorted(set(re.findall(r"#[\w\u4e00-\u9fff-]+", text)), key=str.upper)
    cn_keywords = [
        "AI",
        "semiconductor",
        "chip",
        "GPU",
        "memory",
        "copper",
        "gold",
        "rate",
        "Fed",
        "tariff",
        "China",
        "Japan",
        "Korea",
        "A-share",
        "liquidity",
        "earnings",
        "guidance",
    ]
    lower = text.lower()
    keywords = [kw for kw in cn_keywords if kw.lower() in lower]
    return {"cashtags": cashtags, "hashtags": hashtags, "keywords": keywords}


def build_latest_markdown(rows: list[dict[str, Any]], source_status: list[str]) -> str:
    stamp = now_utc().astimezone().isoformat(timespec="seconds")
    terms = extract_terms(rows)
    recent = rows[:10]
    if rows:
        status = f"updated with {len(rows)} archived posts"
    else:
        status = "no posts archived; source access needs attention"

    lines = [
        "# Livermoerr X Radar - Latest Learned State",
        "",
        f"Last update: {stamp}",
        f"Profile: {PROFILE_URL}",
        f"Status: {status}",
        "",
        "## Current Themes",
        "",
    ]
    if rows:
        for key, values in terms.items():
            value = ", ".join(values[:30]) if values else "none detected"
            lines.append(f"- {key}: {value}")
    else:
        lines.append("- No readable posts were fetched in this run.")
    lines += ["", "## Recent Posts Index", ""]
    if recent:
        for row in recent:
            text = textwrap.shorten(row.get("text", "").replace("\n", " "), width=180, placeholder="...")
            lines.append(f"- {row.get('created_at', '')} | {row.get('url', '')} | {text}")
    else:
        lines.append("- Empty.")
    lines += ["", "## Source Health", ""]
    for item in source_status:
        lines.append(f"- {item}")
    lines += [
        "",
        "## Next Analysis Instructions",
        "",
        "- Treat this file as compact memory, not as a source of verified facts.",
        "- Verify market claims with price, filings, official announcements, and news sources.",
        "- Compare with prior files under `references/daily/` to identify what changed.",
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
    parser = argparse.ArgumentParser(description="Update @livermoerr X radar skill memory.")
    parser.add_argument("--skill-dir", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--import-json", help="Import a local JSON file containing posts.")
    parser.add_argument("--import-jsonl", help="Import a local JSONL file containing posts.")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    rows: list[dict[str, Any]] = []
    source_status: list[str] = []

    if args.import_json or args.import_jsonl:
        path = Path(args.import_json or args.import_jsonl).resolve()
        rows = load_import_file(path)
        source_status.append(f"import ok: {path}")
    else:
        api_rows, api_status = fetch_x_api(args.limit)
        source_status.append(f"official X API: {api_status}")
        rows.extend(api_rows)
        if not rows:
            rss_rows, rss_status = fetch_rss_frontends(args.limit)
            source_status.extend(rss_status)
            rows.extend(rss_rows)

    rows = dedupe(rows)
    write_outputs(skill_dir, rows, source_status)
    print(json.dumps({"skill_dir": str(skill_dir), "rows": len(rows), "source_status": source_status}, ensure_ascii=False, indent=2))
    return 0 if rows else 2


if __name__ == "__main__":
    raise SystemExit(main())
