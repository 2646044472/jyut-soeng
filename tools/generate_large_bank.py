#!/usr/bin/env python3
from __future__ import annotations

import json
import random
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORDS_OUTPUT_PATH = ROOT / "content" / "generated_words_bank.json"
EXPRESSIONS_OUTPUT_PATH = ROOT / "content" / "generated_expressions_bank.json"
WORDS_HK_WORDLIST_URL = "https://words.hk/faiman/analysis/wordslist.json"
TARGET_WORD_COUNT = 2900
TARGET_EXPRESSION_COUNT = 160

ZH_RE = re.compile(r"[\u4e00-\u9fff]{2,4}")
PRON_RE = re.compile(r"[a-z1-6 ]+")

WORD_PRIORITY_CHARS = set("學工講話語口讀音正校準達情意識進資料效率溝通表達進度節奏情緒處理判斷邏輯方法關係感受時間工作學習安排版本結果方向功能練習聲母韻母語氣自然熟練問題做法資料通知處境人心表現選擇方式狀態感覺計畫經驗反應改善理解分析決定完成確認目標")
EXPRESSION_PRIORITY_CHARS = set("講話情理意會心口氣手腳場面節奏感覺狀態關係處境意味")
EXCLUDED_WORDS = {
    "今日",
    "而家",
    "點樣",
    "點解",
    "明白",
    "朋友",
    "香港",
    "廣東話",
    "食飯",
    "飲水",
    "返工",
    "放工",
    "開心",
    "擔心",
    "天氣",
    "落雨",
    "學校",
    "醫院",
    "老師",
    "容易",
    "一定",
    "緊要",
    "其實",
    "小心",
    "多謝",
    "唔該",
    "唔好意思",
    "冇問題",
    "知道",
    "覺得",
    "準備",
    "上堂",
}

BLACKLIST_WORD_FRAGMENTS = ("翳", "黐", "躝", "𨋢")


def load_existing_display_texts() -> set[str]:
    existing = set(EXCLUDED_WORDS)
    for path in ROOT.glob("content/*_bank.json"):
        if path.name in {WORDS_OUTPUT_PATH.name, EXPRESSIONS_OUTPUT_PATH.name}:
            continue
        rows = json.loads(path.read_text(encoding="utf-8"))
        for row in rows:
            text = str(row.get("displayText") or "").strip()
            if text:
                existing.add(text)
    return existing


def fetch_words_hk() -> dict[str, list[str]]:
    with urllib.request.urlopen(WORDS_HK_WORDLIST_URL, timeout=60) as response:
        payload = json.load(response)
    if not isinstance(payload, dict):
        raise SystemExit("Unexpected words.hk wordslist shape")
    return payload


def normalize_pronunciation(values: object) -> str:
    if not isinstance(values, list):
        return ""
    for item in values:
        if isinstance(item, str):
            normalized = item.strip().lower()
            if normalized and PRON_RE.fullmatch(normalized):
                return normalized
    return ""


def classify_word_category(word: str) -> str:
    if any(token in word for token in ("學", "課", "老師", "學生")):
        return "学习场景"
    if any(token in word for token in ("工", "資料", "進度", "效率", "整合", "交代", "處理", "方案")):
        return "工作场景"
    if any(token in word for token in ("情", "心", "緊張", "擔", "怕", "怒", "喜", "悲")):
        return "情绪表达"
    if any(token in word for token in ("講", "話", "答", "問", "聽", "說")):
        return "口语场景"
    if any(token in word for token in ("時間", "今日", "明日", "最近", "即時")):
        return "时间表达"
    if len(word) == 4:
        return "进阶表达"
    return "进阶常用词"


def classify_expression_category(word: str) -> str:
    if any(token in word for token in ("唔", "咩", "喇", "啦", "啫", "咗", "吓")):
        return "俚语表达"
    if any(token in word for token in ("講", "話", "答", "聽")):
        return "口语场景"
    if any(token in word for token in ("心", "情", "緊張", "驚", "怒")):
        return "情绪表达"
    return "日常表达"


def build_usage_tip(word: str, category: str, kind: str) -> str:
    if kind == "expression":
        return f"这是偏口语或进阶说法，重点是整串自然读顺：{word}。"
    if category == "工作场景":
        return f"这个词在工作沟通里很常见，适合用来练更自然的语流：{word}。"
    if category == "学习场景":
        return f"这个词很适合放进学习语境里练熟，重点是把整串读顺：{word}。"
    if category == "情绪表达":
        return f"这是表达状态和感觉时很实用的说法，适合练情绪语气：{word}。"
    if category == "口语场景":
        return f"这是偏口语的说法，练的重点是自然开口，不要太书面：{word}。"
    return f"这是中高级常用词，适合拿来练稳定开口和完整 Jyutping：{word}。"


