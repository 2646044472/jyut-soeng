import json
import sqlite3
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from build_assets import prioritize_reviewed_sentences, reviewed_sentence_ids


class ReviewedStoryPriorityTest(unittest.TestCase):
    def test_bundle_starts_sentence_queue_with_exact_reviewed_snapshot(self):
        entries = json.loads((ROOT / "app/src/main/assets/builtin/content.json").read_text(encoding="utf-8"))["entries"]
        reviewed = reviewed_sentence_ids()
        sentences = [entry for entry in entries if entry["entryType"] == "sentence"]
        self.assertTrue(reviewed)
        self.assertEqual(len(sentences), 15053)
        self.assertEqual({entry["id"] for entry in sentences[:len(reviewed)]}, reviewed)
        self.assertTrue(all(a["sortOrder"] < b["sortOrder"] for a, b in zip(sentences, sentences[1:])))

    def test_partition_preserves_order_and_ids(self):
        entries = [
            {"id": "old-a", "entryType": "sentence"},
            {"id": "word", "entryType": "word"},
            {"id": "ready-a", "entryType": "sentence"},
            {"id": "old-b", "entryType": "sentence"},
            {"id": "ready-b", "entryType": "sentence"},
        ]
        self.assertEqual([e["id"] for e in prioritize_reviewed_sentences(entries, {"ready-a", "ready-b"})],
                         ["word", "ready-a", "ready-b", "old-a", "old-b"])

    def test_actual_dao_query_prioritizes_stories_and_preserves_progress(self):
        source = (ROOT / "app/src/main/java/dev/local/yuecal/data/AppDatabase.kt").read_text(encoding="utf-8")
        query = source.split("suspend fun getNewEntriesByType", 1)[0].rsplit("@Query(", 1)[1].split('"""')[1]
        db = sqlite3.connect(":memory:")
        db.executescript("""
            CREATE TABLE calibration_entries (id TEXT, isActive INTEGER, entryType TEXT, category TEXT, sortOrder INTEGER);
            CREATE TABLE review_progress (entryId TEXT);
            INSERT INTO calibration_entries VALUES
              ('old', 1, 'sentence', '高频回应', 30),
              ('ready-b', 1, 'sentence', '保险', 20),
              ('ready-a', 1, 'sentence', '保险', 10),
              ('learned', 1, 'sentence', '保险', 1),
              ('inactive', 0, 'sentence', '保险', 0),
              ('word-other', 1, 'word', '其他', 1),
              ('word-priority', 1, 'word', '正音重点词', 100);
            INSERT INTO review_progress VALUES ('learned');
        """)
        self.assertEqual([r[0] for r in db.execute(query, {"entryType": "sentence", "limit": 2})], ["ready-a", "ready-b"])
        self.assertEqual([r[0] for r in db.execute(query, {"entryType": "sentence", "limit": 10})], ["ready-a", "ready-b", "old"])
        self.assertEqual(db.execute(query, {"entryType": "word", "limit": 1}).fetchone()[0], "word-priority")
        db.close()
