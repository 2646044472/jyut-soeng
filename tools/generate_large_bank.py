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
TARGET_WORD_COUNT = 2550
TARGET_EXPRESSION_COUNT = 560

ZH_RE = re.compile(r"[\u4e00-\u9fff]{2,5}")
PRON_RE = re.compile(r"[a-z1-6 ]+")

WORD_PRIORITY_CHARS = set("學工講話語口讀音正校準達情意識進資料效率溝通表達進度節奏情緒處理判斷邏輯方法關係感受時間工作學習安排版本結果方向功能練習聲母韻母語氣自然熟練問題做法資料通知處境人心表現選擇方式狀態感覺計畫經驗反應改善理解分析決定完成確認目標")
COLLOQUIAL_CORE_MARKERS = set("唔冇咁啲嘢咗嚟喺嗰咩乜喎啫咋呀哋畀俾佢")
COLLOQUIAL_ACTION_MARKERS = set("搞諗傾睇執扮頂窒頹爆癮篤扯駁搲磨拗扭撐收")
COLLOQUIAL_CONTEXT_MARKERS = set("氣手腳口面眼心聲條句頭尾勢款場")
EMOTION_MARKERS = set("驚嬲煩尷頹怯火氣悶爽癲")
BOOKISH_CHARS = set("詩書禮義寰礡饈璧樞籌纓寂羈晦疆")

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

EXCLUDED_EXPRESSIONS = {
    "係呀",
    "係呢",
    "係啦",
    "係咩",
    "係咪",
    "係唔係",
    "但係",
    "你呢",
    "你哋",
    "佢哋",
    "人哋",
    "一啲",
    "乜嘢",
    "做咩",
    "做嘢",
    "冇嘢",
    "冇事",
    "冇乜",
    "冇問題",
    "冇所謂",
    "有冇計",
}

BLACKLIST_WORD_FRAGMENTS = ("翳", "黐", "躝", "𨋢", "厴", "挐", "掕")
PROFANITY_FRAGMENTS = ("老母", "仆街", "扑街", "屎", "閪", "鳩", "撚", "雞蟲", "風月", "妓", "賤", "鹹濕", "咸濕", "去死", "波大")
BOOKISH_FRAGMENTS = ("珍饈", "垂手", "高手如雲", "防毒", "心術", "立心", "社會現象", "正面回應", "善意提醒", "外科口罩", "人口販賣", "氣勢磅礡")
WEAK_EXPRESSION_FRAGMENTS = (
    "釐",
    "咑",
    "痾",
    "矺",
    "祇",
    "擳",
    "龜逗",
    "碇",
    "卓",
    "挐掕",
    "補鑊",
    "順超",
    "垃集",
    "埗到",
    "依郁",
    "氣候",
    "氣體",
    "節氣",
    "氣旋",
    "干雲",
    "方剛",
    "平氣和",
    "死氣沉沉",
    "豪氣",
    "浩氣",
    "臭氣熏天",
    "傾國傾城",
    "稟神",
    "監粗",
)


def load_existing_display_texts() -> set[str]:
    existing = set(EXCLUDED_WORDS)
    existing.update(EXCLUDED_EXPRESSIONS)
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


def count_hits(word: str, charset: set[str]) -> int:
    return sum(1 for ch in word if ch in charset)


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
    if any(token in word for token in ("嬲", "驚", "煩", "頹", "怯", "火", "尷", "窒住條氣", "頂唔順")):
        return "情绪表达"
    if any(token in word for token in ("講", "話", "問", "答", "駁", "傾", "聲")):
        return "口语场景"
    if any(token in word for token in ("搞掂", "手尾", "收科", "埋單", "交代")):
        return "工作场景"
    if count_hits(word, COLLOQUIAL_CORE_MARKERS) > 0:
        return "俚语表达"
    return "日常表达"


def build_usage_tip(word: str, category: str, kind: str) -> str:
    if kind == "expression":
        return {
            "俚语表达": "多放在熟人闲聊、吐槽和即时反应里。",
            "口语场景": "适合直接放进对话里，句子不用太长。",
            "情绪表达": "多放在讲自己感觉或评价别人状态时。",
            "工作场景": "适合放在讲进度、安排和处理方式时。",
        }.get(category, "日常开口时可以直接带出来。")
    if category == "工作场景":
        return "适合放在开会、交代事情和讲做法时。"
    if category == "学习场景":
        return "适合放在提问、复述和说明时。"
    if category == "情绪表达":
        return "多放在讲感觉、情绪变化和反应时。"
    if category == "口语场景":
        return "对话里很常见，重点是读得自然。"
    return "日常句子里直接用就可以。"


def build_meaning(word: str, category: str, kind: str) -> str:
    if kind == "expression":
        return {
            "俚语表达": "偏口语的说法，常用来讲状态、场面或反应。",
            "口语场景": "对话里常见的说法，听起来会比较自然。",
            "情绪表达": "用来表达感觉、情绪或当下反应。",
            "工作场景": "多用于交代事情、讲进度或讲处理方式。",
        }.get(category, f"常见表达，日常讲话时可以自然用「{word}」。")
    if category == "工作场景":
        return "工作沟通里常见的词。"
    if category == "学习场景":
        return "学习和说明语境里常用的词。"
    if category == "情绪表达":
        return "常用来讲感受、状态或反应。"
    if category == "口语场景":
        return "日常讲话常见词，适合拿来练顺口。"
    return f"常用词，适合放进句子里练熟「{word}」。"


