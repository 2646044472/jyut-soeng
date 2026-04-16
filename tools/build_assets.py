#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED_PATH = ROOT / "content" / "seed_groups.json"
OUTPUT_PATH = ROOT / "app" / "src" / "main" / "assets" / "builtin" / "content.json"

TONE_INFO = {
    1: {"name": "高平", "gloss": "高位平调，适合抓住顶部平台。"},
    2: {"name": "高升", "gloss": "由中高区上扬到高位，检查升幅是否够清楚。"},
    3: {"name": "中平", "gloss": "中位平调，重点在于不要抬得过高。"},
    4: {"name": "低降", "gloss": "低位下降，避免尾部提前收扁。"},
    5: {"name": "低升", "gloss": "从低区回升，注意起点与终点的拉开。"},
    6: {"name": "低平", "gloss": "低位平调，强调稳定而不是松散。"},
}


def build_entries(seed_groups: list[dict]) -> list[dict]:
    entries: list[dict] = []
    for group in seed_groups:
        for tone, tone_info in TONE_INFO.items():
            entry_id = f"builtin-{group['groupId']}-{tone}"
            entries.append(
                {
                    "id": entry_id,
                    "displayText": f"{group['displayName']} · {tone_info['name']}",
                    "promptText": f"播放 {group['displayName']} 的参考轮廓后，选出对应 Jyutping。",
                    "answerJyutping": f"{group['groupId']}{tone}",
                    "gloss": f"{group['gloss']} {tone_info['gloss']}",
                    "notes": f"{group['notes']} 本资源为合成轮廓音，不是人声录音。",
                    "category": group["category"],
                    "groupId": group["groupId"],
                    "tone": tone,
                    "audioAsset": f"audio/generated/{entry_id}.wav",
                    "sourceLabel": "builtin",
                }
            )
    return entries


def main() -> None:
    seed_groups = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    entries = build_entries(seed_groups)
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
