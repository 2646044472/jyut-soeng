#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUNDLE_PATH = ROOT / "app" / "src" / "main" / "assets" / "builtin" / "content.json"
ASSET_ROOT = ROOT / "app" / "src" / "main" / "assets"


def main() -> None:
    bundle = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))
    entries = bundle["entries"]
    if len(entries) < 36:
        raise SystemExit(f"Expected at least 36 entries, found {len(entries)}")

    ids = [entry["id"] for entry in entries]
    duplicates = [entry_id for entry_id, count in Counter(ids).items() if count > 1]
    if duplicates:
        raise SystemExit(f"Duplicate ids: {duplicates[:10]}")

    entry_types = Counter(entry.get("entryType", "word") for entry in entries)
    if entry_types.get("word", 0) < 20:
        raise SystemExit("Need at least 20 word correction entries.")
    if entry_types.get("expression", 0) < 10:
        raise SystemExit("Need at least 10 expression/slang entries.")

    for entry in entries:
        for key in ("displayText", "promptText", "answerJyutping", "gloss", "notes", "category"):
            if not str(entry.get(key, "")).strip():
                raise SystemExit(f"Entry {entry.get('id')} missing required field: {key}")
        audio_asset = entry.get("audioAsset")
        if audio_asset:
            audio_path = ASSET_ROOT / audio_asset
            if not audio_path.exists():
                raise SystemExit(f"Missing audio asset: {audio_path}")

    print(f"Validated {len(entries)} entries.")


if __name__ == "__main__":
    main()
