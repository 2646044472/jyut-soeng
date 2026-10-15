#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from story_quality_progress import audit, row_digest

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
SENTENCE_BANK_DIR = CONTENT_DIR / "sentence_bank"
OUTPUT_PATH = ROOT / "app" / "src" / "main" / "assets" / "builtin" / "content.json"


def reviewed_story_ids(root: Path = ROOT) -> set[str]:
    """Only matching, fully reviewed ledger rows can receive the runtime priority flag."""
    reviews = json.loads((root / "STORY_LANGUAGE_REVIEW.json").read_text(encoding="utf-8"))
    ids: set[str] = set()
    seen: set[tuple[str, int]] = set()
    sources: dict[str, list[dict]] = {}
    for review in reviews:
        file, index = review["file"], review["index"]
        key = (file, index)
        if key in seen:
            raise ValueError(f"Duplicate language review: {key}")
        seen.add(key)
        path = root / file
        independent = path.parent == root / "content" / "sentence_bank"
        if not independent and path not in (root / "content").glob("*sentence*_bank.json"):
            raise ValueError(f"Language review is not a sentence source: {file}")
        if file not in sources:
            sources[file] = json.loads(path.read_text(encoding="utf-8"))
        row = sources[file][index]
        dimensions = ("naturalness", "distinct_plot", "jyutping_readings_and_tones", "complete_gloss")
        if review["sha256"] != row_digest(row) or not all(review.get(k) is True for k in dimensions):
            raise ValueError(f"Unverified or stale language review: {key}")
        if failures := audit(row, selected=not independent):
            raise ValueError(f"Reviewed story fails acceptance: {key}: {failures}")
        entry_id = f"sentence-bank-{path.stem}-{index + 1:04d}" if independent else row["id"]
        if entry_id in ids:
            raise ValueError(f"Duplicate reviewed story ID: {entry_id}")
        ids.add(entry_id)
    return ids


def apply_story_reviews(
    entries: list[dict],
    reviewed_ids: set[str],
    baseline: list[dict] | None = None,
) -> list[dict]:
    """During the migration, retain packaged text for sentences still awaiting review."""
    baseline_by_id = {entry["id"]: entry for entry in baseline} if baseline is not None else None
    output = []
    for entry in entries:
        reviewed = entry["entryType"] == "sentence" and entry["id"] in reviewed_ids
        if entry["entryType"] == "sentence" and not reviewed and baseline_by_id is not None:
            if entry["id"] not in baseline_by_id:
                raise ValueError(f"No previously packaged sentence for unreviewed ID: {entry['id']}")
            entry = baseline_by_id[entry["id"]]
        packaged = {**entry}
        if reviewed:
            packaged["storyReviewed"] = True
        else:
            packaged.pop("storyReviewed", None)
        output.append(packaged)
    missing = reviewed_ids - {entry["id"] for entry in output if entry.get("storyReviewed", False)}
    if missing:
        raise ValueError(f"Reviewed stories missing from bundle: {sorted(missing)}")
    return output


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


def load_independent_sentence_entries(path: Path) -> list[dict]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    entries: list[dict] = []
    for index, row in enumerate(rows, start=1):
        entry_id = f"sentence-bank-{path.stem}-{index:04d}"
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
    for path in sorted(SENTENCE_BANK_DIR.glob("*.json")):
        entries.extend(load_independent_sentence_entries(path))
    return entries


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reviewed-stories-only",
        action="store_true",
        help="Package reviewed story upgrades; retain previously bundled text for other sentences.",
    )
    args = parser.parse_args()
    baseline = None
    if args.reviewed_stories_only:
        baseline = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))["entries"]
    approved_ids = reviewed_story_ids()
    entries = apply_story_reviews(load_all_entries(), approved_ids, baseline)
    for index, entry in enumerate(entries, start=1):
        entry["sortOrder"] = index
    bundle = {
        "version": datetime.now(timezone.utc).strftime("%Y.%m.%d.%H%M%S"),
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "entries": entries,
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(bundle, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(entries)} entries to {OUTPUT_PATH}")
    print(f"Included {len(approved_ids)} reviewed story upgrades")


if __name__ == "__main__":
    main()
