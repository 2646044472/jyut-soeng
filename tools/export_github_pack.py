#!/usr/bin/env python3
from __future__ import annotations

import shutil
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
    shutil.copytree(SOURCE_AUDIO, TARGET_ROOT / "audio" / "generated")
    print(f"Exported GitHub pack to {TARGET_ROOT}")


if __name__ == "__main__":
    main()
