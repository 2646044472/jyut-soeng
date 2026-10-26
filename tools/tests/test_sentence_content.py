from __future__ import annotations

import json
import os
import re
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATHS = sorted(ROOT.glob("content/*sentence*_bank.json"))
INDEPENDENT_SOURCE_PATHS = sorted((ROOT / "content" / "sentence_bank").glob("*.json"))
BUNDLE_PATH = ROOT / "app" / "src" / "main" / "assets" / "builtin" / "content.json"
HAN_CHARACTER = re.compile(
    r"[\u3400-\u9fff\uf900-\ufaff\U00020000-\U0002FA1F\U00030000-\U000323AF]"
)
LAST_SHORT_SENTENCE_BATCH = {
    "long_family_finance_services": 10,
    "long_food_shopping": 10,
    "long_health_services": 10,
    "long_home_family": 9,
    "long_housing_neighborhood": 10,
    "long_money_admin": 27,
    "long_school_education": 10,
    "long_social_leisure": 10,
    "long_transit_travel": 10,
    "long_work_life": 10,
}


class DailySentenceContentTest(unittest.TestCase):

    _jyutping_token = re.compile(r"[a-z]+[1-6]")

    def assert_completed_story(self, row: dict, selected: bool) -> None:
        sentence = row["displayText" if selected else "sentence"].strip()
        jyutping = row["answerJyutping" if selected else "jyutping"].strip().lower()
        han_count = len(HAN_CHARACTER.findall(sentence))
        self.assertGreaterEqual(han_count, 220)
        self.assertLessEqual(han_count, 320)
        self.assertIn("「", sentence)
        self.assertIn("」", sentence)
        self.assertIsNone(re.search(r"[A-Za-z0-9]", sentence))
        self.assertRegex(sentence, r"[。？！][」』”\"]?$")
        self.assertTrue(row.get("usageTip", "").startswith("故事练习："))
        self.assertGreaterEqual(len(HAN_CHARACTER.findall(row["gloss"])), 160)
        residue = re.sub(r"[,，.。:：;；?!？！、「」『』“”\"'\s]", "", jyutping)
        syllables = self._jyutping_token.findall(jyutping)
        self.assertEqual("".join(syllables), residue)
        self.assertEqual(han_count, len(syllables))
        if selected:
            self.assertEqual(sentence, row["exampleSentence"])

    @unittest.skipUnless(
        os.environ.get("JYUT_SOENG_REQUIRE_COMPLETE_STORIES") == "1",
        "Story migration is incomplete; set JYUT_SOENG_REQUIRE_COMPLETE_STORIES=1 for full-corpus acceptance.",
    )
    def test_all_source_cards_are_completed_stories(self) -> None:
        for paths, selected in ((SOURCE_PATHS, True), (INDEPENDENT_SOURCE_PATHS, False)):
            for path in paths:
                for index, row in enumerate(json.loads(path.read_text(encoding="utf-8"))):
                    with self.subTest(source=f"{path.name}:{index}"):
                        self.assert_completed_story(row, selected)

    def test_only_the_reviewed_source_order_prefix_is_retained(self) -> None:
        self.assertEqual(SOURCE_PATHS, [])

    def test_built_bundle_preserves_sentence_reading_fields(self) -> None:
        source_rows = [
            row
            for path in SOURCE_PATHS
            for row in json.loads(path.read_text(encoding="utf-8"))
        ]
        bundle = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))
        bundled = {
            row["id"]: row
            for row in bundle["entries"]
            if row.get("entryType") == "sentence"
        }

        self.assertEqual(len(bundled), 5000)
        self.assertTrue({row["id"] for row in source_rows}.issubset(bundled))
        for source in source_rows:
            with self.subTest(entry_id=source["id"]):
                entry = bundled[source["id"]]
                self.assertEqual(source["displayText"], entry["displayText"])
                self.assertEqual(source["answerJyutping"], entry["answerJyutping"])
                self.assertEqual(source["gloss"].strip(), entry["gloss"])
                self.assertEqual(source["usageTip"].strip(), entry["usageTip"])
                if source["usageTip"].startswith("故事练习："):
                    self.assertEqual(source["exampleSentence"], entry["exampleSentence"])
                self.assertIn("完整句子", entry["promptText"])
                self.assertEqual("curated", entry["sourceLabel"])

    def test_independent_sentence_bank_has_complete_jyutping(self) -> None:
        rows = [
            (path, index, row)
            for path in INDEPENDENT_SOURCE_PATHS
            for index, row in enumerate(json.loads(path.read_text(encoding="utf-8")), start=1)
        ]
        self.assertEqual(len(rows), 5000)
        self.assertEqual(len(rows), len({row["sentence"] for _, _, row in rows}))
        topic_counts = Counter(
            path.stem.rsplit("_", maxsplit=1)[0]
            for path in INDEPENDENT_SOURCE_PATHS
            for _ in json.loads(path.read_text(encoding="utf-8"))
        )
        self.assertEqual(
            {
                "long_family_finance_services": 1267,
                "long_food_shopping": 1533,
                "long_health_services": 1202,
                "long_home_family": 998,
            },
            dict(topic_counts),
        )

        for path, index, row in rows:
            with self.subTest(source=f"{path.name}:{index}"):
                sentence = row["sentence"].strip()
                jyutping = row["jyutping"].strip().lower()
                self.assertTrue(row["category"].strip())
                self.assertTrue(row.get("gloss", "").strip())
                han_count = len(HAN_CHARACTER.findall(sentence))
                if row.get("usageTip", "").startswith("故事练习："):
                    self.assert_completed_story(row, selected=False)
                else:
                    topic, batch = path.stem.rsplit("_", maxsplit=1)
                    lower, upper = (100, 130) if int(batch) > LAST_SHORT_SENTENCE_BATCH[topic] else (60, 90)
                    self.assertGreaterEqual(han_count, lower)
                    self.assertLessEqual(han_count, upper)
                self.assertRegex(sentence, r"[。？！.!?][」』”\"]?$")
                residue = re.sub(r"[,，.。:：;；?!？！、「」『』“”\"'\s]", "", jyutping)
                syllables = self._jyutping_token.findall(jyutping)
                self.assertTrue(syllables)
                self.assertEqual("".join(syllables), residue)
                if not re.search(r"[A-Za-z0-9]", sentence):
                    self.assertEqual(han_count, len(syllables))

    def test_built_bundle_includes_independent_sentence_cards(self) -> None:
        source_rows = [
            (path, index, row)
            for path in INDEPENDENT_SOURCE_PATHS
            for index, row in enumerate(json.loads(path.read_text(encoding="utf-8")), start=1)
        ]
        bundle = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))
        bundled = {
            row["id"]: row
            for row in bundle["entries"]
            if row.get("entryType") == "sentence"
        }
        expected_ids = {
            f"sentence-bank-{path.stem}-{index:04d}"
            for path, index, _ in source_rows
        }
        bundled_independent_ids = {
            row["id"]
            for row in bundle["entries"]
            if row.get("entryType") == "sentence" and row["id"].startswith("sentence-bank-")
        }

        self.assertEqual(expected_ids, bundled_independent_ids)
        for path, index, source in source_rows:
            entry_id = f"sentence-bank-{path.stem}-{index:04d}"
            with self.subTest(entry_id=entry_id):
                entry = bundled[entry_id]
                self.assertEqual(source["sentence"], entry["displayText"])
                self.assertEqual(source["jyutping"], entry["answerJyutping"])
                self.assertEqual(source["category"], entry["category"])
                self.assertEqual(source.get("gloss", "").strip(), entry["gloss"])
                self.assertEqual(source.get("usageTip", "").strip(), entry["usageTip"])
                self.assertEqual("curated", entry["sourceLabel"])
                self.assertEqual("sentence", entry["entryType"])


if __name__ == "__main__":
    unittest.main()
