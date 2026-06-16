#!/usr/bin/env python3
"""Update public JoinQuant/Guorn/ThinkTrader radar memory."""

from __future__ import annotations

import argparse
import datetime as dt
import html
from html.parser import HTMLParser
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


SOURCES = [
    {
        "name": "joinquant",
        "label": "JoinQuant / 聚宽",
        "base": "https://www.joinquant.com/",
        "seeds": [
            "https://www.joinquant.com/",
            "https://www.joinquant.com/community",
            "https://www.joinquant.com/help/api/help",
            "https://www.joinquant.com/sitemap.xml",
        ],
        "search_queries": [
            "site:joinquant.com 聚宽 量化 策略 股票",
            "site:joinquant.com/community 聚宽 策略 回测",
        ],
    },
    {
        "name": "guorn",
        "label": "Guorn / 果仁网",
        "base": "https://guorn.com/",
        "seeds": [
            "https://guorn.com/",
            "https://guorn.com/strategies",
            "https://guorn.com/community",
            "https://guorn.com/sitemap.xml",
        ],
        "search_queries": [
            "site:guorn.com 果仁网 量化 策略 A股 ETF",
            "site:guorn.com 果仁网 策略 回测 因子",
        ],
    },
    {
        "name": "thinktrader",
        "label": "ThinkTrader / 讯投",
        "base": "http://thinktrader.net/",
        "seeds": [
            "http://thinktrader.net/",
            "http://thinktrader.net/sitemap.xml",
        ],
        "search_queries": [
            "site:thinktrader.net ThinkTrader 量化 策略",
            "site:thinktrader.net 讯投 量化 交易",
        ],
    },
]

KEYWORDS = [
    "量化", "策略", "回测", "因子", "选股", "择时", "组合", "ETF", "A股", "港股",
    "股票", "期货", "指数", "多因子", "机器学习", "AI", "人工智能", "数据",
    "研报", "交易", "实盘", "API", "JoinQuant", "聚宽", "果仁", "ThinkTrader",
]

THEME_RULES = {
    "AI/机器学习量化": ["AI", "人工智能", "机器学习", "深度学习", "大模型"],
    "多因子/选股": ["因子", "多因子", "选股", "alpha", "Alpha"],
    "ETF/轮动": ["ETF", "轮动", "指数增强", "行业轮动"],
    "回测/实盘系统": ["回测", "实盘", "交易接口", "API", "模拟交易"],
    "A股策略": ["A股", "股票", "沪深", "北交所"],
    "风险控制/组合": ["风控", "回撤", "组合", "资产配置", "仓位"],
}


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[dict] = []
        self._current_href: str | None = None
        self._text: list[str] = []
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "a":
            attrs_dict = dict(attrs)
            self._current_href = attrs_dict.get("href")
            self._text = []
        elif tag.lower() == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._current_href:
            text = clean_text(" ".join(self._text))
            if text:
                self.links.append({"href": self._current_href, "text": text})
            self._current_href = None
            self._text = []
        elif tag.lower() == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._current_href is not None:
            self._text.append(data)
        if self._in_title:
            self.title += data


def clean_text(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def fetch(url: str, timeout: int = 15) -> tuple[int | None, str, str | None]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Codex Quant Platform Radar; public pages only)",
            "Accept": "text/html,application/xml,application/rss+xml,text/xml,*/*",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read(1_000_000)
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.status, raw.decode(charset, "ignore"), None
    except Exception as exc:  # noqa: BLE001
        return None, "", str(exc)


def is_interesting(text: str) -> bool:
    return any(k.lower() in text.lower() for k in KEYWORDS)


def score_text(text: str) -> int:
    score = sum(1 for k in KEYWORDS if k.lower() in text.lower())
    score += sum(2 for terms in THEME_RULES.values() for term in terms if term.lower() in text.lower())
    return score


def normalize_url(base: str, href: str) -> str:
    return urllib.parse.urljoin(base, href.split("#", 1)[0])


def parse_html_links(source: dict, url: str, content: str) -> list[dict]:
    parser = LinkParser()
    parser.feed(content)
    rows = []
    page_title = clean_text(parser.title)
    if page_title and is_interesting(page_title):
        rows.append(make_item(source, url, page_title, "page-title", score_text(page_title)))
    for link in parser.links:
        final_url = normalize_url(url, link["href"])
        if not final_url.startswith(source["base"].rstrip("/")):
            continue
        text = clean_text(link["text"])
        if len(text) < 2 or not is_interesting(text):
            continue
        rows.append(make_item(source, final_url, text, "homepage-link", score_text(text)))
    return rows


def parse_xml_urls(source: dict, url: str, content: str) -> list[dict]:
    rows = []
    if not content.strip():
        return rows
    try:
        root = ET.fromstring(content)
    except ET.ParseError:
        return rows
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = [el.text for el in root.findall(".//sm:loc", ns)] or [el.text for el in root.findall(".//loc")]
    for loc in locs[:80]:
        if not loc:
            continue
        title = urllib.parse.unquote(loc.rstrip("/").split("/")[-1]) or loc
        if is_interesting(title) or any(part in loc.lower() for part in ["community", "strategy", "research", "api", "help"]):
            rows.append(make_item(source, loc, title, "sitemap", score_text(title)))
    return rows


