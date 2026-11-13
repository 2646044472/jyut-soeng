#!/usr/bin/env python3
"""Archive the v0.36.3 story catalog and compact active source rows safely.

This is deterministic file maintenance only. It never rewrites story language.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BASELINE = "f754289396483da8ecc9111137bd183cc88dc574"
ARCHIVE_REL = "content/story_archive/jyut-soeng-original-source-v0.36.3.zip"
INDEX_REL = "content/story_source_index_map.json"
MANIFEST_REL = "content/story_archive/manifest.json"
SOURCE_DIR = "content/sentence_bank"
SNAPSHOT_FILES = (
    "STORY_QUALITY_REVALIDATION.json",
    "STORY_QUALITY_ORAL_REAUDIT.json",
    "content/story_library_selection.json",
    "app/src/main/assets/builtin/content.json",
)


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonical_sha(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(payload)


def git_show(revision: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{revision}:{path}"], cwd=ROOT, check=True, capture_output=True
    ).stdout


def source_paths_at_baseline() -> list[str]:
    result = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", BASELINE, SOURCE_DIR],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )
    return sorted(line for line in result.stdout.splitlines() if line.endswith(".json"))


def main() -> None:
    archive_path = ROOT / ARCHIVE_REL
    index_path = ROOT / INDEX_REL
    manifest_path = ROOT / MANIFEST_REL
    if archive_path.exists() or index_path.exists() or manifest_path.exists():
        raise SystemExit("Source archive artifacts already exist; refusing to overwrite them")

    source_paths = source_paths_at_baseline()
    snapshot_paths = source_paths + list(SNAPSHOT_FILES)
    original: dict[str, bytes] = {}
    for relative in snapshot_paths:
        baseline_bytes = git_show(BASELINE, relative)
        worktree_path = ROOT / relative
        if not worktree_path.is_file() or worktree_path.read_bytes() != baseline_bytes:
            raise SystemExit(f"Current file is not byte-identical to v0.36.3; refusing migration: {relative}")
        original[relative] = baseline_bytes

    selection = json.loads(original["content/story_library_selection.json"])
    active_ids = selection["active_ids"]
    excluded_ids = selection["excluded_ids"]
    if len(active_ids) != 2000 or len(excluded_ids) != 3000 or set(active_ids) & set(excluded_ids):
        raise SystemExit("Selection is not the expected disjoint 2,000/3,000 partition")

    app = json.loads(original["app/src/main/assets/builtin/content.json"])
    app_entries = app.get("entries", [])
    app_story_ids = [entry["id"] for entry in app_entries if entry.get("id", "").startswith("sentence-bank-")]
    if set(app_story_ids) != set(active_ids) or len(app_story_ids) != 2000:
        raise SystemExit("v0.36.3 app bundle does not contain exactly the selected 2,000 stories")

    active_set, excluded_set = set(active_ids), set(excluded_ids)
    active_rows: list[dict] = []
    archived_rows: list[dict] = []
    compacted: dict[str, bytes] = {}
    original_row_count = 0
    file_records: list[dict] = []
    for relative in source_paths:
        raw = original[relative]
        rows = json.loads(raw)
        file_records.append({"path": relative, "sha256": sha256(raw), "rows": len(rows)})
        new_rows = []
        for original_index, row in enumerate(rows):
            entry_id = f"sentence-bank-{Path(relative).stem}-{original_index + 1:04d}"
            digest = canonical_sha(row)
            original_row_count += 1
            if entry_id in active_set:
                current_index = len(new_rows)
                new_rows.append(row)
                active_rows.append({
                    "id": entry_id,
                    "current_file": relative,
                    "current_index": current_index,
                    "original_file": relative,
                    "original_index": original_index,
                    "original_row_sha256": digest,
                })
            elif entry_id in excluded_set:
                archived_rows.append({
                    "id": entry_id,
                    "original_file": relative,
                    "original_index": original_index,
                    "original_row_sha256": digest,
                    "archive_member": f"snapshot/{relative}",
                })
            else:
                raise SystemExit(f"Source row is not covered by selection: {entry_id}")
        compacted[relative] = (json.dumps(new_rows, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

    if original_row_count != 5000 or len(active_rows) != 2000 or len(archived_rows) != 3000:
        raise SystemExit("Source rows do not match the expected 5,000/2,000/3,000 counts")
    if {row["id"] for row in active_rows} != active_set or {row["id"] for row in archived_rows} != excluded_set:
        raise SystemExit("Source IDs do not match the active/excluded partition")

    index_map = {
        "schema_version": 1,
        "source_layout": "compact_active",
        "source_snapshot_commit": BASELINE,
        "archive_path": ARCHIVE_REL,
        "original_source_file_count": len(source_paths),
        "original_row_count": original_row_count,
        "active_count": len(active_rows),
        "archived_count": len(archived_rows),
        "active_rows": active_rows,
        "archived_rows": archived_rows,
    }

    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for relative in sorted(original):
            info = zipfile.ZipInfo(f"snapshot/{relative}", date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, original[relative], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    manifest = {
        "schema_version": 1,
        "source_snapshot_commit": BASELINE,
        "archive_path": ARCHIVE_REL,
        "archive_sha256": sha256(archive_path.read_bytes()),
        "original_source_file_count": len(source_paths),
        "original_row_count": original_row_count,
        "active_count": len(active_rows),
        "archived_count": len(archived_rows),
        "release_app_entry_count": len(app_entries),
        "release_story_count": len(app_story_ids),
        "release_app_entries_sha256": canonical_sha(app_entries),
        "release_story_id_order_sha256": canonical_sha(app_story_ids),
        "files": file_records + [
            {"path": relative, "sha256": sha256(original[relative]), "rows": None}
            for relative in SNAPSHOT_FILES
        ],
    }

    # Persist the immutable archive and both indexes before compacting any source file.
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    index_path.write_text(json.dumps(index_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for relative, payload in compacted.items():
        (ROOT / relative).write_bytes(payload)

    current_counts = [len(json.loads((ROOT / relative).read_text(encoding="utf-8"))) for relative in source_paths]
    if sum(current_counts) != 2000:
        raise SystemExit("Post-migration source count is not 2,000; the archive remains available for recovery")
    print(json.dumps({
        "archive": ARCHIVE_REL,
        "archive_sha256": manifest["archive_sha256"],
        "original_source_rows": original_row_count,
        "active_source_rows": sum(current_counts),
        "archived_source_rows": len(archived_rows),
        "source_files": len(source_paths),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
