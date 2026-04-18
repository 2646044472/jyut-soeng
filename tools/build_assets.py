#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
OUTPUT_PATH = ROOT / "app" / "src" / "main" / "assets" / "builtin" / "content.json"
QUALITY_OVERRIDES_PATH = CONTENT_DIR / "quality_overrides.json"
ASCII_RE = re.compile(r"[A-Za-z]")
LOW_INFO_USAGE_MARKERS = (
    "适合练",
    "适合拿来练",
    "适合拿来校正",
    "适合校正",
    "适合做基础稳定练习",
    "适合练自然收句",
    "拿来练",
    "值得反复校正",
    "越高频越值得校准",
    "重点是读得自然",
    "读起来容易",
    "自然收句",
    "稳定度很合适",
    "最容易听出前后差别",
    "高频而且很容易受普通话影响",
    "很适合拿来练",
)


def load_quality_overrides() -> dict[str, dict[str, str]]:
    if not QUALITY_OVERRIDES_PATH.exists():
        return {}
    raw = json.loads(QUALITY_OVERRIDES_PATH.read_text(encoding="utf-8"))
    return {
        str(entry_id): {
            str(key): str(value)
            for key, value in fields.items()
            if isinstance(value, str) and value.strip()
        }
        for entry_id, fields in raw.items()
        if isinstance(fields, dict)
    }


QUALITY_OVERRIDES = load_quality_overrides()


def build_fallback_meaning(display_text: str, category: str, entry_type: str) -> str:
    if entry_type == "expression":
        if category == "俚语表达":
            return "偏口语的说法，主要拿来讲某种状态、反应或场面。"
        if category == "口语场景":
            return "对话里常见的说法，开口时可以直接带出来。"
        if category == "情绪表达":
            return "用来表达感觉、情绪或当下状态。"
        if category == "工作场景":
            return "多用于交代事情、讲进度或讲处理方式。"
        return f"常见表达，日常讲话时可以自然用「{display_text}」。"
    if category == "工作场景":
        return "工作沟通里常见的词，适合拿来练稳定开口。"
    if category == "学习场景":
        return "学习语境常见词，适合拿来校正读法。"
    if category == "情绪表达":
        return "常用来讲感受、状态或反应。"
    if category == "口语场景":
        return "日常讲话常见词，重点是读顺和讲自然。"
    return f"常用词，适合放进日常句子里练熟「{display_text}」。"


def build_fallback_usage(display_text: str, category: str, entry_type: str) -> str:
    if entry_type == "expression":
        if category == "俚语表达":
            return "多放在熟人对话里，通常用来回应状况、吐槽或者补一句态度。"
        if category == "口语场景":
            return "适合直接当回应或接话位，后面再补一句解释就够。"
        if category == "情绪表达":
            return "多用来讲自己当下感受，也可以拿来评价别人状态。"
        if category == "工作场景":
            return "常放在讲安排、进度、做法或交代事情的时候。"
        if category == "安抚表达":
            return "多用来叫人放松一点、先稳住，或者提醒对方唔使急。"
        if category == "礼貌表达":
            return "多放在回应多谢、请人帮忙或把语气放软的时候。"
        if category == "鼓励表达":
            return "用来俾人打气最自然，通常单独讲一句就已经够。"
        if category == "高频口语":
            return "多当短回应或句尾补充，令语气听起来更自然。"
        if category == "日常表达":
            return "放在日常对话里最自然，通常一开口就可以直接带出来。"
        return f"多放在口语句子里，先用短句把「{display_text}」讲顺，再慢慢拉长。"
    if category == "问句高频词":
        return "多放在问句开头，用来追问原因、做法或者而家个状况。"
    if category in {"地点常用词", "地名常用词"}:
        return "多跟「喺 / 去 / 返 / 到」呢类动词搭配，讲人喺边或者去边。"
    if category == "礼貌表达":
        return "多用来道谢、请人帮忙、借过，或者先把语气放软。"
    if category == "工作场景":
        return "开会、交代事情、讲做法或者讲进度时最常用。"
    if category == "学习场景":
        return "多用来讲上堂、练习、功课或者学习安排。"
    if category == "情绪表达":
        return "多用来讲自己感觉、评价状态，或者安抚别人。"
    if category == "提醒表达":
        return "多用来提醒对方注意、先停一停，或者换个做法。"
    if category == "组织表达":
        return "多用来讲整理资料、分步骤说明，或者把事情串起来。"
    if category == "安抚表达":
        return "多用来叫人唔使急、先放松，或者一步一步来。"
    if category == "时间表达":
        return "多放在句首或动词前，交代时间点或者最近呢段时间。"
    if category == "评价表达":
        return "多用来判断人、做法或者结果够唔够好、啱唔啱。"
    if category == "正音术语":
        return "多出现在纠音、教学或者讲读法的时候，用来点出问题位。"
    if category == "主题核心词":
        return "多用来讲自己想学、会讲，或者直接指粤语呢门语言。"
    if category == "高频口语":
        return "多放在短句里直接用，通常一开口就会接到。"
    if category == "高频日常词":
        return "多用来讲眼前发生的事、日常安排或者基本状态。"
    if category == "进阶常用词":
        return "多用来讲状态、变化或者较抽象的概念，常放在判断句里。"
    return f"先放进最短的日常句里，用「{display_text}」讲清自己想表达什么。"


