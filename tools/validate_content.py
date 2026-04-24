#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from meaning_rules import is_low_info_gloss
from meaning_rules import is_low_info_usage

ROOT = Path(__file__).resolve().parent.parent
BUNDLE_PATH = ROOT / "app" / "src" / "main" / "assets" / "builtin" / "content.json"
ASSET_ROOT = ROOT / "app" / "src" / "main" / "assets"
LEGACY_GENERATED_MARKERS = (
    "讲一次完整句子",
    "读得更顺一点",
    "试住自然带出",
    "遇到类似情况时，可以直接讲",
    "平时开口讲话时，经常会用到",
    "想讲感觉时，就用",
)
FORCED_SENTENCE_MARKERS = (
    "自己试着用",
    "自己开口说一次",
    "想一个会用到",
    "说一句",
)
LOW_INFO_CURATED_USAGE_MARKERS = (
    "适合拿来练",
    "适合拿来校正",
    "适合校正",
    "适合做基础稳定练习",
    "适合练自然收句",
    "值得反复校正",
    "越高频越值得校准",
    "重点是读得自然",
    "最容易听出前后差别",
)
GENERIC_CURATED_EXAMPLE_MARKERS = (
    "下次开口时，再用一次",
    "你可以再用一次",
    "把句子说顺一点",
    "把读法读顺",
    "讲一次完整句子",
    "读得更顺一点",
)
LOW_CONFIDENCE_GENERATED_WORD_FRAGMENTS = (
    "工時",
    "結構",
    "受孕",
    "表達式",
    "語音學",
    "音韻學",
    "流產",
    "通知金",
    "人臉識別",
    "分子料理",
    "心理變態",
    "心肺功能",
    "恆定狀態",
    "意識形態",
    "法定語言",
    "知識分子",
    "自然科學",
    "理工大學",
    "工業學校",
    "文法學校",
    "公開處決",
    "反式脂肪",
)
LOW_CONFIDENCE_GENERATED_EXPRESSION_FRAGMENTS = (
    "嚟神氣",
    "火冇貓",
    "唔聲唔聲",
    "唔嘢",
    "搭霎",
    "鬆化",
    "頂唔蒲",
    "嗅米氣",
    "冇脈",
    "冇掕",
    "呀支呀左",
    "乜乜七七",
    "乜乜柒柒",
    "乜乜物物",
    "啫啫煲",
    "啲啲震",
    "羊咩咩",
    "咁高咁大",
)


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
    if entry_types.get("expression", 0) < 1000:
        raise SystemExit("Need at least 1000 expression/slang entries.")

    for entry in entries:
        for key in ("displayText", "promptText", "answerJyutping", "usageTip", "exampleSentence", "category"):
            if not str(entry.get(key, "")).strip():
                raise SystemExit(f"Entry {entry.get('id')} missing required field: {key}")
        display_text = str(entry.get("displayText", "")).strip()
        gloss = str(entry.get("gloss", "")).strip()
        usage_tip = str(entry.get("usageTip", "")).strip()
        example_sentence = str(entry.get("exampleSentence", "")).strip()
        if is_low_info_gloss(gloss, display_text):
            raise SystemExit(f"Entry {entry.get('id')} still has low-information gloss: {gloss}")
        if is_low_info_usage(usage_tip):
            raise SystemExit(f"Entry {entry.get('id')} still has low-information usageTip: {usage_tip}")
        if entry.get("sourceLabel") == "generated":
            example_sentence = str(entry.get("exampleSentence", "")).strip()
            if any(marker in example_sentence for marker in LEGACY_GENERATED_MARKERS):
                raise SystemExit(f"Generated entry {entry.get('id')} still contains legacy fake example copy")
            if any(marker in example_sentence for marker in FORCED_SENTENCE_MARKERS):
                raise SystemExit(f"Generated entry {entry.get('id')} still pushes forced sentence-making")
            suspicious_markers = (
                LOW_CONFIDENCE_GENERATED_EXPRESSION_FRAGMENTS
                if entry.get("entryType") == "expression"
                else LOW_CONFIDENCE_GENERATED_WORD_FRAGMENTS
            )
            if any(marker in display_text for marker in suspicious_markers):
                raise SystemExit(f"Generated entry {entry.get('id')} still contains low-confidence wording: {display_text}")
        else:
            gloss = str(entry.get("gloss", "")).strip()
            example_lines = [line.strip() for line in example_sentence.splitlines() if line.strip()]
            if example_lines and all(display_text not in line for line in example_lines):
                raise SystemExit(f"Curated entry {entry.get('id')} exampleSentence never mentions displayText")
            if gloss == display_text:
                raise SystemExit(f"Curated entry {entry.get('id')} gloss still repeats displayText")
            if any(marker in usage_tip for marker in LOW_INFO_CURATED_USAGE_MARKERS):
                raise SystemExit(f"Curated entry {entry.get('id')} usageTip still reads like pronunciation filler")
            if any(marker in example_sentence for marker in GENERIC_CURATED_EXAMPLE_MARKERS):
                raise SystemExit(f"Curated entry {entry.get('id')} still contains fake follow-up example copy")
        audio_asset = entry.get("audioAsset")
        if audio_asset:
            audio_path = ASSET_ROOT / audio_asset
            if not audio_path.exists():
                raise SystemExit(f"Missing audio asset: {audio_path}")

    print(f"Validated {len(entries)} entries.")


if __name__ == "__main__":
    main()