def build_examples(word: str, category: str, kind: str) -> str:
    if kind == "expression":
        if category == "情绪表达":
            return f"我一听到呢件事，就觉得可以讲「{word}」。\n想表达自己状态时，可以直接用「{word}」。"
        if category == "口语场景":
            return f"朋友倾偈时，可以直接讲「{word}」。\n想讲得自然一点时，就顺手带出「{word}」。"
        if category == "工作场景":
            return f"讲安排或者进度时，可以用「{word}」。\n想交代得简洁一点，就直接讲「{word}」。"
        return f"遇到类似情况时，可以直接讲「{word}」。\n下次开口时，试住自然带出「{word}」。"
    if category == "工作场景":
        return f"讲工作内容时，可以用「{word}」。\n你可以试住用「{word}」讲一次完整句子。"
    if category == "学习场景":
        return f"今日先练熟「{word}」呢个词。\n讲学习安排时，可以直接用「{word}」。"
    if category == "情绪表达":
        return f"我而家个状态有啲似「{word}」。\n想讲感觉时，就用「{word}」去讲。"
    if category == "口语场景":
        return f"平时开口讲话时，经常会用到「{word}」。\n你可以试住用「{word}」讲一次。"
    return f"你可以先用「{word}」讲一次完整句子。\n再试多次，把「{word}」读得更顺一点。"


def build_rows(pairs: list[tuple[str, str]], kind: str, start_index: int = 1) -> list[dict]:
    rows = []
    for index, (word, pronunciation) in enumerate(pairs, start=start_index):
        category = classify_expression_category(word) if kind == "expression" else classify_word_category(word)
        rows.append(
            {
                "id": f"gen-{kind}-{index:04d}",
                "displayText": word,
                "answerJyutping": pronunciation,
                "gloss": build_meaning(word, category, kind),
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


def score_word(word: str) -> tuple[int, int, int]:
    hits = count_hits(word, WORD_PRIORITY_CHARS)
    distinct = len(set(word))
    return (-hits, -distinct, len(word))


def should_keep_word_candidate(word: str) -> bool:
    if any(fragment in word for fragment in BLACKLIST_WORD_FRAGMENTS):
        return False
    if len(word) >= 3 and word[0] == word[1]:
        return False
    return True


def expression_colloquial_score(word: str) -> int:
    return (
        count_hits(word, COLLOQUIAL_CORE_MARKERS) * 6
        + count_hits(word, COLLOQUIAL_ACTION_MARKERS) * 4
        + count_hits(word, EMOTION_MARKERS) * 3
        + count_hits(word, COLLOQUIAL_CONTEXT_MARKERS)
        + (2 if 3 <= len(word) <= 4 else 1)
        + (len(word) - len(set(word)))
    )


def score_expression(word: str) -> tuple[int, int, str]:
    penalty = count_hits(word, BOOKISH_CHARS) * 4
    if word.startswith(("一", "你", "佢", "我", "依", "呢")):
        penalty += 2
    return (-(expression_colloquial_score(word) - penalty), len(word), word)


def should_keep_expression_candidate(word: str) -> bool:
    if len(word) < 3 or len(word) > 5:
        return False
    if word in EXCLUDED_EXPRESSIONS:
        return False
    if any(fragment in word for fragment in PROFANITY_FRAGMENTS):
        return False
    if any(fragment in word for fragment in BOOKISH_FRAGMENTS):
        return False
    if any(fragment in word for fragment in WEAK_EXPRESSION_FRAGMENTS):
        return False
    if word.startswith(("冇有", "一唔", "之唔")):
        return False
    if word.endswith(("唔", "都", "處")):
        return False
    strong_hits = count_hits(word, COLLOQUIAL_CORE_MARKERS)
    action_hits = count_hits(word, COLLOQUIAL_ACTION_MARKERS)
    emotion_hits = count_hits(word, EMOTION_MARKERS)
    context_hits = count_hits(word, COLLOQUIAL_CONTEXT_MARKERS)
    if strong_hits == 0 and action_hits < 2:
        return False
    if strong_hits == 0 and count_hits(word, BOOKISH_CHARS) > 0:
        return False
    if strong_hits == 0 and action_hits == 0 and context_hits == 0:
        return False
    if word.endswith(("場所", "現象", "功能", "口罩")):
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

        if should_keep_expression_candidate(normalized_word):
            expression_candidates.append((normalized_word, pronunciation))
            continue

        if (
            len(normalized_word) >= 3
            and has_priority_chars(normalized_word, WORD_PRIORITY_CHARS)
            and should_keep_word_candidate(normalized_word)
        ):
            word_candidates.append((normalized_word, pronunciation))

    word_candidates = sorted(word_candidates, key=lambda item: score_word(item[0]))
    word_candidates = word_candidates[: max(TARGET_WORD_COUNT * 3, TARGET_WORD_COUNT)]
    random.Random(2646044472).shuffle(word_candidates)
    selected_words = word_candidates[:TARGET_WORD_COUNT]

    expression_candidates = sorted(expression_candidates, key=lambda item: score_expression(item[0]))
    expression_candidates = expression_candidates[: max(TARGET_EXPRESSION_COUNT * 4, TARGET_EXPRESSION_COUNT)]
    random.Random(2646044473).shuffle(expression_candidates)
    selected_expressions = expression_candidates[:TARGET_EXPRESSION_COUNT]

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
