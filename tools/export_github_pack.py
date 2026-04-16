#!/usr/bin/env python3
from __future__ import annotations

import shutil
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE_BUNDLE = ROOT / "app" / "src" / "main" / "assets" / "builtin" / "content.json"
SOURCE_AUDIO = ROOT / "app" / "src" / "main" / "assets" / "audio" / "generated"
TARGET_ROOT = ROOT / "dist" / "github" / "canto-calibrator"


def main() -> None:
    if TARGET_ROOT.exists():
        shutil.rmtree(TARGET_ROOT)
    TARGET_ROOT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE_BUNDLE, TARGET_ROOT / "content.json")
    bundle = json.loads(SOURCE_BUNDLE.read_text(encoding="utf-8"))
    referenced_audio = sorted(
        {
            entry.get("audioAsset", "").replace("audio/generated/", "", 1)
            for entry in bundle.get("entries", [])
            if str(entry.get("audioAsset") or "").startswith("audio/generated/")
        }
    )
    if referenced_audio:
        target_audio_dir = TARGET_ROOT / "audio" / "generated"
        target_audio_dir.mkdir(parents=True, exist_ok=True)
        for relative_name in referenced_audio:
            source = SOURCE_AUDIO / relative_name
            if source.exists():
                shutil.copy2(source, target_audio_dir / relative_name)
    print(f"Exported GitHub pack to {TARGET_ROOT}")


if __name__ == "__main__":
    main()
