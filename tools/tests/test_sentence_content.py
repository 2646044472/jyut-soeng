from __future__ import annotations

import json
import re
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATHS = sorted(ROOT.glob("content/*sentence*_bank.json"))
INDEPENDENT_SOURCE_PATHS = sorted((ROOT / "content" / "sentence_bank").glob("*.json"))
BUNDLE_PATH = ROOT / "app" / "src" / "main" / "assets" / "builtin" / "content.json"


class DailySentenceContentTest(unittest.TestCase):

    _jyutping_token = re.compile(r"[a-z]+[1-6]")

    def test_source_contains_complete_curated_sentences(self) -> None:
        rows = [
            row
            for path in SOURCE_PATHS
            for row in json.loads(path.read_text(encoding="utf-8"))
        ]
        self.assertGreaterEqual(len(rows), 300)
        self.assertTrue(all(row["id"].startswith("sentence-") for row in rows))
        self.assertTrue(all(row.get("sourceLabel") == "curated" for row in rows))
        self.assertEqual(len(rows), len({row["id"] for row in rows}))
        self.assertEqual(len(rows), len({row["displayText"] for row in rows}))
        for field in ("gloss", "notes", "usageTip"):
            self.assertLessEqual(max(Counter(row[field] for row in rows).values()), 3)
        self.assertLessEqual(max(Counter(row["displayText"][:18] for row in rows).values()), 3)

        for row in rows:
            with self.subTest(entry_id=row.get("id")):
                sentence = row["displayText"].strip()
                jyutping = row["answerJyutping"].strip()
                self.assertEqual("curated", row.get("sourceLabel", "curated"))
                self.assertGreaterEqual(len(sentence), 30)
                self.assertGreaterEqual(
                    sentence.count("，") + sentence.count("；") + sentence.count("？"),
                    2,
                )
                self.assertRegex(sentence, r"[。？！]")
                self.assertGreaterEqual(len(jyutping.split()), 28)
                residue = re.sub(r"[，。；？！、\s]", "", jyutping.lower())
                syllables = self._jyutping_token.findall(jyutping.lower())
                self.assertEqual("".join(syllables), residue)
                self.assertEqual(
                    len(re.findall(r"[\u3400-\u9fff\U00020000-\U0002FA1F]", sentence)),
                    len(syllables),
                )
                self.assertTrue(row["gloss"].strip())
                self.assertTrue(row["notes"].strip())
                self.assertTrue(row["usageTip"].strip())
                self.assertIn(sentence, row["exampleSentence"])

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

        self.assertTrue({row["id"] for row in source_rows}.issubset(bundled))
        for source in source_rows:
            with self.subTest(entry_id=source["id"]):
                entry = bundled[source["id"]]
                self.assertEqual(source["displayText"], entry["displayText"])
                self.assertEqual(source["answerJyutping"], entry["answerJyutping"])
                self.assertIn("完整句子", entry["promptText"])
                self.assertEqual("curated", entry["sourceLabel"])

    def test_independent_sentence_bank_has_complete_jyutping(self) -> None:
        rows = [
            (path, index, row)
            for path in INDEPENDENT_SOURCE_PATHS
            for index, row in enumerate(json.loads(path.read_text(encoding="utf-8")), start=1)
        ]
        self.assertEqual(len(rows), 10000)
        self.assertEqual(len(rows), len({row["sentence"] for _, _, row in rows}))
        topic_counts = Counter(
            path.stem.rsplit("_", maxsplit=1)[0]
            for path in INDEPENDENT_SOURCE_PATHS
            for _ in json.loads(path.read_text(encoding="utf-8"))
        )
        self.assertEqual(
            {
                "long_family_finance_services": 1000,
                "long_food_shopping": 1000,
                "long_health_services": 1000,
                "long_home_family": 1000,
                "long_housing_neighborhood": 1000,
                "long_money_admin": 1000,
                "long_school_education": 1000,
                "long_social_leisure": 1000,
                "long_transit_travel": 1000,
                "long_work_life": 1000,
            },
            dict(topic_counts),
        )

        for path, index, row in rows:
            with self.subTest(source=f"{path.name}:{index}"):
                sentence = row["sentence"].strip()
                jyutping = row["jyutping"].strip().lower()
                self.assertTrue(row["category"].strip())
                self.assertTrue(row.get("gloss", "").strip())
                han_count = len(
                    re.findall(
                        r"[\u3400-\u9fff\uf900-\ufaff\U00020000-\U0002FA1F\U00030000-\U000323AF]",
                        sentence,
                    )
                )
                self.assertGreaterEqual(han_count, 60)
                self.assertLessEqual(han_count, 90)
                self.assertRegex(sentence, r"[。？！.!?][」』”\"]?$")
                residue = re.sub(r"[,，.。:：;；?!？！、\s]", "", jyutping)
                syllables = self._jyutping_token.findall(jyutping)
                self.assertTrue(syllables)
                self.assertEqual("".join(syllables), residue)
                self.assertGreaterEqual(len(syllables), 22)
                if not re.search(r"[A-Za-z0-9]", sentence) and "中英文" not in sentence:
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
