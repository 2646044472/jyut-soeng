"""Load individually edited readings. The original v0.36.3 snapshot remains restorable."""
import json
import re
from pathlib import Path

HAN = re.compile(r"[\u3400-\u9fff\uf900-\ufaff\U00020000-\U0002FA1F\U00030000-\U000323AF]")
SYLLABLE = re.compile(r"[a-z]+[1-6]")
SEPARATORS = re.compile(r"[\s,.?!:;，。？！：；、「」『』“”\"']")
# An editorial beat decides where a revised story ends; the archive keeps its old limit.
PROOFREAD_LENGTH = (220, None)
MIRROR = {"sentence": "displayText", "jyutping": "answerJyutping", "gloss": "gloss", "usageTip": "usageTip", "category": "category"}

def approved_story_ids(root: Path) -> set[str]:
    """The current editorial ledger, not the old 2,000-card pass flags or a file glob."""
    ledger = (root / "STORY_PROOFREAD_PROGRESS.md").read_text(encoding="utf-8")
    tally = re.search(r"当前轮次：([\d,]+)/2,000 已终校", ledger)
    if not tally:
        raise ValueError("Missing proofread ledger tally")
    rows = re.findall(r"^\| (\d{2}-\d{4}|\d{4})(?=\s)", ledger, re.MULTILINE)
    ids = {"sentence-bank-long_family_finance_services_" +
           (short if "-" in short else "01-" + short) for short in rows}
    if len(ids) != len(rows) or len(ids) != int(tally[1].replace(",", "")):
        raise ValueError("Proofread ledger contains duplicate/missing accepted IDs")
    return ids


def load_proofreads(root: Path, index: dict) -> dict[str, dict]:
    # An explicit snapshot restore builds precisely the snapshot, not later revisions.
    if index.get("source_layout") == "full_restored":
        return {}
    active = {x["id"] for x in index["active_rows"]}
    edits = {}
    for approved_id in sorted(approved_story_ids(root)):
        p = root / "content" / "story_proofread" / (approved_id + ".json")
        if p.stem not in active:
            raise ValueError(f"{p.name}: not an active story ID")
        d = json.loads(p.read_text(encoding="utf-8"))
        text, reading = [], []
        for i, (line, phon) in enumerate(d["beats"], 1):
            tokens = SYLLABLE.findall(phon)
            if (not tokens or "".join(tokens) != SEPARATORS.sub("", phon)
                    or len(tokens) != len(HAN.findall(line))):
                raise ValueError(f"{p.name} beat {i}: one numbered syllable per character required")
            text.append(line)
            reading.append(phon)
        edits[p.stem] = {"sentence": "".join(text), "jyutping": " ".join(reading),
                         **{k: d[k] for k in ("gloss", "usageTip", "category")}}
    return edits
