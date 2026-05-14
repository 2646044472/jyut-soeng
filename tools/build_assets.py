#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from meaning_rules import is_low_info_gloss
from meaning_rules import is_fake_example_sentence
from meaning_rules import is_low_info_usage
from meaning_rules import build_better_gloss
from meaning_rules import build_better_usage
from meaning_rules import build_better_example

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
OUTPUT_PATH = ROOT / "app" / "src" / "main" / "assets" / "builtin" / "content.json"
QUALITY_OVERRIDES_PATH = CONTENT_DIR / "quality_overrides.json"

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


def build_prompt_text(raw: str, entry_type: str, source_label: str) -> str:
    text = str(raw or "").strip()
    if text:
        return text
    if source_label == "generated":
        if entry_type == "word":
            return "先想清楚意思，再写出 Jyutping，再看用法同例句。"
        return "先理解呢条表达，再写出 Jyutping，再看用法同例句。"
    if entry_type == "word":
        return "先按自己答案写出 Jyutping，再看意思、用法同例句。"
    return "先理解呢条表达，再写出 Jyutping，再看意思、用法同例句。"


def trim_examples(raw: str) -> str:
    lines = [line.strip() for line in str(raw or "").split("\n") if line.strip()]
    return "\n".join(lines[:3])


def normalize_example(
    raw: str,
    display_text: str,
    category: str,
    entry_type: str,
    source_label: str,
    gloss: str,
    usage_tip: str,
) -> str:
    text = str(raw or "").strip()
    text = trim_examples(text)
    if source_label == "generated" and (is_fake_example_sentence(text, display_text) or not text):
        return trim_examples(build_better_example(display_text, category, entry_type, gloss, usage_tip))
    return text


def normalize_gloss(raw: str, display_text: str, category: str, entry_type: str, source_label: str) -> str:
    text = str(raw or "").strip()
    if source_label == "generated" and is_low_info_gloss(text, display_text):
        return str(build_better_gloss(display_text, category, entry_type, source_label)).strip()
    return text


def normalize_usage(raw: str, display_text: str, category: str, entry_type: str, source_label: str) -> str:
    text = str(raw or "").strip()
    if source_label == "generated" and is_low_info_usage(text):
        return str(build_better_usage(display_text, category, entry_type, source_label)).strip()
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
        gloss = normalize_gloss(row.get("gloss", ""), display_text, category, entry_type, resolved_source_label)
        usage_tip = normalize_usage(
            row.get("usageTip", ""),
            display_text,
            category,
            entry_type,
            resolved_source_label,
        )
        item = {
            "id": row["id"],
            "displayText": display_text,
            "promptText": build_prompt_text(
                row.get("promptText", ""),
                entry_type=entry_type,
                source_label=resolved_source_label,
            ),
            "answerJyutping": row["answerJyutping"],
            "gloss": gloss,
            "notes": "",
            "usageTip": usage_tip,
            "exampleSentence": normalize_example(
                row.get("exampleSentence", ""),
                display_text,
                category,
                entry_type,
                resolved_source_label,
                gloss,
                usage_tip,
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
