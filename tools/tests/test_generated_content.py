from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GENERATED_PATHS = (
    ROOT / "content" / "generated_words_bank.json",
    ROOT / "content" / "generated_expressions_bank.json",
)
BUNDLE_PATH = ROOT / "app" / "src" / "main" / "assets" / "builtin" / "content.json"
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
FORBIDDEN_BUILT_GLOSS_FRAGMENTS = (
    "通常唔系逐个字照字面解",
    "一个固定词语，要连前后文一齐先容易明白讲紧乜",
    "多数唔系讲字面",
    "呢类讲法通常靠前后文先完整",
    "一句追问情况、原因或者来历嘅口语说法",
    "一句带否定意思嘅口语说法",
)
FORBIDDEN_BUILT_USAGE_FRAGMENTS = (
    "多半系熟人之间顺口爆出来",
    "多系当场拒绝、讲做唔到",
    "通常系跟住眼前情况顺口讲出",
    "多数系讲完件事之后",
)
FORBIDDEN_BUILT_EXAMPLE_FRAGMENTS = (
    "朋友見到眼前個情況",
    "真係遇到嗰下，講句",
    "你問我點睇，我只可以講句",
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

    def test_built_bundle_avoids_generic_generated_copy(self) -> None:
        bundle = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))
        generated_rows = [row for row in bundle.get("entries", []) if row.get("sourceLabel") == "generated"]
        self.assertTrue(generated_rows)
        for row in generated_rows:
            gloss = str(row.get("gloss", ""))
            usage = str(row.get("usageTip", ""))
            example = str(row.get("exampleSentence", ""))
            self.assertFalse(
                any(marker in gloss for marker in FORBIDDEN_BUILT_GLOSS_FRAGMENTS),
                msg=f"generic gloss:{row.get('id')}",
            )
            self.assertFalse(
                any(marker in usage for marker in FORBIDDEN_BUILT_USAGE_FRAGMENTS),
                msg=f"generic usage:{row.get('id')}",
            )
            self.assertFalse(
                any(marker in example for marker in FORBIDDEN_BUILT_EXAMPLE_FRAGMENTS),
                msg=f"generic example:{row.get('id')}",
            )


if __name__ == "__main__":
    unittest.main()
