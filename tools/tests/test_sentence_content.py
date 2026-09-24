from __future__ import annotations

import json
import re
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATHS = sorted(ROOT.glob("content/*sentence*_bank.json"))
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
        self.assertTrue(all(path.name.startswith("handwritten_sentences_") for path in SOURCE_PATHS))
        self.assertTrue(all(row["id"].startswith("sentence-hand-") for row in rows))
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
                self.assertEqual("".join(self._jyutping_token.findall(jyutping.lower())), residue)
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

        self.assertEqual({row["id"] for row in source_rows}, set(bundled))
        for source in source_rows:
            with self.subTest(entry_id=source["id"]):
                entry = bundled[source["id"]]
                self.assertEqual(source["displayText"], entry["displayText"])
                self.assertEqual(source["answerJyutping"], entry["answerJyutping"])
                self.assertIn("完整句子", entry["promptText"])
                self.assertEqual("curated", entry["sourceLabel"])


if __name__ == "__main__":
    unittest.main()
