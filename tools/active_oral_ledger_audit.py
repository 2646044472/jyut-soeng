#!/usr/bin/env python3
"""Read-only audit for active oral-review counts, row hashes, and app mirrors.

This helper only reads project JSON. It never creates, translates, or rewrites
story language. Canonical source identity is
``sentence-bank-{Path(file).stem}-{index + 1:04d}``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SELECTION_PATH = ROOT / "content" / "story_library_selection.json"
V2_PATH = ROOT / "STORY_QUALITY_REVALIDATION.json"
ORAL_PATH = ROOT / "STORY_QUALITY_ORAL_REAUDIT.json"
APP_PATH = ROOT / "app" / "src" / "main" / "assets" / "builtin" / "content.json"
MIRROR_FIELDS = {
    "sentence": "displayText",
    "jyutping": "answerJyutping",
    "gloss": "gloss",
    "usageTip": "usageTip",
    "category": "category",
}
VALID_STATUSES = {"pass", "needs_revision", "pending"}


def read_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def row_digest(row: dict) -> str:
    payload = json.dumps(
        row, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def canonical_story_id(file: str, index: int) -> str:
    return f"sentence-bank-{Path(file).stem}-{index + 1:04d}"


def indexed_records(ledger: dict, errors: list[str], label: str) -> dict[tuple[str, int], dict]:
    indexed: dict[tuple[str, int], dict] = {}
    for record in ledger.get("cards", []):
        key = (record.get("file", ""), record.get("index", -1))
        if key in indexed:
            errors.append(f"duplicate {label} record: {key}")
        indexed[key] = record
    return indexed


def audit(show_topics: bool = False) -> tuple[dict, list[str]]:
    errors: list[str] = []
    selection = read_json(SELECTION_PATH)
    v2 = read_json(V2_PATH)
    oral = read_json(ORAL_PATH)
    app = read_json(APP_PATH)
    active_ids = set(selection.get("active_ids", []))
    if len(active_ids) != selection.get("target_active_cards"):
        errors.append("active ID count does not match target_active_cards")

    v2_by_key = indexed_records(v2, errors, "V2")
    oral_by_key = indexed_records(oral, errors, "oral")
    id_to_source: dict[str, tuple[str, int, dict]] = {}
    source_keys: set[tuple[str, int]] = set()
    for source_path in sorted((ROOT / "content" / "sentence_bank").glob("*.json")):
        relative = source_path.relative_to(ROOT).as_posix()
        rows = read_json(source_path)
        for index, row in enumerate(rows):
            key = (relative, index)
            source_keys.add(key)
            story_id = canonical_story_id(relative, index)
            if story_id in id_to_source:
                errors.append(f"duplicate canonical source ID: {story_id}")
            id_to_source[story_id] = (relative, index, row)
            digest = row_digest(row)
            v2_record = v2_by_key.get(key)
            oral_record = oral_by_key.get(key)
            if v2_record is None:
                errors.append(f"missing V2 record: {key}")
            elif v2_record.get("status") in {"pass", "needs_revision"} and v2_record.get("v2_sha256") != digest:
                errors.append(f"stale V2 hash: {story_id}")
            if oral_record is None:
                errors.append(f"missing oral record: {key}")
            elif oral_record.get("status") in {"pass", "needs_revision"} and oral_record.get("source_sha256") != digest:
                errors.append(f"stale oral hash: {story_id}")

    if set(v2_by_key) != source_keys:
        errors.append("V2 ledger keys do not match source rows")
    if set(oral_by_key) != source_keys:
        errors.append("oral ledger keys do not match source rows")
    missing_active = sorted(active_ids - id_to_source.keys())
    if missing_active:
        errors.append(f"active IDs missing source rows: {missing_active[:5]}")

    active_v2_counts: Counter[str] = Counter()
    active_oral_counts: Counter[str] = Counter()
    active_topic_counts: Counter[str] = Counter()
    for story_id in sorted(active_ids & id_to_source.keys()):
        relative, index, _row = id_to_source[story_id]
        key = (relative, index)
        v2_record = v2_by_key[key]
        oral_record = oral_by_key[key]
        active_v2_counts[v2_record.get("status", "unknown")] += 1
        status = oral_record.get("status", "unknown")
        active_oral_counts[status] += 1
        if status not in VALID_STATUSES:
            errors.append(f"unknown active oral status {status!r}: {story_id}")
        active_topic_counts.update(oral_record.get("topic_notes", []))

    expected_v2 = {key: active_v2_counts.get(key, 0) for key in ("pass", "needs_revision", "pending")}
    expected_oral = {key: active_oral_counts.get(key, 0) for key in ("pass", "needs_revision", "pending")}
    if selection.get("active_v2_status_counts") != expected_v2:
        errors.append("selection active V2 counts are stale")
    if selection.get("active_oral_reaudit_status_counts") != expected_oral:
        errors.append("selection active oral counts are stale")
    if selection.get("active_oral_topic_note_counts_nonexclusive") != dict(sorted(active_topic_counts.items())):
        errors.append("selection active oral topic-note counts are stale")

    app_entries = app.get("entries", [])
    app_by_id = {entry.get("id"): entry for entry in app_entries}
    if len(app_by_id) != len(app_entries):
        errors.append("duplicate IDs in app bundle")
    missing_app = sorted(active_ids - app_by_id.keys())
    if missing_app:
        errors.append(f"active IDs missing app mirrors: {missing_app[:5]}")
    for story_id in sorted(active_ids & id_to_source.keys() & app_by_id.keys()):
        source_row = id_to_source[story_id][2]
        app_row = app_by_id[story_id]
        for source_field, app_field in MIRROR_FIELDS.items():
            if app_row.get(app_field) != source_row.get(source_field):
                errors.append(f"app mirror mismatch {story_id}: {source_field}->{app_field}")

    summary = {
        "active_ids": len(active_ids),
        "source_rows": len(source_keys),
        "active_v2_status_counts": expected_v2,
        "active_oral_status_counts": expected_oral,
        "active_oral_topic_note_types": len(active_topic_counts),
        "active_oral_topic_note_tags": sum(active_topic_counts.values()),
        "app_entries": len(app_entries),
        "errors": errors,
    }
    if show_topics:
        summary["active_oral_topic_note_counts_nonexclusive"] = dict(sorted(active_topic_counts.items()))
    return summary, errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topics", action="store_true", help="print every active topic-note count")
    args = parser.parse_args()
    summary, errors = audit(show_topics=args.topics)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    sys.exit(1 if errors else 0)
