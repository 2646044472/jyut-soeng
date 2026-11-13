#!/usr/bin/env python3
"""Verify or explicitly restore the complete v0.36.3 story source snapshot."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from story_source_index import INDEX_PATH, ROOT, archive_manifest, archive_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--restore", action="store_true", help="write original snapshot files under the selected destination")
    parser.add_argument("--include-app", action="store_true", help="also restore the v0.36.3 bundled app asset")
    parser.add_argument("--destination", type=Path, default=ROOT, help="restore root (defaults to the repository)")
    args = parser.parse_args()

    manifest = archive_manifest()
    archive = archive_path()
    if hashlib.sha256(archive.read_bytes()).hexdigest() != manifest["archive_sha256"]:
        raise SystemExit("Archive SHA-256 mismatch; refusing to read or restore it")

    with zipfile.ZipFile(archive) as bundle:
        for record in manifest["files"]:
            relative = record["path"]
            if relative.startswith("app/") and not args.include_app:
                continue
            payload = bundle.read(f"snapshot/{relative}")
            if hashlib.sha256(payload).hexdigest() != record["sha256"]:
                raise SystemExit(f"Archive member checksum mismatch: {relative}")
            if args.restore:
                target = args.destination / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(payload)

    if args.restore:
        restored_index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        restored_index["source_layout"] = "full_restored"
        for record in restored_index["active_rows"] + restored_index["archived_rows"]:
            record["current_file"] = record["original_file"]
            record["current_index"] = record["original_index"]
        index_target = args.destination / INDEX_PATH.relative_to(ROOT)
        index_target.parent.mkdir(parents=True, exist_ok=True)
        index_target.write_text(json.dumps(restored_index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.restore:
        print(f"Original files restored from the verified archive under {args.destination}.")
    else:
        print(f"Archive verified: {manifest['original_row_count']} original story rows, {len(manifest['files'])} files.")
        print("Pass --restore to restore the source, selection, and review ledgers; add --include-app to restore the v0.36.3 app asset.")


if __name__ == "__main__":
    main()
