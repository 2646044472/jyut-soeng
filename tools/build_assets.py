#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORDS_PATH = ROOT / "content" / "word_bank.json"
EXPRESSIONS_PATH = ROOT / "content" / "expression_bank.json"
OUTPUT_PATH = ROOT / "app" / "src" / "main" / "assets" / "builtin" / "content.json"


def load_entries(path: Path, entry_type: str) -> list[dict]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    entries: list[dict] = []
    for row in rows:
        item = {
            "id": row["id"],
            "displayText": row["displayText"],
            "promptText": row.get(
                "promptText",
                "先按自己的习惯读一遍，再写出 Jyutping，用它检查自己有没有读准。"
                if entry_type == "word"
                else "先理解这条口语表达，再写出 Jyutping，最后跟着例句开口读。",
            ),
            "answerJyutping": row["answerJyutping"],
            "gloss": row.get("gloss", ""),
            "notes": row.get("notes", ""),
            "usageTip": row.get("usageTip", ""),
            "exampleSentence": row.get("exampleSentence", ""),
            "exampleTranslation": row.get("exampleTranslation", ""),
            "entryType": entry_type,
            "category": row.get("category", ""),
            "groupId": row.get("groupId", row["id"]),
            "tone": row.get("tone", 0),
            "audioAsset": row.get("audioAsset"),
            "sourceLabel": row.get("sourceLabel", "builtin"),
        }
        entries.append(item)
    return entries


def main() -> None:
    entries = load_entries(WORDS_PATH, "word") + load_entries(EXPRESSIONS_PATH, "expression")
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
