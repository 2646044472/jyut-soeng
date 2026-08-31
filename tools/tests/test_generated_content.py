from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BUNDLE_PATH = ROOT / "app" / "src" / "main" / "assets" / "builtin" / "content.json"
FORCED_SENTENCE_MARKERS = (
    "自己试着用",
    "自己开口说一次",
    "想一个会用到",
    "说一句",
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

    def test_built_bundle_has_only_hand_written_content(self) -> None:
        bundle = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))
        generated_rows = [row for row in bundle.get("entries", []) if row.get("sourceLabel") == "generated"]
        self.assertEqual([], generated_rows)


if __name__ == "__main__":
    unittest.main()
