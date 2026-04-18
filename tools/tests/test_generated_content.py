from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GENERATED_PATHS = (
    ROOT / "content" / "generated_words_bank.json",
    ROOT / "content" / "generated_expressions_bank.json",
)
FORCED_SENTENCE_MARKERS = (
    "自己试着用",
    "自己开口说一次",
    "想一个会用到",
    "说一句",
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
CURATED_PATHS = tuple(
    path
    for path in (ROOT / "content").glob("*_bank.json")
    if not path.name.startswith("generated_")
)


class GeneratedContentTest(unittest.TestCase):

    def test_generated_rows_are_self_describing(self) -> None:
        for path in GENERATED_PATHS:
            with self.subTest(path=path.name):
                rows = json.loads(path.read_text(encoding="utf-8"))
                self.assertTrue(rows)
                for row in rows[:25]:
                    self.assertEqual("generated", row.get("sourceLabel"))
                    self.assertIn(row.get("entryType"), {"word", "expression"})
                    self.assertTrue(str(row.get("promptText", "")).strip())

    def test_generated_rows_do_not_force_sentence_making(self) -> None:
        for path in GENERATED_PATHS:
            with self.subTest(path=path.name):
                rows = json.loads(path.read_text(encoding="utf-8"))
                for row in rows[:100]:
                    example_sentence = str(row.get("exampleSentence", ""))
                    self.assertFalse(
                        any(marker in example_sentence for marker in FORCED_SENTENCE_MARKERS),
                        msg=f"{path.name}:{row.get('id')}",
                    )

    def test_generated_rows_skip_low_confidence_wording(self) -> None:
        for path in GENERATED_PATHS:
            with self.subTest(path=path.name):
                rows = json.loads(path.read_text(encoding="utf-8"))
                blocked = (
                    LOW_CONFIDENCE_GENERATED_EXPRESSION_FRAGMENTS
                    if "expression" in path.name
                    else LOW_CONFIDENCE_GENERATED_WORD_FRAGMENTS
                )
                for row in rows:
                    display_text = str(row.get("displayText", ""))
                    self.assertFalse(
                        any(marker in display_text for marker in blocked),
                        msg=f"{path.name}:{display_text}",
                    )

    def test_curated_examples_keep_the_target_text_visible(self) -> None:
        for path in CURATED_PATHS:
            with self.subTest(path=path.name):
                rows = json.loads(path.read_text(encoding="utf-8"))
                for row in rows:
                    display_text = str(row.get("displayText", "")).strip()
                    example_sentence = str(row.get("exampleSentence", "")).strip()
                    lines = [line.strip() for line in example_sentence.splitlines() if line.strip()]
                    if display_text and lines:
                        self.assertTrue(
                            any(display_text in line for line in lines),
                            msg=f"{path.name}:{row.get('id')}",
                        )


if __name__ == "__main__":
    unittest.main()
