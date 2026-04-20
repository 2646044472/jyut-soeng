#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORDS_OUTPUT_PATH = ROOT / "content" / "generated_words_bank.json"
EXPRESSIONS_OUTPUT_PATH = ROOT / "content" / "generated_expressions_bank.json"
WORDS_HK_WORDLIST_URL = "https://words.hk/faiman/analysis/wordslist.json"
TARGET_WORD_COUNT = 2550
TARGET_EXPRESSION_COUNT = 1000

ZH_RE = re.compile(r"[\u4e00-\u9fff]{2,6}")
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

BLACKLIST_WORD_FRAGMENTS = ("翳", "黀", "躝", "\U000282E2", "厴", "挑", "捕")
LOW_CONFIDENCE_WORD_FRAGMENTS = (
    "工時",
    "結構",
    "受孕",
    "流產",
    "表達式",
    "語音學",
    "音韻學",
    "人臉識別",
    "人口販賣",
    "人工呼吸",
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
    "通知金",
)
PROFANITY_FRAGMENTS = ("老母", "仆街", "扑街", "屎", "閪", "鳩", "撚", "屌", "雞蟲", "風月", "奷", "賤", "鹹濕", "咸濕", "去死", "波大")
BOOKISH_FRAGMENTS = ("珍饈", "垂手", "高手如雲", "防毒", "心術", "立心", "社會現象", "正面回應", "善意提醒", "外科口罩", "人口販賣", "氣勢磅礡")
WEAK_EXPRESSION_FRAGMENTS = (
    "釐",
    "咑",
    "疾",
    "矺",
    "祇",
    "擳",
    "龜逗",
    "碇",
    "卓",
    "挑捕",
    "補鐺",
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
LOW_CONFIDENCE_WORD_SUFFIXES = ("學", "學校", "效應", "作用", "結構", "工時")
EXPRESSION_STRONG_MARKERS = (
    "唔",
    "冇",
    "乜",
    "咁",
    "佢",
    "嗰",
    "嚟",
    "咗",
    "喎",
    "咩",
    "囉",
    "噉",
    "嘢",
    "喺",
)
EXPRESSION_SOFT_MARKERS = (
    "啲",
    "呢",
    "啦",
    "晒",
    "嘅",
    "尐",
    "嗮",
)
EXPRESSION_VARIANT_PENALTY_CHARS = set("戙疋噉厴砣説甫檯櫈柚")
EXPRESSION_VARIANT_BONUS_CHARS = set("棟匹咁掩陀說到枱凳遊")
EXTRA_COLLOQUIAL_EXPRESSIONS = {
    "傻傻戇戇",
    "傻傻更更",
    "手手腳腳",
    "頭頭尾尾",
    "口口聲聲",
    "快快手手",
    "神神怪怪",
    "神神經經",
    "老友鬼鬼",
    "迷迷懵懵",
    "迷迷糊糊",
    "問到口啞啞",
    "大大話話",
    "四四正正",
    "四腳爬爬",
    "安安份份",
    "安安靜靜",
    "官仔骨骨",
    "巴巴閉閉",
    "晨早流流",
    "新年流流",
    "思思縮縮",
    "忙忙狼狼",
    "死死地氣",
    "陰陰嘴笑",
    "快快脆脆",
    "大啖大啖",
    "拍拍籮柚",
    "搬搬抬抬",
    "整下整下",
    "溶溶爛爛",
    "毛毛草草",
    "好好醜醜",
    "草草收尾",
    "草草收場",
    "人頭湧湧",
    "笑口噬噬",
    "大巴大巴",
    "歪歪斜斜",
    "密密麻麻",
    "老老實實",
}
BLOCKED_EXPRESSIONS = {
    "一個唔該",
    "對唔住",
    "俾電話",
    "畀電話",
    "啫喱筆",
    "啫喱糖",
    "清潔姐姐",
    "收益率",
    "收視率",
    "收銀機",
    "收銀櫃",
    "收藏品",
    "機頂盒",
    "未婚媽媽",
    "巴巴多斯",
    "發生關係",
    "裙帶關係",
    "關係到",
    "打通關係",
    "時哩沙啦",
    "殀殀晒晒",
    "又話呢又話嚕",
    "又話呢又話路",
    "唵嘛呢叭咪吽",
    "嚤囉差玩音樂",
    "摩囉差玩音樂",
    "傳説中嘅",
    "邊度係呢",
    "咯咯咯咯",
    "哩哩啦啦",
    "而字噉手",
    "禾熟噉頭",
    "四萬噉口",
    "吟詩吟唔甩",
    "吟詩都吟唔甩",
    "侲侲哋",
    "借啲意",
    "第二啲",
    "北角過啲",
    "有啲那個",
    "賓虛噉嘅場面",
    "舞龍噉舞",
    "食七噉食",
    "你啲人",
    "囉囉攣",
    "哈囉喂",
    "嚤囉差",
    "囉機字",
    "摩囉差",
    "摩囉綢",
    "該偎囉",
    "金波囉",
}




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
    if any(token in word for token in ("嬲", "驚", "煩", "頹", "怯", "火", "尷", "慌", "忟", "炆")):
        return "情绪表达"
    if any(token in word for token in ("交代", "埋單", "收尾", "跟進", "進度", "開會", "收科")):
        return "工作场景"
    return "俚语表达"


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
        return (
            f"先把「{word}」跟读两次，记住语气和节奏。\n"
            "这类生成表达只供语气练习，不代表推荐用法，不必硬套进句子。"
        )
    return (
        f"先把「{word}」读两次，留意每个音节。\n"
        "这类生成词条只供读音练习，不代表推荐用法，不必硬套进句子。"
    )


def build_prompt_text(kind: str) -> str:
    if kind == "expression":
        return "先理解这条口语表达，再写出 Jyutping，最后按提示先练语气。"
    return "先按自己的习惯读一遍，再写出 Jyutping，最后按提示先练读音。"


def build_rows(pairs: list[tuple[str, str]], kind: str, start_index: int = 1) -> list[dict]:
    rows = []
    for index, (word, pronunciation) in enumerate(pairs, start=start_index):
        category = classify_expression_category(word) if kind == "expression" else classify_word_category(word)
        rows.append(
            {
                "id": f"gen-{kind}-{index:04d}",
                "displayText": word,
                "promptText": build_prompt_text(kind),
                "answerJyutping": pronunciation,
                "gloss": build_meaning(word, category, kind),
                "notes": "",
                "usageTip": build_usage_tip(word, category, kind),
                "exampleSentence": build_examples(word, category, kind),
                "exampleTranslation": "",
                "entryType": kind,
                "category": category,
                "sourceLabel": "generated",
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
    if any(fragment in word for fragment in LOW_CONFIDENCE_WORD_FRAGMENTS):
        return False
    if any(word.endswith(suffix) for suffix in LOW_CONFIDENCE_WORD_SUFFIXES):
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


def score_expression(word: str) -> tuple[int, int, int, str]:
    penalty = count_hits(word, BOOKISH_CHARS) * 4
    strong_count = sum(marker in word for marker in EXPRESSION_STRONG_MARKERS)
    soft_count = sum(marker in word for marker in EXPRESSION_SOFT_MARKERS)
    bonus = strong_count * 4 + soft_count
    if word in EXTRA_COLLOQUIAL_EXPRESSIONS:
        bonus += 6
    if word.startswith(("一", "你", "佢", "我", "依", "呢")):
        penalty += 2
    variant_penalty = (
        count_hits(word, EXPRESSION_VARIANT_PENALTY_CHARS)
        - count_hits(word, EXPRESSION_VARIANT_BONUS_CHARS)
    )
    return (-(expression_colloquial_score(word) + bonus - penalty), variant_penalty, len(word), word)


def should_keep_expression_candidate(word: str) -> bool:
    if len(word) < 3 or len(word) > 6:
        return False
    if word in EXCLUDED_EXPRESSIONS:
        return False
    if word in BLOCKED_EXPRESSIONS:
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


def has_expression_grammar_markers(word: str) -> bool:
    strong_count = sum(marker in word for marker in EXPRESSION_STRONG_MARKERS)
    soft_count = sum(marker in word for marker in EXPRESSION_SOFT_MARKERS)
    return strong_count > 0 or soft_count >= 2


def should_keep_expanded_expression_candidate(word: str) -> bool:
    if should_keep_expression_candidate(word):
        return True
    if word in BLOCKED_EXPRESSIONS:
        return False
    if any(fragment in word for fragment in PROFANITY_FRAGMENTS):
        return False
    if any(fragment in word for fragment in BOOKISH_FRAGMENTS):
        return False
    if any(fragment in word for fragment in WEAK_EXPRESSION_FRAGMENTS):
        return False
    if len(word) < 3 or len(word) > 6:
        return False
    return has_expression_grammar_markers(word) or word in EXTRA_COLLOQUIAL_EXPRESSIONS


def select_expression_candidates(pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    ranked = sorted(pairs, key=lambda item: score_expression(item[0]))
    return ranked[:TARGET_EXPRESSION_COUNT]


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

        if should_keep_expanded_expression_candidate(normalized_word):
            expression_candidates.append((normalized_word, pronunciation))
            continue

        if (
            3 <= len(normalized_word) <= 4
            and has_priority_chars(normalized_word, WORD_PRIORITY_CHARS)
            and should_keep_word_candidate(normalized_word)
        ):
            word_candidates.append((normalized_word, pronunciation))

    word_candidates = sorted(word_candidates, key=lambda item: score_word(item[0]))
    selected_words = word_candidates[:TARGET_WORD_COUNT]

    selected_expressions = select_expression_candidates(expression_candidates)

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