def build_generated_usage_tip(entry_type: str) -> str:
    if entry_type == "expression":
        return "这条先当语气卡：跟读、记节奏就够；真要学点用，优先看人工整理的表达卡。"
    return "这条先当读音卡：跟读、拆音、写 Jyutping 就够；真要学点用，优先看人工整理词条。"


def is_low_info_usage(text: str) -> bool:
    return any(marker in text for marker in LOW_INFO_USAGE_MARKERS)


def build_generated_practice_prompt(display_text: str, entry_type: str) -> str:
    if entry_type == "expression":
        return "\n".join(
            [
                f"先把「{display_text}」跟读两次，记住语气和节奏。",
                "这类生成表达只供语气练习，不代表推荐用法，不必硬套进句子。",
            ],
        )
    return "\n".join(
        [
            f"先把「{display_text}」读两次，留意每个音节。",
            "这类生成词条只供读音练习，不代表推荐用法，不必硬套进句子。",
        ],
    )


def build_prompt_text(raw: str, entry_type: str, source_label: str) -> str:
    text = str(raw or "").strip()
    if text:
        return text
    if source_label == "generated":
        if entry_type == "word":
            return "先按自己的习惯读一遍，再写出 Jyutping，最后按提示把词读顺。"
        return "先理解这条口语表达，再写出 Jyutping，最后按提示自己开口讲。"
    if entry_type == "word":
        return "先按自己的习惯读一遍，再写出 Jyutping，用它检查自己有没有读准。"
    return "先理解这条口语表达，再写出 Jyutping，最后跟着例句开口读。"


def ensure_two_line_examples(display_text: str, raw: str, category: str, entry_type: str) -> str:
    lines = [line.strip() for line in str(raw or "").split("\n") if line.strip()]
    if not lines:
        if entry_type == "expression":
            lines = [f"朋友倾偈时，可以直接讲「{display_text}」。"]
        else:
            lines = [f"先用「{display_text}」讲一条最短、最自然的日常句子。"]
    return "\n".join(lines[:3])


def normalize_gloss(raw: str, display_text: str, category: str, entry_type: str) -> str:
    text = str(raw or "").strip()
    if not text or ASCII_RE.search(text):
        return build_fallback_meaning(display_text, category, entry_type)
    return text


def normalize_usage(raw: str, display_text: str, category: str, entry_type: str, source_label: str) -> str:
    if source_label == "generated":
        return build_generated_usage_tip(entry_type)
    text = str(raw or "").strip()
    if not text or ASCII_RE.search(text) or is_low_info_usage(text):
        return build_fallback_usage(display_text, category, entry_type)
    return text


def infer_source_label(path: Path) -> str:
    return "generated" if path.stem.startswith("generated_") else "curated"


def load_entries(path: Path, entry_type: str) -> list[dict]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    entries: list[dict] = []
    source_label = infer_source_label(path)
    for row in rows:
        category = row.get("category", "")
        display_text = row["displayText"]
        resolved_source_label = row.get("sourceLabel", source_label)
        item = {
            "id": row["id"],
            "displayText": display_text,
            "promptText": build_prompt_text(
                row.get("promptText", ""),
                entry_type=entry_type,
                source_label=resolved_source_label,
            ),
            "answerJyutping": row["answerJyutping"],
            "gloss": normalize_gloss(row.get("gloss", ""), display_text, category, entry_type),
            "notes": "",
            "usageTip": normalize_usage(
                row.get("usageTip", ""),
                display_text,
                category,
                entry_type,
                resolved_source_label,
            ),
            "exampleSentence": (
                build_generated_practice_prompt(display_text, entry_type)
                if resolved_source_label == "generated"
                else ensure_two_line_examples(display_text, row.get("exampleSentence", ""), category, entry_type)
            ),
            "exampleTranslation": "",
            "entryType": entry_type,
            "category": category,
            "groupId": row.get("groupId", row["id"]),
            "tone": row.get("tone", 0),
            "audioAsset": row.get("audioAsset"),
            "sourceLabel": resolved_source_label,
        }
        item.update(QUALITY_OVERRIDES.get(row["id"], {}))
        entries.append(item)
    return entries


def load_all_entries() -> list[dict]:
    entries: list[dict] = []
    for path in sorted(CONTENT_DIR.glob("*_bank.json")):
        name = path.stem.lower()
        entry_type = "expression" if any(token in name for token in ("expression", "slang", "conversation")) else "word"
        entries.extend(load_entries(path, entry_type))
    return entries


def main() -> None:
    entries = load_all_entries()
    for index, entry in enumerate(entries, start=1):
        entry["sortOrder"] = index
    bundle = {
        "version": datetime.now(timezone.utc).strftime("%Y.%m.%d.%H%M"),
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "entries": entries,
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(bundle, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(entries)} entries to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
