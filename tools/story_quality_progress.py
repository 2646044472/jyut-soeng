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
QUALITY_REVALIDATION_PATH = ROOT / "STORY_QUALITY_REVALIDATION.json"
REVIEW_GOAL = 5_000
ACTIVE_REVIEW_ROUND = "macau-comedy-upgrade-v1"
ACTIVE_REVALIDATION_ROUND = "macau-comedy-revalidation-v2"


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


def quality_revalidations() -> dict[tuple[str, int], dict]:
    ledger = json.loads(QUALITY_REVALIDATION_PATH.read_text(encoding="utf-8"))
    if ledger.get("review_round") != ACTIVE_REVALIDATION_ROUND:
        raise ValueError("Unexpected quality revalidation round")
    indexed = {}
    for record in ledger.get("cards", []):
        key = (record["file"], record["index"])
        if key in indexed:
            raise ValueError(f"Duplicate quality revalidation: {key}")
        indexed[key] = record
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
    revalidations = quality_revalidations()
    reviewed = 0
    v2_passed = 0
    v2_needs_revision = 0
    v2_pending = 0
    matched_reviews = set()
    matched_revalidations = set()
    valid_reviewed_keys = set()
    source_keys = []
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
            source_keys.append(key)
            review = reviews.get(key)
            if review is not None:
                matched_reviews.add(key)
                dimensions = ("naturalness", "distinct_plot", "jyutping_readings_and_tones", "complete_gloss")
                if (
                    review.get("sha256") == row_digest(row)
                    and review.get("review_round") == ACTIVE_REVIEW_ROUND
                    and all(review.get(dimension) is True for dimension in dimensions)
                    and not audit(row, selected)
                ):
                    reviewed += 1
                    valid_reviewed_keys.add(key)
            revalidation = revalidations.get(key)
            if revalidation is not None:
                matched_revalidations.add(key)
                status = revalidation.get("status")
                current_hash = row_digest(row)
                if status in {"pass", "needs_revision"} and revalidation.get("v2_sha256") != current_hash:
                    raise ValueError(f"Stale quality revalidation: {key}")
                if status == "pass":
                    v2_passed += 1
                elif status == "needs_revision":
                    v2_needs_revision += 1
                elif status == "pending":
                    v2_pending += 1
                else:
                    raise ValueError(f"Unknown quality revalidation status {status!r}: {key}")
        passed = sum(not audit(row, selected) for row in rows)
        total += len(rows)
        passing += passed
        sections.append(f"| `{path.relative_to(ROOT).as_posix()}` | {passed}/{len(rows)} | {len(rows) - passed} |")
    if matched_reviews != reviews.keys():
        raise ValueError("Language review references missing source rows")
    if matched_revalidations != revalidations.keys() or len(revalidations) != total:
        raise ValueError("Quality revalidation ledger does not match source rows")
    goal_keys = source_keys[:REVIEW_GOAL]
    goal_key_set = set(goal_keys)
    goal_reviewed = sum(key in valid_reviewed_keys for key in goal_keys)
    contiguous_prefix = 0
    for key in goal_keys:
        if key not in valid_reviewed_keys:
            break
        contiguous_prefix += 1
    first_goal_gap = next((key for key in goal_keys if key not in valid_reviewed_keys), None)
    reviewed_outside_goal = sum(key not in goal_key_set for key in valid_reviewed_keys)
    sections.extend((
        "", f"**Overall mechanical pass: {passing}/{total}.**", "",
        f"**Goal (main-agent language review within the first {REVIEW_GOAL} source rows): {goal_reviewed}/{min(REVIEW_GOAL, total)}; remaining: {max(0, min(REVIEW_GOAL, total) - goal_reviewed)}.**", "",
        f"**Contiguous reviewed source-order prefix: {contiguous_prefix}/{min(REVIEW_GOAL, total)}.**", "",
        f"**First uncovered goal row: `{first_goal_gap[0]}` index {first_goal_gap[1]}.**" if first_goal_gap else "**First uncovered goal row: none.**", "",
        f"**Valid language reviews outside the first {REVIEW_GOAL} source rows: {reviewed_outside_goal}.**", "",
        f"**Corpus language review: {reviewed}/{total}; source rows without a valid review: {total - reviewed}.**", "",
        f"**Clarified quality revalidation (`{ACTIVE_REVALIDATION_ROUND}`): {v2_passed}/{total} pass; {v2_needs_revision} need revision; {v2_pending} pending.**", "",
        f"`STORY_LANGUAGE_REVIEW.json` remains the historical `{ACTIVE_REVIEW_ROUND}` ledger. A stale historical hash is not current approval. `STORY_QUALITY_REVALIDATION.json` records current hashes and individual revalidation decisions; hashes verify synchronization but do not assess language quality.", "",
    ))
    return "\n".join(sections), passing, total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        help="Write the generated checklist to this path; otherwise print it.",
    )
    parser.add_argument("--require-complete", action="store_true", help="Fail unless every source card mechanically passes and has a current v2 pass.")
    args = parser.parse_args()
    report, passing, total = render_report()
    if args.output:
        output_path = args.output if args.output.is_absolute() else ROOT / args.output
        output_path.write_text(report, encoding="utf-8")
        print(f"Wrote mechanical checklist to {output_path}")
    else:
        print(report, end="")
    if args.require_complete:
        revalidations = quality_revalidations()
        accepted = sum(record.get("status") == "pass" for record in revalidations.values())
        if passing != total or accepted != total:
            raise SystemExit(f"Story upgrade incomplete: {accepted}/{total} v2 reviewed, {passing}/{total} mechanically accepted.")


if __name__ == "__main__":
    main()
