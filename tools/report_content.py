#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUNDLE_PATH = ROOT / "app" / "src" / "main" / "assets" / "builtin" / "content.json"


def main() -> None:
    bundle = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))
    entries = bundle["entries"]
    category_counts = Counter(entry["category"] for entry in entries)
    type_counts = Counter(entry.get("entryType", "word") for entry in entries)

    print(f"Bundle version: {bundle['version']}")
    print(f"Generated at: {bundle['generatedAt']}")
    print(f"Total entries: {len(entries)}")
    print("Entries per type:")
    for entry_type, count in sorted(type_counts.items()):
        print(f"  {entry_type}: {count}")
    print("Entries per category:")
    for category, count in sorted(category_counts.items()):
        print(f"  {category}: {count}")


if __name__ == "__main__":
    main()
