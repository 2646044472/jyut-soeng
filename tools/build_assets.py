#!/usr/bin/env python3
from __future__ import annotations

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
SENTENCE_BANK_DIR = CONTENT_DIR / "sentence_bank"
STORY_SELECTION_PATH = CONTENT_DIR / "story_library_selection.json"
OUTPUT_PATH = ROOT / "app" / "src" / "main" / "assets" / "builtin" / "content.json"


def story_selection() -> tuple[set[str], set[str]]:
    if not STORY_SELECTION_PATH.exists():
        raise SystemExit(f"Missing active story selection manifest: {STORY_SELECTION_PATH}")
    selection = json.loads(STORY_SELECTION_PATH.read_text(encoding="utf-8"))
    active_ids = selection.get("active_ids", [])
    excluded_ids = selection.get("excluded_ids", [])
    if (
        len(active_ids) != selection.get("target_active_cards")
        or len(active_ids) != len(set(active_ids))
        or len(excluded_ids) != selection.get("excluded_cards")
        or len(excluded_ids) != len(set(excluded_ids))
        or set(active_ids) & set(excluded_ids)
        or len(active_ids) + len(excluded_ids) != selection.get("source_cards")
    ):
        raise SystemExit("Story selection manifest has an invalid active/excluded ID partition")
    return set(active_ids), set(excluded_ids)


def reviewed_sentence_entry_ids() -> set[str]:
    ledger_path = ROOT / "STORY_QUALITY_REVALIDATION.json"
    if not ledger_path.exists():
        return set()

    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    reviewed_ids: set[str] = set()
    for record in ledger.get("cards", []):
        if record.get("status") != "pass":
            continue
        source_path = ROOT / record["file"]
        rows = json.loads(source_path.read_text(encoding="utf-8"))
        index = record["index"]
        if index < 0 or index >= len(rows):
            continue
        row = rows[index]
        encoded = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        if hashlib.sha256(encoded).hexdigest() != record.get("v2_sha256"):
            continue
        reviewed_ids.add(f"sentence-bank-{source_path.stem}-{index + 1:04d}")
    return reviewed_ids
def build_prompt_text(raw: str, entry_type: str) -> str:
    text = str(raw or "").strip()
    if text:
        return text
    if entry_type == "word":
        return "先按自己答案写出 Jyutping，再看意思、用法同例句。"
    if entry_type == "sentence":
        return "先顺住读完整句子同 Jyutping，再留意语气、节奏同连贯度。"
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
            raise SystemExit(f"Only curated entries are allowed: {row['id']}")
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


def load_independent_sentence_entries(
    path: Path, selected_ids: set[str], source_ids: set[str]
) -> list[dict]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    entries: list[dict] = []
    for index, row in enumerate(rows, start=1):
        entry_id = f"sentence-bank-{path.stem}-{index:04d}"
        if entry_id in source_ids:
            raise SystemExit(f"Duplicate source story ID: {entry_id}")
        source_ids.add(entry_id)
        if entry_id not in selected_ids:
            continue
        entries.append(
            {
                "id": entry_id,
                "displayText": row["sentence"],
                "promptText": build_prompt_text("", entry_type="sentence"),
                "answerJyutping": row["jyutping"],
                "gloss": str(row.get("gloss", "")).strip(),
                "notes": "",
                "usageTip": str(row.get("usageTip", "")).strip(),
                "exampleSentence": "",
                "exampleTranslation": "",
                "entryType": "sentence",
                "category": row["category"],
                "groupId": entry_id,
                "tone": 0,
                "audioAsset": None,
                "sourceLabel": "curated",
            }
        )
    return entries


def load_all_entries() -> list[dict]:
    entries: list[dict] = []
    for path in sorted(CONTENT_DIR.glob("*_bank.json")):
        name = path.stem.lower()
        entry_type = (
            "sentence"
            if "sentence" in name
            else "expression"
            if any(token in name for token in ("expression", "slang", "conversation"))
            else "word"
        )
        entries.extend(load_entries(path, entry_type))
    selected_ids, excluded_ids = story_selection()
    found_ids: set[str] = set()
    source_ids: set[str] = set()
    for path in sorted(SENTENCE_BANK_DIR.glob("*.json")):
        selected_entries = load_independent_sentence_entries(path, selected_ids, source_ids)
        found_ids.update(entry["id"] for entry in selected_entries)
        entries.extend(selected_entries)
    if source_ids != selected_ids | excluded_ids:
        unknown = sorted(source_ids - selected_ids - excluded_ids)
        stale = sorted((selected_ids | excluded_ids) - source_ids)
        raise SystemExit(f"Story selection/source mismatch: {len(unknown)} unlisted, {len(stale)} missing IDs")
    if found_ids != selected_ids:
        missing = sorted(selected_ids - found_ids)
        raise SystemExit(f"Active story IDs missing from source: {missing[:10]}")
    reviewed_ids = reviewed_sentence_entry_ids()
    for entry in entries:
        if entry["id"] in reviewed_ids:
            entry["qualityPriority"] = 1
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
