#!/usr/bin/env python3
"""Report mechanical progress for the hand-written sentence story upgrade."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
HAN_CHARACTER = re.compile(
    r"[\u3400-\u9fff\uf900-\ufaff\U00020000-\U0002FA1F\U00030000-\U000323AF]"
)
JYUTPING_TOKEN = re.compile(r"[a-z]+[1-6]")
ALLOWED_JYUTPING_SEPARATORS = re.compile(r"[,，.。:：;；?!？！、「」『』“”\"'\s]")
STORY_TIP_PREFIX = "故事练习："
LANGUAGE_REVIEW_PATH = ROOT / "STORY_LANGUAGE_REVIEW.json"
REVIEW_GOAL = 10_000


def row_digest(row: dict) -> str:
    encoded = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def language_reviews() -> dict[tuple[str, int], dict]:
    if not LANGUAGE_REVIEW_PATH.exists():
        return {}
    reviews = json.loads(LANGUAGE_REVIEW_PATH.read_text(encoding="utf-8"))
    indexed = {}
    for review in reviews:
        key = (review["file"], review["index"])
        if key in indexed:
            raise ValueError(f"Duplicate language review: {key}")
        indexed[key] = review
    return indexed


def audit(row: dict, selected: bool) -> list[str]:
    sentence_key = "displayText" if selected else "sentence"
    jyutping_key = "answerJyutping" if selected else "jyutping"
    sentence = str(row.get(sentence_key, "")).strip()
    jyutping = str(row.get(jyutping_key, "")).strip().lower()
    tokens = JYUTPING_TOKEN.findall(jyutping)
    han_count = len(HAN_CHARACTER.findall(sentence))
    residue = ALLOWED_JYUTPING_SEPARATORS.sub("", jyutping)
    failures: list[str] = []

    if not 220 <= han_count <= 320:
        failures.append("story-length")
    if not tokens or "".join(tokens) != residue or len(tokens) != han_count:
        failures.append("jyutping-alignment")
    if not str(row.get("gloss", "")).strip():
        failures.append("missing-gloss")
    elif len(HAN_CHARACTER.findall(str(row["gloss"]))) < 160:
        failures.append("short-gloss")
    if not str(row.get("usageTip", "")).startswith(STORY_TIP_PREFIX):
        failures.append("story-practice-tip")
    if not str(row.get("category", "")).strip():
        failures.append("missing-category")
    if not re.search(r"[。？！.!?][」』”\"]?$", sentence):
        failures.append("ending-punctuation")
    if "「" not in sentence or "」" not in sentence:
        failures.append("direct-dialogue")
    if re.search(r"[A-Za-z0-9]", sentence):
        failures.append("unaligned-latin-text")
    if sum(sentence.count(mark) for mark in ("，", "；", "？")) < 2:
        failures.append("story-turns")
    if selected and row.get("exampleSentence") != row.get("displayText"):
        failures.append("example-mismatch")
    return failures


def source_files() -> list[tuple[Path, bool]]:
    independent = [(path, False) for path in sorted((CONTENT_DIR / "sentence_bank").glob("*.json"))]
    selected = [(path, True) for path in sorted(CONTENT_DIR.glob("*sentence*_bank.json"))]
    return independent + selected


def render_report() -> tuple[str, int, int]:
    reviews = language_reviews()
    reviewed = 0
    matched_reviews = set()
    sections: list[str] = [
        "# Sentence Story Quality Checklist",
        "",
        "Mechanical status only: counts cover story length, Jyutping token alignment, required fields, story tips, punctuation, and selected-card example consistency. A passing row still needs human review for natural Macau Cantonese, accurate readings, complete translation, and a distinct story.",
        "",
        "| Source file | Mechanical pass | Needs work |",
        "| --- | ---: | ---: |",
    ]
    total = 0
    passing = 0
    for path, selected in source_files():
        rows = json.loads(path.read_text(encoding="utf-8"))
        for index, row in enumerate(rows):
            key = (path.relative_to(ROOT).as_posix(), index)
            review = reviews.get(key)
            if review is not None:
                matched_reviews.add(key)
                if review["sha256"] != row_digest(row):
                    raise ValueError(f"Stale language review: {key}")
                dimensions = ("naturalness", "distinct_plot", "jyutping_readings_and_tones", "complete_gloss")
                if all(review.get(dimension) is True for dimension in dimensions) and not audit(row, selected):
                    reviewed += 1
        passed = sum(not audit(row, selected) for row in rows)
        total += len(rows)
        passing += passed
        sections.append(f"| `{path.relative_to(ROOT).as_posix()}` | {passed}/{len(rows)} | {len(rows) - passed} |")
    if matched_reviews != reviews.keys():
        raise ValueError("Language review references missing source rows")
    sections.extend((
        "", f"**Overall mechanical pass: {passing}/{total}.**", "",
        f"**Goal (main-agent language review): {min(reviewed, REVIEW_GOAL)}/{REVIEW_GOAL}; remaining to goal: {max(0, REVIEW_GOAL - reviewed)}.**", "",
        f"**Corpus language review: {reviewed}/{total}; source rows without a valid review: {total - reviewed}.**", "",
        "Language review records are maintained manually in `STORY_LANGUAGE_REVIEW.json`; hashes only detect later edits, they do not assess language quality. Existing mechanically passing stories without a recorded review remain pending language review.", "",
    ))
    return "\n".join(sections), passing, total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        help="Write the generated checklist to this path; otherwise print it.",
    )
    parser.add_argument("--require-complete", action="store_true", help="Fail unless every source card passes story acceptance.")
    args = parser.parse_args()
    report, passing, total = render_report()
    if args.output:
        output_path = args.output if args.output.is_absolute() else ROOT / args.output
        output_path.write_text(report, encoding="utf-8")
        print(f"Wrote mechanical checklist to {output_path}")
    else:
        print(report, end="")
    if args.require_complete and passing != total:
        raise SystemExit(f"Story upgrade incomplete: {passing}/{total} mechanically accepted.")


if __name__ == "__main__":
    main()