def build_examples(word: str, category: str, kind: str) -> str:
    if kind == "expression":
        return f"最近我成日会听到人讲「{word}」。\n下次开口时，你可以试住自然咁带出「{word}」。"
    if category == "工作场景":
        return f"呢个词喺工作场景好常用：{word}。\n你可以试住用「{word}」去讲一次。"
    if category == "学习场景":
        return f"我想先练熟「{word}」呢个词。\n你可以试住用「{word}」做今日学习例句。"
    if category == "情绪表达":
        return f"我而家个感觉就似「{word}」。\n讲到情绪时，用「{word}」会好自然。"
    if category == "口语场景":
        return f"日常对话里，呢个词可以直接讲成「{word}」。\n你开口时试下自然咁带出「{word}」。"
    return f"呢个词本身就值得练顺口：「{word}」。\n下次讲到相关情况，你可以直接试住用「{word}」。"


def build_rows(pairs: list[tuple[str, str]], kind: str, start_index: int = 1) -> list[dict]:
    rows = []
    for index, (word, pronunciation) in enumerate(pairs, start=start_index):
        category = classify_expression_category(word) if kind == "expression" else classify_word_category(word)
        rows.append(
            {
                "id": f"gen-{kind}-{index:04d}",
                "displayText": word,
                "answerJyutping": pronunciation,
                "gloss": "",
                "notes": "",
                "usageTip": build_usage_tip(word, category, kind),
                "exampleSentence": build_examples(word, category, kind),
                "exampleTranslation": "",
                "category": category,
            }
        )
    return rows


def has_priority_chars(word: str, charset: set[str]) -> bool:
    return any(ch in charset for ch in word)


def score_word(word: str, charset: set[str]) -> tuple[int, int, int]:
    hits = sum(1 for ch in word if ch in charset)
    distinct = len(set(word))
    return (-hits, -distinct, len(word))


def should_keep_word_candidate(word: str) -> bool:
    if any(fragment in word for fragment in BLACKLIST_WORD_FRAGMENTS):
        return False
    if len(word) >= 3 and word[0] == word[1]:
        return False
    return True


def main() -> None:
    existing = load_existing_display_texts()
    source = fetch_words_hk()
    word_candidates: list[tuple[str, str]] = []
    expression_candidates: list[tuple[str, str]] = []

    for word, values in source.items():
        if not isinstance(word, str):
            continue
        normalized_word = word.strip()
        if normalized_word in existing:
            continue
        if not ZH_RE.fullmatch(normalized_word):
            continue
        pronunciation = normalize_pronunciation(values)
        if not pronunciation:
            continue
        if len(normalized_word) == 4 and has_priority_chars(normalized_word, EXPRESSION_PRIORITY_CHARS):
            expression_candidates.append((normalized_word, pronunciation))
        elif (
            len(normalized_word) >= 3
            and has_priority_chars(normalized_word, WORD_PRIORITY_CHARS)
            and should_keep_word_candidate(normalized_word)
        ):
            word_candidates.append((normalized_word, pronunciation))

    word_candidates = sorted(word_candidates, key=lambda item: score_word(item[0], WORD_PRIORITY_CHARS))
    word_candidates = word_candidates[: max(TARGET_WORD_COUNT * 2, TARGET_WORD_COUNT)]
    random.Random(2646044472).shuffle(word_candidates)
    random.Random(2646044473).shuffle(expression_candidates)

    selected_words = word_candidates[:TARGET_WORD_COUNT]
    expression_set = {word for word, _ in selected_words}
    selected_expressions = [
        item for item in expression_candidates
        if item[0] not in expression_set
    ][:TARGET_EXPRESSION_COUNT]

    WORDS_OUTPUT_PATH.write_text(
        json.dumps(build_rows(selected_words, "word"), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    EXPRESSIONS_OUTPUT_PATH.write_text(
        json.dumps(build_rows(selected_expressions, "expression"), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(selected_words)} generated word entries to {WORDS_OUTPUT_PATH}")
    print(f"Wrote {len(selected_expressions)} generated expression entries to {EXPRESSIONS_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
