"""Run the shipped new-sentence DAO query against the real packaged rows and old progress."""
import json
import re
import sqlite3
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "app/src/main/java/dev/local/yuecal/data"
BUILTIN = ROOT / "app/src/main/assets/builtin/content.json"


def sql_from_dao(method):
    source = (DATA / "AppDatabase.kt").read_text()
    section = source[:source.index("suspend fun " + method + "(")]
    return section.rsplit('@Query(', 1)[1].split('"""')[1]


class ProofreadQueueTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = json.loads(BUILTIN.read_text())["entries"]
        cls.stories = [e for e in cls.bundle if e["entryType"] == "sentence"]
        manifest = json.loads((ROOT / "content/story_source_index_map.json").read_text())
        with zipfile.ZipFile(ROOT / manifest["archive_path"]) as z:
            cls.old = json.loads(z.read("snapshot/app/src/main/assets/builtin/content.json"))["entries"]
        rows = re.findall(r"^\| (\d{2}-\d{4}|\d{4})(?=\s)", (ROOT / "STORY_PROOFREAD_PROGRESS.md").read_text(), re.M)
        cls.approved = {"sentence-bank-long_family_finance_services_" + (s if "-" in s else "01-" + s) for s in rows}

    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.addCleanup(self.db.close)
        self.db.executescript("""
          CREATE TABLE calibration_entries(id TEXT PRIMARY KEY, entryType TEXT, qualityPriority INTEGER, sortOrder INTEGER, category TEXT, isActive INTEGER, displayText TEXT);
          CREATE TABLE review_progress(entryId TEXT PRIMARY KEY, repetitions INTEGER, nextReviewEpochDay INTEGER, lastReviewedAt INTEGER);
          CREATE TABLE study_attempts(entryId TEXT, answeredAt INTEGER);
        """)
        self.apply(self.old)

    def apply(self, entries):
        self.db.executemany("INSERT OR REPLACE INTO calibration_entries VALUES(?,?,?,?,?,1,?)",
            [(e["id"],e["entryType"],e.get("qualityPriority",0),e["sortOrder"],e["category"],e["displayText"]) for e in entries])
    def queue(self, limit):
        return [r[0] for r in self.db.execute(sql_from_dao("getNewEntriesByType"), dict(entryType="sentence",limit=limit))]
    def study(self, ids):
        self.db.executemany("INSERT INTO review_progress VALUES (?,2,42,7)",[(i,) for i in ids])
        self.db.executemany("INSERT INTO study_attempts VALUES (?,7)",[(i,) for i in ids])

    def test_fresh_install_stable_priority_and_fallback(self):
        self.assertEqual([e["id"] for e in self.old], [e["id"] for e in self.bundle])
        self.apply(self.bundle)
        all_ids = self.queue(2000)
        self.assertEqual(len(set(all_ids)), 2000)
        self.assertEqual(set(all_ids[:len(self.approved)]), self.approved)
        self.assertEqual(self.queue(50), all_ids[:50])
        self.assertEqual(self.queue(2000), all_ids)
        self.assertTrue(all(e.get("qualityPriority",0)==int(e["id"] in self.approved) for e in self.bundle))

    def test_cover_upgrade_and_content_refresh_preserve_progress_at_tier_boundary(self):
        approved=sorted(self.approved)
        ordinary=sorted(e["id"] for e in self.stories if e["id"] not in self.approved)
        studied=approved[:-2]+ordinary[:5]
        self.study(studied)
        before = list(self.db.execute("SELECT * FROM review_progress ORDER BY entryId"))
        attempts = list(self.db.execute("SELECT * FROM study_attempts ORDER BY entryId"))
        for _ in range(2): # offline built-in seed and identical downloaded content
            self.apply(self.bundle)
            queue = self.queue(50)
            self.assertEqual(set(queue[:2]),set(approved[-2:]))
            self.assertTrue(all(e not in self.approved for e in queue[2:]))
            self.assertTrue(set(queue).isdisjoint(studied))
            self.assertEqual(list(self.db.execute("SELECT * FROM review_progress ORDER BY entryId")), before)
            self.assertEqual(list(self.db.execute("SELECT * FROM study_attempts ORDER BY entryId")), attempts)
            due=[e[0] for e in self.db.execute(sql_from_dao("getDueEntriesByType"),dict(entryType="sentence",today=42,limit=2000))]
            self.assertEqual(set(due),set(studied))
        self.study(approved[-2:])
        self.assertTrue(set(self.queue(2000)).isdisjoint(self.approved))
