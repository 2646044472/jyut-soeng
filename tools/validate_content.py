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
    if len(entries) != 240:
        raise SystemExit(f"Expected 240 entries, found {len(entries)}")

    ids = [entry["id"] for entry in entries]
    duplicates = [entry_id for entry_id, count in Counter(ids).items() if count > 1]
    if duplicates:
        raise SystemExit(f"Duplicate ids: {duplicates[:10]}")

    tones_per_group: dict[str, set[int]] = defaultdict(set)
    missing_audio: list[str] = []
    for entry in entries:
        tones_per_group[entry["groupId"]].add(int(entry["tone"]))
        audio_path = ASSET_ROOT / entry["audioAsset"]
        if not audio_path.exists():
            missing_audio.append(str(audio_path))

    incomplete_groups = {
        group_id: sorted(set(range(1, 7)) - tones)
        for group_id, tones in tones_per_group.items()
        if tones != set(range(1, 7))
    }
    if incomplete_groups:
        raise SystemExit(f"Incomplete tone ladders: {incomplete_groups}")
    if missing_audio:
        raise SystemExit(f"Missing audio assets: {missing_audio[:10]}")

    print(f"Validated {len(entries)} entries across {len(tones_per_group)} groups.")


if __name__ == "__main__":
    main()
