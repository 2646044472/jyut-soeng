from __future__ import annotations

import json
import hashlib
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
import zipfile
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from story_source_index import (
    all_rows_by_current_coordinate,
    active_rows_by_current_coordinate,
    archived_source_rows,
    load_index,
    row_digest,
)
SOURCE_PATHS = sorted(ROOT.glob("content/*sentence*_bank.json"))
INDEPENDENT_SOURCE_PATHS = sorted((ROOT / "content" / "sentence_bank").glob("*.json"))
BUNDLE_PATH = ROOT / "app" / "src" / "main" / "assets" / "builtin" / "content.json"
SELECTION_PATH = ROOT / "content" / "story_library_selection.json"
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

        selection = json.loads(SELECTION_PATH.read_text(encoding="utf-8"))
        active_ids = set(selection["active_ids"])
        standalone_ids = {
            entry_id for entry_id in bundled if entry_id.startswith("sentence-bank-")
        }
        self.assertEqual(len(active_ids), selection["target_active_cards"])
        self.assertEqual(selection["target_active_cards"], 2000)
        self.assertEqual(len(standalone_ids), selection["target_active_cards"])
        self.assertEqual(standalone_ids, active_ids)
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
        self.assertEqual(len(rows), 2000)
        self.assertEqual(len(rows), len({row["sentence"] for _, _, row in rows}))

        selection = json.loads(SELECTION_PATH.read_text(encoding="utf-8"))
        active_ids = set(selection["active_ids"])
        self.assertEqual(selection["target_active_cards"], 2000)
        self.assertEqual(len(active_ids), 2000)
        index_map = load_index()
        current_map = active_rows_by_current_coordinate(index_map)
        current_ids = set()
        for path, index, row in rows:
            mapping = current_map[(path.relative_to(ROOT).as_posix(), index - 1)]
            self.assertEqual(row_digest(row), mapping["original_row_sha256"])
            current_ids.add(mapping["id"])
        self.assertEqual(current_ids, active_ids)
        revalidation = json.loads((ROOT / "STORY_QUALITY_REVALIDATION.json").read_text(encoding="utf-8"))
        passed_ids = {
            f"sentence-bank-{Path(record['file']).stem}-{record['index'] + 1:04d}"
            for record in revalidation["cards"]
            if record.get("status") == "pass"
        }
        self.assertTrue(active_ids.issubset(passed_ids))

        for path, index, row in rows:
            entry_id = current_map[(path.relative_to(ROOT).as_posix(), index - 1)]["id"]
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
        index_map = load_index()
        current_map = active_rows_by_current_coordinate(index_map)
        source_ids = {
            current_map[(path.relative_to(ROOT).as_posix(), index - 1)]["id"]
            for path, index, _ in source_rows
        }
        selection = json.loads(SELECTION_PATH.read_text(encoding="utf-8"))
        expected_ids = set(selection["active_ids"])
        bundled_independent_ids = {
            row["id"]
            for row in bundle["entries"]
            if row.get("entryType") == "sentence" and row["id"].startswith("sentence-bank-")
        }

        self.assertEqual(len(source_ids), 2000)
        self.assertEqual(source_ids, expected_ids)
        self.assertEqual(expected_ids, bundled_independent_ids)
        for path, index, source in source_rows:
            entry_id = current_map[(path.relative_to(ROOT).as_posix(), index - 1)]["id"]
            with self.subTest(entry_id=entry_id):
                entry = bundled[entry_id]
                self.assertEqual(source["sentence"], entry["displayText"])
                self.assertEqual(source["jyutping"], entry["answerJyutping"])
                self.assertEqual(source["category"], entry["category"])
                self.assertEqual(source.get("gloss", "").strip(), entry["gloss"])
                self.assertEqual(source.get("usageTip", "").strip(), entry["usageTip"])
                self.assertEqual("curated", entry["sourceLabel"])
                self.assertEqual("sentence", entry["entryType"])

    def test_source_archive_is_restorable_and_app_entries_match_v0363(self) -> None:
        index_map = load_index()
        manifest = json.loads((ROOT / "content" / "story_archive" / "manifest.json").read_text(encoding="utf-8"))
        original_rows = archived_source_rows(index_map)
        selection = json.loads(SELECTION_PATH.read_text(encoding="utf-8"))
        active_ids = set(selection["active_ids"])
        excluded_ids = set(selection["excluded_ids"])
        mapped_active = {row["id"] for row in index_map["active_rows"]}
        mapped_excluded = {row["id"] for row in index_map["archived_rows"]}
        self.assertEqual((len(original_rows), len(mapped_active), len(mapped_excluded)), (5000, 2000, 3000))
        self.assertEqual(mapped_active, active_ids)
        self.assertEqual(mapped_excluded, excluded_ids)
        self.assertFalse(mapped_active & mapped_excluded)
        mappings = index_map["active_rows"] + index_map["archived_rows"]
        mapped_coordinates = set()
        for mapping in mappings:
            coordinate = (mapping["original_file"], mapping["original_index"])
            self.assertNotIn(coordinate, mapped_coordinates)
            mapped_coordinates.add(coordinate)
            self.assertEqual(
                mapping["id"],
                f"sentence-bank-{Path(mapping['original_file']).stem}-{mapping['original_index'] + 1:04d}",
            )
            self.assertEqual(
                row_digest(original_rows[coordinate]),
                mapping["original_row_sha256"],
            )
        self.assertEqual(mapped_coordinates, set(original_rows))

        with zipfile.ZipFile(ROOT / index_map["archive_path"]) as archive:
            for record in manifest["files"]:
                payload = archive.read(f"snapshot/{record['path']}")
                self.assertEqual(hashlib.sha256(payload).hexdigest(), record["sha256"])
            baseline_bundle = json.loads(archive.read("snapshot/app/src/main/assets/builtin/content.json"))

        current_bundle = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(current_bundle["entries"], baseline_bundle["entries"])
        self.assertEqual(len(baseline_bundle["entries"]), manifest["release_app_entry_count"])
        canonical_entries = json.dumps(
            baseline_bundle["entries"], ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        self.assertEqual(hashlib.sha256(canonical_entries).hexdigest(), manifest["release_app_entries_sha256"])
        self.assertEqual(
            {entry["id"] for entry in baseline_bundle["entries"] if entry.get("id", "").startswith("sentence-bank-")},
            active_ids,
        )

        with tempfile.TemporaryDirectory(prefix="jyut-soeng-full-restore-") as temporary:
            restored_root = Path(temporary) / "repo"
            restored_root.mkdir()
            for relative in (
                "content/sentence_bank",
                "content/story_archive",
                "tools",
                "app/src/main/assets/builtin",
            ):
                shutil.copytree(ROOT / relative, restored_root / relative)
            for relative in (
                "content/story_source_index_map.json",
                "content/story_library_selection.json",
                "STORY_QUALITY_REVALIDATION.json",
                "STORY_QUALITY_ORAL_REAUDIT.json",
            ):
                shutil.copy2(ROOT / relative, restored_root / relative)
            for bank_path in ROOT.glob("content/*_bank.json"):
                shutil.copy2(bank_path, restored_root / "content" / bank_path.name)

            subprocess.run(
                ["python", "tools/restore_story_archive.py", "--restore", "--include-app"],
                cwd=restored_root, check=True, capture_output=True, text=True,
            )
            restored_index = json.loads((restored_root / "content/story_source_index_map.json").read_text(encoding="utf-8"))
            restored_current_map = all_rows_by_current_coordinate(restored_index)
            restored_source_count = sum(
                len(json.loads(path.read_text(encoding="utf-8")))
                for path in (restored_root / "content/sentence_bank").glob("*.json")
            )
            self.assertEqual(restored_index["source_layout"], "full_restored")
            self.assertEqual((restored_source_count, len(restored_current_map)), (5000, 5000))

            build_result = subprocess.run(
                ["python", "tools/build_assets.py"], cwd=restored_root, capture_output=True, text=True
            )
            self.assertEqual(build_result.returncode, 0, build_result.stderr)
            audit_result = subprocess.run(
                ["python", "tools/active_oral_ledger_audit.py"],
                cwd=restored_root, check=True, capture_output=True, text=True,
            )
            restored_audit = json.loads(audit_result.stdout)
            self.assertEqual(restored_audit["errors"], [])
            rebuilt = json.loads((restored_root / "app/src/main/assets/builtin/content.json").read_text(encoding="utf-8"))
            self.assertEqual(rebuilt["entries"], baseline_bundle["entries"])


if __name__ == "__main__":
    unittest.main()