def search_bing(source: dict, query: str) -> list[dict]:
    url = "https://www.bing.com/search?q=" + urllib.parse.quote(query)
    status, content, err = fetch(url, timeout=12)
    if err or not content:
        return [make_status(source, "search", f"{query}: {err or status}")]
    text = re.sub(r"<[^>]+>", " ", content)
    text = clean_text(text)
    rows = []
    for match in re.finditer(r"(https?://[^\s\"'<>]+)", content):
        candidate = html.unescape(match.group(1))
        if source["base"].split("//", 1)[-1].rstrip("/") not in candidate:
            continue
        candidate = candidate.split("&", 1)[0]
        snippet_start = max(0, match.start() - 180)
        snippet_end = min(len(text), match.start() + 260)
        snippet = clean_text(text[snippet_start:snippet_end])
        if is_interesting(snippet):
            rows.append(make_item(source, candidate, snippet[:220], "search-snippet", score_text(snippet)))
    return rows[:10]


def make_item(source: dict, url: str, title: str, kind: str, score: int) -> dict:
    return {
        "source": source["name"],
        "source_label": source["label"],
        "kind": kind,
        "url": url,
        "title": clean_text(title)[:300],
        "score": score,
        "themes": detect_themes(title),
    }


def make_status(source: dict, kind: str, message: str) -> dict:
    return {
        "source": source["name"],
        "source_label": source["label"],
        "kind": f"status-{kind}",
        "url": source["base"],
        "title": message[:300],
        "score": 0,
        "themes": [],
    }


def detect_themes(text: str) -> list[str]:
    themes = []
    lower = text.lower()
    for theme, terms in THEME_RULES.items():
        if any(term.lower() in lower for term in terms):
            themes.append(theme)
    return themes


def dedupe(items: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for item in sorted(items, key=lambda x: x.get("score", 0), reverse=True):
        key = (item.get("source"), item.get("url"), item.get("title"))
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def update(skill_dir: Path) -> dict:
    now = dt.datetime.now(dt.timezone.utc).astimezone()
    items = []
    status_lines = []
    for source in SOURCES:
        for seed in source["seeds"]:
            status, content, err = fetch(seed)
            if err:
                status_lines.append(f"{source['name']}: {seed}: {err}")
                continue
            status_lines.append(f"{source['name']}: ok {seed} ({status})")
            if "xml" in seed or content.lstrip().startswith("<?xml"):
                items.extend(parse_xml_urls(source, seed, content))
            else:
                items.extend(parse_html_links(source, seed, content))
        for query in source["search_queries"]:
            items.extend(search_bing(source, query))

    items = dedupe(items)
    rows = []
    for item in items[:120]:
        row = {"collected_at": now.isoformat(), **item}
        rows.append(row)

    refs = skill_dir / "references"
    daily = refs / "daily"
    daily.mkdir(parents=True, exist_ok=True)
    archive = daily / f"{now.date().isoformat()}.jsonl"
    with archive.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    latest = refs / "latest.md"
    latest.write_text(render_latest(now, rows, status_lines), encoding="utf-8")
    return {"skill_dir": str(skill_dir), "rows": len(rows), "archive": str(archive), "source_status": status_lines}


def render_latest(now: dt.datetime, rows: list[dict], status_lines: list[str]) -> str:
    by_source: dict[str, list[dict]] = {}
    theme_counts: dict[str, int] = {}
    for row in rows:
        by_source.setdefault(row["source"], []).append(row)
        for theme in row.get("themes") or []:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1

    lines = [
        "# Quant Platform Radar - Latest Learned State",
        "",
        f"Last update: {now.isoformat()}",
        f"Status: updated with {len(rows)} public items",
        "",
        "## Current Themes",
        "",
    ]
    if theme_counts:
        for theme, count in sorted(theme_counts.items(), key=lambda kv: kv[1], reverse=True):
            lines.append(f"- {theme}: {count}")
    else:
        lines.append("- No high-confidence themes detected from public pages.")

    lines += ["", "## Source Deltas", ""]
    for source in SOURCES:
        source_rows = by_source.get(source["name"], [])
        lines.append(f"### {source['label']}")
        lines.append("")
        if not source_rows:
            lines.append("- No usable public items collected.")
        else:
            for row in source_rows[:12]:
                themes = ", ".join(row.get("themes") or ["unclassified"])
                lines.append(f"- {row['kind']} | score {row['score']} | {themes} | [{row['title']}]({row['url']})")
        lines.append("")

    lines += [
        "## Source Health",
        "",
    ]
    for status in status_lines:
        lines.append(f"- {status}")
    lines += [
        "",
        "## Next Analysis Instructions",
        "",
        "- Treat search snippets and partial page titles as Weak evidence.",
        "- Verify any stock mapping with live market data, filings, announcements, or credible news.",
        "- Prefer repeated strategy/style themes across multiple platforms.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-dir", required=True)
    args = parser.parse_args()
    result = update(Path(args.skill_dir))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
