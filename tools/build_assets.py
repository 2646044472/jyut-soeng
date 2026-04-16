#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
OUTPUT_PATH = ROOT / "app" / "src" / "main" / "assets" / "builtin" / "content.json"
ASCII_RE = re.compile(r"[A-Za-z]")


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
            return "多放在熟人闲聊、吐槽或情绪反应里。"
        if category == "口语场景":
            return "适合直接放进对话里，句子不用太长。"
        if category == "情绪表达":
            return "通常放在讲自己感觉或评价别人状态时。"
        if category == "工作场景":
            return "适合放在讲安排、进度和处理方式时。"
        return f"想讲得自然一点时，可以直接用「{display_text}」。"
    if category == "工作场景":
        return "适合放在开会、交代事情或讲做法时。"
    if category == "学习场景":
        return "适合拿来练习说明、提问和复述。"
    if category == "情绪表达":
        return "多放在讲感觉、情绪变化和反应时。"
    return f"开口时直接把「{display_text}」带进句子里就可以。"


def ensure_two_line_examples(display_text: str, raw: str, category: str, entry_type: str) -> str:
    lines = [line.strip() for line in str(raw or "").split("\n") if line.strip()]
    if not lines:
        if entry_type == "expression":
            lines = [
                f"朋友倾偈时，可以直接讲「{display_text}」。",
                f"下次讲到类似情况时，试住自然带出「{display_text}」。",
            ]
        else:
            lines = [
                f"你可以先用「{display_text}」讲一次完整句子。",
                f"再试多次，把「{display_text}」读得更顺一点。",
            ]
    elif len(lines) == 1:
        lines.append(
            f"下次开口时，再用一次「{display_text}」，把读法读顺。"
            if entry_type == "expression"
            else f"你可以再用一次「{display_text}」，把句子说顺一点。"
        )
    return "\n".join(lines[:3])


def normalize_gloss(raw: str, display_text: str, category: str, entry_type: str) -> str:
    text = str(raw or "").strip()
    if not text or ASCII_RE.search(text):
        return build_fallback_meaning(display_text, category, entry_type)
    return text


def normalize_usage(raw: str, display_text: str, category: str, entry_type: str) -> str:
    text = str(raw or "").strip()
    if not text or ASCII_RE.search(text):
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
        item = {
            "id": row["id"],
            "displayText": display_text,
            "promptText": row.get(
                "promptText",
                "先按自己的习惯读一遍，再写出 Jyutping，用它检查自己有没有读准。"
                if entry_type == "word"
                else "先理解这条口语表达，再写出 Jyutping，最后跟着例句开口读。",
            ),
            "answerJyutping": row["answerJyutping"],
            "gloss": normalize_gloss(row.get("gloss", ""), display_text, category, entry_type),
            "notes": "",
            "usageTip": normalize_usage(row.get("usageTip", ""), display_text, category, entry_type),
            "exampleSentence": ensure_two_line_examples(display_text, row.get("exampleSentence", ""), category, entry_type),
            "exampleTranslation": "",
            "entryType": entry_type,
            "category": category,
            "groupId": row.get("groupId", row["id"]),
            "tone": row.get("tone", 0),
            "audioAsset": row.get("audioAsset"),
            "sourceLabel": row.get("sourceLabel", source_label),
        }
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
