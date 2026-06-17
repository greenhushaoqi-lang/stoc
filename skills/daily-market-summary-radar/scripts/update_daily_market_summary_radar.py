#!/usr/bin/env python3
"""Update compact memory for local daily market summary notes."""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import hashlib
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_SOURCE_DIR = Path(r"C:\Users\lixue\Desktop\st总结")
TEXT_EXTS = {".txt", ".md"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

THEME_KEYWORDS = [
    "AI", "算力", "半导体", "芯片", "存储", "HBM", "CPO", "光模块", "液冷",
    "PCB", "CCL", "覆铜板", "铜箔", "MLCC", "被动元件", "铝电解电容",
    "玻璃基板", "先进封装", "六氟化钨", "电子特气", "稀土", "钨", "锗", "铜",
    "小金属", "功率半导体", "AI电源", "电网", "变压器", "机器人", "固态电池",
    "半导体设备", "半导体材料", "光刻", "检测设备", "自动化", "券商", "并购",
    "重组", "涨价", "供需", "美联储", "降息", "关税", "政策", "美股", "日股",
    "韩股", "英伟达", "AMD", "台积电", "三星", "海力士",
]

SOURCE_MARKERS = [
    "鹏睿", "老鱼", "糖糖", "抖音博主", "x上", "livermoer", "海外华人A股资讯",
    "投研荟", "白何愁博士", "雪球老鱼", "孙潇雅", "joy", "新闸路摸鱼仔",
    "短线小富婆", "老高",
]

RISK_PATTERNS = [
    "谨慎追高", "回调", "中阴", "高开", "冲高回落", "跌破", "破5日", "破30日",
    "机构减仓", "不能突破", "风险", "兑现", "低吸", "做T", "减点", "留个底仓",
]

KNOWN_STOCKS = [
    "光华科技", "圣泉集团", "铜陵有色", "富创精密", "厦门钨业", "晶丰明源", "三环集团",
    "洁美科技", "鸿远电子", "宏达电子", "建滔积层板", "建滔集团", "德科立", "容大感光",
    "四会富士", "金太阳", "云南锗业", "安孚科技", "安靠智电", "铜冠铜箔", "联瑞新材",
    "杰华特", "源杰科技", "斯迪克", "大普微", "麦格米特", "南芯科技", "星源材质",
    "世运电路", "三祥新材", "激智科技", "东威科技", "劲拓股份", "炬光科技", "微导纳米",
    "方正科技", "开勒股份", "新益昌", "永鼎股份", "太极实业", "合盛硅业", "华正新材",
    "金安国纪", "宝鼎科技", "深南电路", "龙蟠科技", "力诺药包", "日联科技", "信德新材",
    "奕东电子", "罗博特科", "奥特维", "天准科技", "快克智能", "博众精工", "凯格精机",
    "杰普特", "精测电子", "联动科技", "柏诚股份", "东山精密", "天孚通信", "拓荆科技",
    "先锋精科", "致尚科技", "昊华科技", "盛美上海", "长光华芯", "晶升股份", "天岳先进",
    "华海清科", "中微公司", "芯源微", "华海诚科", "中巨芯", "华虹宏力", "鼎通科技",
    "广钢气体", "柏楚电子", "鸿富瀚", "珂玛科技", "行云科技", "智立方", "汇成真空",
    "本川智能", "燕麦科技", "鼎龙股份", "风华高科", "赛腾股份", "合锻智能", "宏工科技",
    "先惠技术", "海目星", "科翔股份", "普源精电", "一博科技", "苏州固锝", "芯碁微装",
]


def sha1_text(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8", errors="ignore")).hexdigest()[:16]


def read_text(path: Path) -> str:
    for enc in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="ignore")


def short(text: str, width: int = 180) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text[: width - 3] + "..." if len(text) > width else text


def load_manual_image_notes(skill_dir: Path) -> dict[str, dict[str, Any]]:
    path = skill_dir / "references" / "manual-image-notes.jsonl"
    notes: dict[str, dict[str, Any]] = {}
    if not path.exists():
        return notes
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        notes[str(obj.get("file", ""))] = obj
    return notes


def collect_sources(source_dir: Path, skill_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    manual_notes = load_manual_image_notes(skill_dir)
    text_items: list[dict[str, Any]] = []
    image_items: list[dict[str, Any]] = []

    for path in sorted(source_dir.iterdir(), key=lambda p: p.name):
        if path.is_dir():
            continue
        stat = path.stat()
        if path.suffix.lower() in TEXT_EXTS:
            text = read_text(path)
            text_items.append(
                {
                    "file": path.name,
                    "path": str(path),
                    "mtime": dt.datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "sha1": sha1_text(text),
                    "text": text,
                }
            )
        elif path.suffix.lower() in IMAGE_EXTS:
            note = manual_notes.get(path.name)
            image_items.append(
                {
                    "file": path.name,
                    "path": str(path),
                    "mtime": dt.datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "size": stat.st_size,
                    "manual_note": note,
                    "status": "learned from manual visual note" if note else "pending visual/OCR review",
                }
            )
    return text_items, image_items


def split_date_sections(text: str) -> dict[str, str]:
    pattern = re.compile(r"(?m)^\s*(\d{1,2}\.\d{1,2})\s*$")
    matches = list(pattern.finditer(text))
    if not matches:
        return {"undated": text}
    sections: dict[str, str] = {}
    prefix = text[: matches[0].start()].strip()
    if prefix:
        sections["context"] = prefix
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[match.group(1)] = text[start:end].strip()
    return sections


def extract_entities(text: str) -> dict[str, Any]:
    stock_counter = collections.Counter()
    for stock in KNOWN_STOCKS:
        if stock in text:
            stock_counter[stock] += text.count(stock)
    for name in re.findall(r"【([^】]{2,12})】", text):
        if not re.search(r"[0-9a-zA-Z]", name):
            stock_counter[name] += 1

    theme_counter = collections.Counter({kw: text.count(kw) for kw in THEME_KEYWORDS if kw in text})
    source_counter = collections.Counter({src: text.count(src) for src in SOURCE_MARKERS if src in text})
    risks = [p for p in RISK_PATTERNS if p in text]
    levels = sorted(set(re.findall(r"(?<!\d)(?:40\d{2}|41\d{2}|39\d{2}|4154|4133|4107|4070|4008)(?!\d)", text)))
    dates = sorted(set(re.findall(r"(?<!\d)\d{1,2}\.\d{1,2}(?!\d)", text)))
    return {
        "stocks": stock_counter.most_common(80),
        "themes": theme_counter.most_common(60),
        "sources": source_counter.most_common(40),
        "risks": risks,
        "index_levels": levels,
        "dates": dates,
    }


def build_compact_records(text_items: list[dict[str, Any]], image_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for item in text_items:
        sections = split_date_sections(item["text"])
        for date_label, body in sections.items():
            records.append(
                {
                    "type": "text-section",
                    "source_file": item["file"],
                    "source_sha1": item["sha1"],
                    "section": date_label,
                    "entities": extract_entities(body),
                    "snippet": short(body, 500),
                }
            )
    for item in image_items:
        note = item.get("manual_note")
        records.append(
            {
                "type": "image-note" if note else "image-pending",
                "source_file": item["file"],
                "status": item["status"],
                "summary": note.get("summary") if note else "",
                "framework_tags": note.get("framework_tags", []) if note else [],
                "stocks_or_themes": note.get("stocks_or_themes", []) if note else [],
                "risk_notes": note.get("risk_notes", []) if note else [],
            }
        )
    return records


def build_latest(records: list[dict[str, Any]], text_items: list[dict[str, Any]], image_items: list[dict[str, Any]]) -> str:
    now = dt.datetime.now().isoformat(timespec="seconds")
    all_text = "\n".join(item["text"] for item in text_items)
    global_entities = extract_entities(all_text)
    image_notes = [r for r in records if r["type"] == "image-note"]
    pending_images = [r for r in records if r["type"] == "image-pending"]

    lines = [
        "# Daily Market Summary Radar - Latest Learned State",
        "",
        f"Last update: {now}",
        f"Text files learned: {len(text_items)}",
        f"Images indexed: {len(image_items)}",
        f"Manual image notes used: {len(image_notes)}",
        "",
        "## Source Files",
        "",
    ]
    for item in text_items:
        lines.append(f"- text: `{item['file']}` | mtime={item['mtime']} | sha1={item['sha1']}")
    for item in image_items:
        lines.append(f"- image: `{item['file']}` | {item['status']} | mtime={item['mtime']}")

    lines += ["", "## Current Extracted Themes", ""]
    lines.append("- themes: " + (", ".join(f"{k}({v})" for k, v in global_entities["themes"][:40]) or "none"))
    lines.append("- stocks: " + (", ".join(f"{k}({v})" for k, v in global_entities["stocks"][:60]) or "none"))
    lines.append("- sources: " + (", ".join(f"{k}({v})" for k, v in global_entities["sources"][:30]) or "none"))
    lines.append("- index levels: " + (", ".join(global_entities["index_levels"]) or "none"))
    lines.append("- risk words: " + (", ".join(global_entities["risks"]) or "none"))

    lines += ["", "## Date Sections", ""]
    for record in records:
        if record["type"] != "text-section":
            continue
        ents = record["entities"]
        stocks = ", ".join(k for k, _ in ents["stocks"][:20]) or "none"
        themes = ", ".join(k for k, _ in ents["themes"][:20]) or "none"
        levels = ", ".join(ents["index_levels"]) or "none"
        risks = ", ".join(ents["risks"]) or "none"
        lines += [
            f"### {record['section']} / {record['source_file']}",
            "",
            f"- themes: {themes}",
            f"- stocks: {stocks}",
            f"- index levels: {levels}",
            f"- risk clues: {risks}",
            f"- snippet: {record['snippet']}",
            "",
        ]

    lines += ["## Image Framework Notes", ""]
    if image_notes:
        for note in image_notes:
            lines.append(f"### {note['source_file']}")
            lines.append("")
            lines.append(f"- summary: {note['summary']}")
            lines.append("- framework_tags: " + ", ".join(note["framework_tags"]))
            lines.append("- stocks_or_themes: " + ", ".join(note["stocks_or_themes"]))
            lines.append("- risk_notes: " + ", ".join(note["risk_notes"]))
            lines.append("")
    else:
        lines.append("- No manual image notes available.")
    if pending_images:
        lines.append("## Pending Image Review")
        lines.append("")
        for img in pending_images:
            lines.append(f"- `{img['source_file']}`")
        lines.append("")

    lines += [
        "## Next Analysis Instructions",
        "",
        "- Treat all extracted stocks as research leads, not buy/sell instructions.",
        "- Verify market data, filings, company announcements, and credible news before ranking.",
        "- Separate long-form framework logic from short-term blogger/X chatter.",
        "- Use repeated themes and price/volume confirmation to upgrade signal quality.",
        "- Downgrade high-crowding, high-open selloff, and EPS-not-confirmed narratives.",
    ]
    return "\n".join(lines) + "\n"


def write_outputs(skill_dir: Path, records: list[dict[str, Any]], latest: str) -> None:
    refs = skill_dir / "references"
    daily = refs / "daily"
    daily.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    (daily / f"{today}.jsonl").write_text(
        "\n".join(json.dumps(record, ensure_ascii=False, sort_keys=True) for record in records) + "\n",
        encoding="utf-8",
    )
    (refs / "latest.md").write_text(latest, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Update daily market summary radar memory.")
    parser.add_argument("--skill-dir", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--source-dir", default=str(DEFAULT_SOURCE_DIR))
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    source_dir = Path(args.source_dir).resolve()
    if not source_dir.exists():
        raise SystemExit(f"source dir does not exist: {source_dir}")

    text_items, image_items = collect_sources(source_dir, skill_dir)
    records = build_compact_records(text_items, image_items)
    latest = build_latest(records, text_items, image_items)
    write_outputs(skill_dir, records, latest)
    print(
        json.dumps(
            {
                "skill_dir": str(skill_dir),
                "source_dir": str(source_dir),
                "text_files": len(text_items),
                "images": len(image_items),
                "records": len(records),
                "manual_image_notes": sum(1 for item in image_items if item.get("manual_note")),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
