#!/usr/bin/env python3
"""Stable story IDs and reversible source archive access."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "content" / "story_source_index_map.json"
ARCHIVE_MANIFEST_PATH = ROOT / "content" / "story_archive" / "manifest.json"


def row_digest(row: dict) -> str:
    encoded = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_index() -> dict:
    if not INDEX_PATH.exists():
        raise ValueError(f"Missing stable source index map: {INDEX_PATH}")
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def archive_path(index: dict | None = None) -> Path:
    index = index or load_index()
    return ROOT / index["archive_path"]


def archive_manifest() -> dict:
    if not ARCHIVE_MANIFEST_PATH.exists():
        raise ValueError(f"Missing source archive manifest: {ARCHIVE_MANIFEST_PATH}")
    return json.loads(ARCHIVE_MANIFEST_PATH.read_text(encoding="utf-8"))


def archived_source_rows(index: dict | None = None) -> dict[tuple[str, int], dict]:
    """Load every original row from the immutable, byte-verified archive."""
    index = index or load_index()
    archive = archive_path(index)
    manifest = archive_manifest()
    archive_bytes = archive.read_bytes()
    if hashlib.sha256(archive_bytes).hexdigest() != manifest.get("archive_sha256"):
        raise ValueError("Story source archive SHA-256 does not match its manifest")
    rows: dict[tuple[str, int], dict] = {}
    with zipfile.ZipFile(archive) as bundle:
        for record in manifest["files"]:
            relative = record["path"]
            if not relative.startswith("content/sentence_bank/"):
                continue
            payload = bundle.read(f"snapshot/{relative}")
            if hashlib.sha256(payload).hexdigest() != record["sha256"]:
                raise ValueError(f"Archived source file hash mismatch: {relative}")
            parsed = json.loads(payload)
            if len(parsed) != record["rows"]:
                raise ValueError(f"Archived source row count mismatch: {relative}")
            for row_index, row in enumerate(parsed):
                rows[(relative, row_index)] = row
    if len(rows) != index.get("original_row_count"):
        raise ValueError("Archived story source row count does not match the index map")
    return rows


def active_rows_by_current_coordinate(index: dict | None = None) -> dict[tuple[str, int], dict]:
    """Return current compact source coordinates mapped to their stable ID rows."""
    index = index or load_index()
    result = {}
    for record in index["active_rows"]:
        key = (record["current_file"], record["current_index"])
        if key in result:
            raise ValueError(f"Duplicate current source coordinate in index map: {key}")
        result[key] = record
    return result


def all_rows_by_current_coordinate(index: dict | None = None) -> dict[tuple[str, int], dict]:
    """Return current source coordinates for either compact or restored state."""
    index = index or load_index()
    result = active_rows_by_current_coordinate(index)
    for record in index.get("archived_rows", []):
        if "current_file" not in record:
            continue
        key = (record["current_file"], record["current_index"])
        if key in result:
            raise ValueError(f"Duplicate current source coordinate in index map: {key}")
        result[key] = record
    return result


def active_id_by_original_coordinate(index: dict | None = None) -> dict[tuple[str, int], str]:
    index = index or load_index()
    return {
        (record["original_file"], record["original_index"]): record["id"]
        for record in index["active_rows"]
    }


def all_catalog_rows(index: dict | None = None) -> list[tuple[str, int, dict]]:
    """Return the full 5,000-row original catalog in its original ordering."""
    index = index or load_index()
    rows = archived_source_rows(index)
    return [(file, row_index, row) for (file, row_index), row in sorted(rows.items())]
