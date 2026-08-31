#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
OUTPUT_PATH = ROOT / "app" / "src" / "main" / "assets" / "builtin" / "content.json"
def build_prompt_text(raw: str, entry_type: str) -> str:
    text = str(raw or "").strip()
    if text:
        return text
    if entry_type == "word":
        return "先按自己答案写出 Jyutping，再看意思、用法同例句。"
    return "先理解呢条表达，再写出 Jyutping，再看意思、用法同例句。"


def trim_examples(raw: str) -> str:
    lines = [line.strip() for line in str(raw or "").split("\n") if line.strip()]
    return "\n".join(lines[:3])


def load_entries(path: Path, entry_type: str) -> list[dict]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    entries: list[dict] = []
    for row in rows:
        category = row.get("category", "")
        display_text = row["displayText"]
        if row.get("sourceLabel", "curated") != "curated":
            raise SystemExit(f"Only hand-written curated entries are allowed: {row['id']}")
        item = {
            "id": row["id"],
            "displayText": display_text,
            "promptText": build_prompt_text(
                row.get("promptText", ""),
                entry_type=entry_type,
            ),
            "answerJyutping": row["answerJyutping"],
            "gloss": str(row.get("gloss", "")).strip(),
            "notes": str(row.get("notes", "")).strip(),
            "usageTip": str(row.get("usageTip", "")).strip(),
            "exampleSentence": trim_examples(row.get("exampleSentence", "")),
            "exampleTranslation": "",
            "entryType": entry_type,
            "category": category,
            "groupId": row.get("groupId", row["id"]),
            "tone": row.get("tone", 0),
            "audioAsset": row.get("audioAsset"),
            "sourceLabel": "curated",
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
