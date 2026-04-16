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
    if len(entries) < 3200:
        raise SystemExit(f"Expected at least 3200 entries, found {len(entries)}")

    ids = [entry["id"] for entry in entries]
    duplicates = [entry_id for entry_id, count in Counter(ids).items() if count > 1]
    if duplicates:
        raise SystemExit(f"Duplicate ids: {duplicates[:10]}")

    entry_types = Counter(entry.get("entryType", "word") for entry in entries)
    if entry_types.get("word", 0) < 2500:
        raise SystemExit("Need at least 2500 word correction entries.")
    if entry_types.get("expression", 0) < 500:
        raise SystemExit("Need at least 500 expression/slang entries.")

    for entry in entries:
        for key in ("displayText", "promptText", "answerJyutping", "usageTip", "exampleSentence", "category"):
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
