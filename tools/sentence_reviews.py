#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REVIEW_PATH = ROOT / "content" / "sentence_human_reviews.json"
REVIEWED_FIELDS = (
    "id",
    "displayText",
    "answerJyutping",
    "gloss",
    "notes",
    "usageTip",
    "exampleSentence",
    "category",
)


def content_fingerprint(entry: dict) -> str:
    reviewed = {field: entry.get(field, "") for field in REVIEWED_FIELDS}
    payload = json.dumps(reviewed, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def require_human_reviews(entries: list[dict], path: Path = REVIEW_PATH) -> None:
    if not path.is_file():
        raise ValueError(f"Human sentence review file is missing: {path}")
    document = json.loads(path.read_text(encoding="utf-8"))
    records = document.get("reviews") if isinstance(document, dict) else None
    if not isinstance(records, list):
        raise ValueError("Human sentence reviews must be a list")

    sentences = {entry["id"]: entry for entry in entries if entry.get("entryType") == "sentence"}
    seen: set[str] = set()
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Each human sentence review must be an object")
        entry_id = record.get("id")
        if not isinstance(entry_id, str) or not entry_id:
            raise ValueError("Each human sentence review needs an id")
        if entry_id in seen:
            raise ValueError(f"Duplicate human review: {entry_id}")
        seen.add(entry_id)
        if entry_id not in sentences:
            raise ValueError(f"Human review refers to an unknown sentence: {entry_id}")
        if record.get("humanAuthored") is not True:
            raise ValueError(f"Sentence {entry_id} has no human-authorship attestation")
        if any(
            not isinstance(record.get(field), str) or not record[field].strip()
            for field in ("author", "reviewer")
        ):
            raise ValueError(f"Sentence {entry_id} needs a named author and reviewer")
        try:
            reviewed_at = record["reviewedAt"]
            if date.fromisoformat(reviewed_at).isoformat() != reviewed_at:
                raise ValueError("Date must use YYYY-MM-DD")
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Sentence {entry_id} needs an ISO review date") from exc
        if record.get("contentSha256") != content_fingerprint(sentences[entry_id]):
            raise ValueError(f"Sentence {entry_id} changed since human review")

    missing = sentences.keys() - seen
    if missing:
        raise ValueError(f"Missing human reviews for {len(missing)} sentences; first: {sorted(missing)[0]}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a sentence fingerprint after human review")
    parser.add_argument("sentence_id")
    args = parser.parse_args()

    from build_assets import load_all_entries

    matches = [entry for entry in load_all_entries() if entry["id"] == args.sentence_id]
    if len(matches) != 1 or matches[0]["entryType"] != "sentence":
        parser.error("sentence_id must identify exactly one source sentence")
    print(content_fingerprint(matches[0]))


if __name__ == "__main__":
    main()
