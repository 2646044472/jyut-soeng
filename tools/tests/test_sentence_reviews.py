from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from sentence_reviews import content_fingerprint, require_human_reviews


class HumanSentenceReviewTest(unittest.TestCase):
    def setUp(self) -> None:
        self.entry = {
            "id": "sentence-test-1",
            "entryType": "sentence",
            "displayText": "reviewed text",
            "answerJyutping": "jyut6 ping3",
            "gloss": "meaning",
        }
        self.review = {
            "id": self.entry["id"],
            "humanAuthored": True,
            "author": "Human contributor",
            "reviewer": "Human reviewer",
            "reviewedAt": "2026-09-24",
            "contentSha256": content_fingerprint(self.entry),
        }

    def check(self, reviews: list[dict], entries: list[dict] | None = None) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "reviews.json"
            path.write_text(json.dumps({"reviews": reviews}), encoding="utf-8")
            require_human_reviews(entries if entries is not None else [self.entry], path)

    def test_reviewed_sentence_passes(self) -> None:
        self.check([self.review])

    def test_unreviewed_sentence_fails(self) -> None:
        with self.assertRaisesRegex(ValueError, "Missing human reviews"):
            self.check([])

    def test_changed_sentence_requires_new_review(self) -> None:
        changed = {**self.entry, "answerJyutping": "new1 reading2"}
        with self.assertRaisesRegex(ValueError, "changed since human review"):
            self.check([self.review], [changed])

    def test_duplicate_review_fails(self) -> None:
        with self.assertRaisesRegex(ValueError, "Duplicate human review"):
            self.check([self.review, self.review])

    def test_missing_attestation_fails(self) -> None:
        with self.assertRaisesRegex(ValueError, "human-authorship attestation"):
            self.check([{**self.review, "humanAuthored": False}])

    def test_null_author_fails(self) -> None:
        with self.assertRaisesRegex(ValueError, "named author and reviewer"):
            self.check([{**self.review, "author": None}])


if __name__ == "__main__":
    unittest.main()
