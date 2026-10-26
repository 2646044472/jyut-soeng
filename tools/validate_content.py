#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from meaning_rules import is_low_info_gloss
from meaning_rules import is_fake_example_sentence
from meaning_rules import is_low_info_usage

ROOT = Path(__file__).resolve().parent.parent
BUNDLE_PATH = ROOT / "app" / "src" / "main" / "assets" / "builtin" / "content.json"
ASSET_ROOT = ROOT / "app" / "src" / "main" / "assets"
STANDALONE_SENTENCE_PREFIX = "sentence-bank-"
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
MIN_CURATED_SENTENCE_HAN_COUNT = 220
MAX_CURATED_SENTENCE_HAN_COUNT = 320
MIN_LEGACY_CURATED_SENTENCE_LENGTH = 30
MIN_LEGACY_CURATED_SENTENCE_SYLLABLES = 28
MIN_CURATED_SENTENCE_SEGMENTS = 2
MIN_CURATED_SENTENCE_GLOSS_HAN_COUNT = 160
MIN_CURATED_SENTENCE_COUNT = 5000
JYUTPING_TOKEN = re.compile(r"[a-z]+[1-6]")
JYUTPING_ALLOWED_SEPARATORS = re.compile(r"[,，.。:：;；?!？！、「」『』“”\"'\s]")
HAN_CHARACTER = re.compile(
    r"[\u3400-\u9fff\uf900-\ufaff\U00020000-\U0002FA1F\U00030000-\U000323AF]"
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


def main(
    min_sentence_count: int = MIN_CURATED_SENTENCE_COUNT,
    require_story_upgrade: bool = False,
) -> None:
    bundle = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))
    entries = bundle["entries"]
    if len(entries) < 250:
        raise SystemExit(f"Expected at least 250 curated entries, found {len(entries)}")

    ids = [entry["id"] for entry in entries]
    duplicates = [entry_id for entry_id, count in Counter(ids).items() if count > 1]
    if duplicates:
        raise SystemExit(f"Duplicate ids: {duplicates[:10]}")

    entry_types = Counter(entry.get("entryType", "word") for entry in entries)
    if entry_types.get("word", 0) < 150:
        raise SystemExit("Need at least 150 curated word correction entries.")
    if entry_types.get("expression", 0) < 100:
        raise SystemExit("Need at least 100 curated daily expression entries.")
    if entry_types.get("sentence", 0) < min_sentence_count:
        raise SystemExit(
            f"Need at least {min_sentence_count} curated daily sentence entries; "
            f"found {entry_types.get('sentence', 0)}."
        )

    sentences = [entry for entry in entries if entry.get("entryType") == "sentence"]
    for field, label in (
        ("displayText", "opening"),
        ("gloss", "gloss"),
        ("notes", "notes"),
        ("usageTip", "usage tip"),
    ):
        values = (
            str(entry.get(field, "")).strip()[:18]
            if field == "displayText"
            else str(entry.get(field, "")).strip()
            for entry in sentences
        )
        repeated = [(text, count) for text, count in Counter(values).items() if text and count > 3]
        if repeated:
            text, count = repeated[0]
            raise SystemExit(f"Repeated sentence {label} ({count} times): {text}")

    for entry in entries:
        standalone_sentence = (
            entry.get("entryType") == "sentence"
            and str(entry.get("id", "")).startswith(STANDALONE_SENTENCE_PREFIX)
        )
        story_sentence = (
            entry.get("entryType") == "sentence"
            and str(entry.get("usageTip", "")).startswith("故事练习：")
        )
        required_fields = ["displayText", "promptText", "answerJyutping", "category"]
        if not standalone_sentence:
            required_fields.extend(("usageTip", "exampleSentence"))
        elif story_sentence:
            required_fields.append("usageTip")
        for key in required_fields:
            if not str(entry.get(key, "")).strip():
                raise SystemExit(f"Entry {entry.get('id')} missing required field: {key}")
        display_text = str(entry.get("displayText", "")).strip()
        gloss = str(entry.get("gloss", "")).strip()
        usage_tip = str(entry.get("usageTip", "")).strip()
        example_sentence = str(entry.get("exampleSentence", "")).strip()
        if entry.get("entryType") == "sentence":
            han_count = len(HAN_CHARACTER.findall(display_text))
            if require_story_upgrade and not story_sentence:
                raise SystemExit(f"Sentence {entry.get('id')} still awaits its story upgrade")
            if story_sentence:
                if not MIN_CURATED_SENTENCE_HAN_COUNT <= han_count <= MAX_CURATED_SENTENCE_HAN_COUNT:
                    raise SystemExit(
                        f"Sentence {entry.get('id')} has an unsupported story length: {han_count} Han characters"
                    )
                if "「" not in display_text or "」" not in display_text:
                    raise SystemExit(f"Sentence {entry.get('id')} needs direct dialogue")
                if len(HAN_CHARACTER.findall(gloss)) < MIN_CURATED_SENTENCE_GLOSS_HAN_COUNT:
                    raise SystemExit(f"Sentence {entry.get('id')} needs a complete Mandarin story translation")
                if re.search(r"[A-Za-z0-9]", display_text):
                    raise SystemExit(f"Sentence {entry.get('id')} contains unaligned Latin characters or digits")
                if not standalone_sentence and example_sentence != display_text:
                    raise SystemExit(f"Sentence {entry.get('id')} exampleSentence must match displayText")
                minimum_syllables = han_count
            elif standalone_sentence:
                if 60 <= han_count <= 90:
                    minimum_syllables = 22
                elif 100 <= han_count <= 130:
                    minimum_syllables = 100
                else:
                    raise SystemExit(f"Sentence {entry.get('id')} has an unsupported legacy length: {han_count}")
                if not gloss:
                    raise SystemExit(f"Sentence {entry.get('id')} is missing its Mandarin meaning")
            else:
                if len(display_text) < MIN_LEGACY_CURATED_SENTENCE_LENGTH:
                    raise SystemExit(f"Sentence {entry.get('id')} is too short for daily reading mode")
                minimum_syllables = MIN_LEGACY_CURATED_SENTENCE_SYLLABLES
            if story_sentence or standalone_sentence:
                if not re.search(r"[。？！.!?][」』”\"]?$", display_text):
                    raise SystemExit(f"Sentence {entry.get('id')} is missing ending punctuation")
            if story_sentence or not standalone_sentence:
                segment_count = sum(display_text.count(mark) for mark in ("，", "；", "？"))
                if segment_count < MIN_CURATED_SENTENCE_SEGMENTS:
                    raise SystemExit(f"Sentence {entry.get('id')} needs at least two conversational segments")
            syllable_count = len(
                JYUTPING_TOKEN.findall(str(entry.get("answerJyutping", "")).lower())
            )
            if syllable_count < minimum_syllables:
                raise SystemExit(f"Sentence {entry.get('id')} needs a complete Jyutping line")
            jyutping = str(entry.get("answerJyutping", "")).lower()
            residue = JYUTPING_ALLOWED_SEPARATORS.sub("", jyutping)
            tokens = JYUTPING_TOKEN.findall(jyutping)
            if not tokens or "".join(tokens) != residue:
                raise SystemExit(f"Sentence {entry.get('id')} contains non-Jyutping text")
            if not re.search(r"[A-Za-z0-9]", display_text) and syllable_count != han_count:
                raise SystemExit(f"Sentence {entry.get('id')} Jyutping must map one syllable to each Han character")
        if not standalone_sentence and is_low_info_gloss(gloss, display_text):
            raise SystemExit(f"Entry {entry.get('id')} still has low-information gloss: {gloss}")
        if not standalone_sentence and is_low_info_usage(usage_tip):
            raise SystemExit(f"Entry {entry.get('id')} still has low-information usageTip: {usage_tip}")
        if entry.get("sourceLabel") == "generated":
            raise SystemExit(f"Generated entry {entry.get('id')} is not allowed in the release bundle")
        elif not standalone_sentence:
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-sentences", type=int, default=MIN_CURATED_SENTENCE_COUNT)
    parser.add_argument("--require-story-upgrade", action="store_true", help="Require all sentence cards to pass full-story acceptance.")
    args = parser.parse_args()
    if args.min_sentences < 0:
        parser.error("--min-sentences must be nonnegative")
    main(args.min_sentences, require_story_upgrade=args.require_story_upgrade)
