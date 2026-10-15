import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_assets import ROOT, apply_story_reviews, load_all_entries, reviewed_story_ids
from story_quality_progress import row_digest


class ReviewedStoryPackagingTest(unittest.TestCase):
    def test_packaged_reviewed_snapshot_matches_all_valid_ledger_rows(self):
        entries = json.loads((ROOT / "app/src/main/assets/builtin/content.json").read_text(encoding="utf-8"))["entries"]
        reviewed = reviewed_story_ids()
        self.assertEqual(reviewed, {entry["id"] for entry in entries if entry.get("storyReviewed")})
        sources = {entry["id"]: entry for entry in load_all_entries()}
        for entry in entries:
            if entry["id"] in reviewed:
                for field in ("displayText", "answerJyutping", "gloss", "usageTip", "exampleSentence"):
                    self.assertEqual(sources[entry["id"]][field], entry[field], (entry["id"], field))

    def test_only_reviewed_upgrades_replace_previously_packaged_sentences(self):
        current = [
            {"id": "approved", "entryType": "sentence", "displayText": "approved update"},
            {"id": "draft", "entryType": "sentence", "displayText": "unreviewed draft", "usageTip": "故事练习："},
            {"id": "word", "entryType": "word", "displayText": "new word"},
        ]
        baseline = [{"id": "draft", "entryType": "sentence", "displayText": "packaged original"}]
        result = apply_story_reviews(current, {"approved"}, baseline)
        self.assertEqual(["approved update", "packaged original", "new word"], [e["displayText"] for e in result])
        self.assertEqual([True, False, False], [e.get("storyReviewed", False) for e in result])
        self.assertEqual("unreviewed draft", current[1]["displayText"])

    def test_missing_baseline_cannot_silently_ship_a_draft(self):
        with self.assertRaisesRegex(ValueError, "No previously packaged sentence"):
            apply_story_reviews([{"id": "draft", "entryType": "sentence"}], set(), [])

    def test_review_hash_dimensions_and_one_based_runtime_id(self):
        review = json.loads((ROOT / "STORY_LANGUAGE_REVIEW.json").read_text(encoding="utf-8"))[0]
        row = json.loads((ROOT / review["file"]).read_text(encoding="utf-8"))[review["index"]]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "content/sentence_bank/test.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps([row]), encoding="utf-8")
            record = {**review, "file": "content/sentence_bank/test.json", "index": 0, "sha256": row_digest(row)}
            ledger = root / "STORY_LANGUAGE_REVIEW.json"
            ledger.write_text(json.dumps([record]), encoding="utf-8")
            self.assertEqual({"sentence-bank-test-0001"}, reviewed_story_ids(root))
            ledger.write_text(json.dumps([{**record, "complete_gloss": False}]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Unverified or stale"):
                reviewed_story_ids(root)
            ledger.write_text(json.dumps([{**record, "sha256": "changed"}]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Unverified or stale"):
                reviewed_story_ids(root)


if __name__ == "__main__":
    unittest.main()
