#!/usr/bin/env python3
"""Write one bounded, sanitized runtime snapshot for cloud-task troubleshooting.

The logger executes only fixed, read-only diagnostics. It never logs process
arguments, environment variables, command output wholesale, credentials, or file
contents. Story-review counts are ledger labels only, not proof of semantic review.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
from urllib.parse import urlsplit, urlunsplit
import uuid


ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "diagnostics" / "cloud_task_runtime.jsonl"
MAX_LOG_BYTES = 64 * 1024
BRANCH = "codex/macau-story-upgrade-batch-progress"
LEDGER = "STORY_QUALITY_REVALIDATION.json"
REMOTE_REF = f"refs/heads/{BRANCH}"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds")


def sanitize(text: str, limit: int = 500) -> str:
    text = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", text)
    text = re.sub(r"(?i)\bBearer\s+\S+", "Bearer <redacted>", text)
    text = re.sub(
        r"(?i)(token|password|passwd|secret|authorization|cookie)\s*[:=]\s*\S+",
        r"\1=<redacted>",
        text,
    )
    def safe_url(match: re.Match[str]) -> str:
        raw = match.group(0).rstrip(".,;)")
        try:
            parts = urlsplit(raw)
            host = parts.hostname or "<redacted-host>"
            if parts.port:
                host += f":{parts.port}"
            safe = urlunsplit((parts.scheme, host, parts.path, "<redacted>" if parts.query else "", ""))
            return safe + match.group(0)[len(raw):]
        except ValueError:
            return "<redacted-url>"

    text = re.sub(r"https?://[^\s<>\"']+", safe_url, text, flags=re.IGNORECASE)
    text = re.sub(r"\b(?:gh[pousr]_[A-Za-z0-9_]{12,}|github_pat_[A-Za-z0-9_]{12,}|sk-[A-Za-z0-9_-]{16,}|xox[baprs]-[A-Za-z0-9-]{12,})\b", "<redacted-token>", text)
    text = re.sub(r"\bAKIA[0-9A-Z]{16}\b", "<redacted-key>", text)
    text = re.sub(r"(https?://)[^/@\s]+:[^/@\s]+@", r"\1<redacted>@", text)
    return text.strip()[:limit]


def run_check(name: str, argv: list[str], timeout: float = 8.0) -> dict:
    started_at = utc_now()
    t0 = time.monotonic()
    try:
        p = subprocess.run(
            argv,
            cwd=ROOT,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
            check=False,
            shell=False,
        )
        return {
            "name": name,
            "started_at_utc": started_at,
            "ended_at_utc": utc_now(),
            "duration_ms": round((time.monotonic() - t0) * 1000),
            "exit_status": p.returncode,
            "stdout": p.stdout,
            "error": sanitize(p.stderr) if p.returncode else None,
        }
    except subprocess.TimeoutExpired:
        return {
            "name": name,
            "started_at_utc": started_at,
            "ended_at_utc": utc_now(),
            "duration_ms": round((time.monotonic() - t0) * 1000),
            "exit_status": None,
            "error": f"timeout after {int(timeout * 1000)} ms",
        }
    except Exception as exc:  # diagnostic failure only; do not hide it
        return {
            "name": name,
            "started_at_utc": started_at,
            "ended_at_utc": utc_now(),
            "duration_ms": round((time.monotonic() - t0) * 1000),
            "exit_status": None,
            "error": sanitize(f"{type(exc).__name__}: {exc}"),
        }


def short_lines(result: dict, count: int = 8, chars: int = 1600) -> list[str] | None:
    if result.get("exit_status") != 0:
        return None
    return [sanitize(x, 240) for x in result.get("stdout", "").splitlines()[:count]][:count]


def git_dirty_summary(result: dict) -> dict:
    raw = result.get("stdout", "")
    names: list[str] = []
    for line in raw.splitlines():
        if len(line) >= 4:
            names.append(sanitize(line[3:], 240))
    return {"count": len(names), "paths": names[:80]}


def ledger_counts(path: Path) -> dict:
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
        cards = d.get("cards", [])
        return {
            "pass": sum(c.get("status") == "pass" for c in cards),
            "needs_revision": sum(c.get("status") == "needs_revision" for c in cards),
            "pending": sum(c.get("status") == "pending" for c in cards),
            "total": len(cards),
        }
    except Exception as exc:
        return {"error": f"{type(exc).__name__}: ledger could not be read"}


def ledger_map(data: dict) -> dict[tuple[str, int], tuple[str, str]]:
    return {
        (c.get("file", ""), int(c.get("index", -1))): (
            c.get("status", ""), c.get("v2_sha256", "")
        )
        for c in data.get("cards", [])
    }


def changed_pass_rows(local_path: Path, base_json: str | None) -> int | None:
    if base_json is None:
        return None
    try:
        local = json.loads(local_path.read_text(encoding="utf-8"))
        base = json.loads(base_json)
        before, after = ledger_map(base), ledger_map(local)
        return sum(
            status == "pass" and before.get(key) != (status, digest)
            for key, (status, digest) in after.items()
        )
    except Exception:
        return None


def rotate_bounded(line: bytes) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    if len(line) > MAX_LOG_BYTES:
        raise ValueError("diagnostic record exceeds maximum log size")
    prior = LOG.with_suffix(LOG.suffix + ".1")
    if LOG.exists() and LOG.stat().st_size + len(line) > MAX_LOG_BYTES:
        if prior.exists():
            prior.unlink()
        os.replace(LOG, prior)
    with LOG.open("ab") as f:
        f.write(line)


def overall_failures(checks: dict, branch: str, remote_sha: str | None, head: str) -> list[str]:
    failed = [name for name, result in checks.items() if result.get("exit_status") != 0]
    if branch != BRANCH:
        failed.append("expected_branch")
    if not remote_sha:
        failed.append("remote_sha_unavailable")
    if remote_sha and head != remote_sha:
        failed.append("remote_head_mismatch")
    return sorted(set(failed))


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--environment-id", default=None)
    ap.add_argument("--provider", default=None)
    ap.add_argument("--connectivity", default=None)
    ap.add_argument("--observed-phase", default=None)
    ap.add_argument("--spec-revision", default=None)
    ap.add_argument("--network-policy-state", default=None)
    args = ap.parse_args()

    run_id = str(uuid.uuid4())
    started = utc_now()
    checks = {
        "pwd": run_check("pwd", ["pwd"]),
        "branch": run_check("branch", ["git", "rev-parse", "--abbrev-ref", "HEAD"]),
        "head": run_check("head", ["git", "rev-parse", "HEAD"]),
        "status": run_check("status", ["git", "status", "--short"]),
        "remote": run_check("remote", ["git", "ls-remote", "origin", REMOTE_REF], 15.0),
        "disk": run_check("disk", ["df", "-h", "/workspace"]),
        "memory": run_check("memory", ["free", "-h"]),
        "load": run_check("load", ["uptime"]),
        "processes": run_check(
            "processes", ["ps", "-eo", "pid,comm,%cpu,%mem", "--sort=-%cpu"]
        ),
    }

    remote_sha = None
    remote_out = checks["remote"].get("stdout", "").split()
    if checks["remote"].get("exit_status") == 0 and len(remote_out) >= 2:
        if re.fullmatch(r"[0-9a-f]{40,64}", remote_out[0]):
            remote_sha = remote_out[0]

    head = checks["head"].get("stdout", "").strip()
    base_json = None
    if remote_sha:
        remote_ledger = run_check(
            "remote_ledger",
            ["git", "show", f"{remote_sha}:{LEDGER}"],
            8.0,
        )
        if remote_ledger.get("exit_status") == 0:
            base_json = remote_ledger.get("stdout")
        checks["remote_ledger"] = {
            k: v for k, v in remote_ledger.items() if k != "stdout"
        }

    local_counts = ledger_counts(ROOT / LEDGER)
    dirty = git_dirty_summary(checks["status"])
    local_unpushed_pass = changed_pass_rows(ROOT / LEDGER, base_json)
    process_lines = short_lines(checks["processes"], count=9, chars=1800)

    safe_checks = {}
    for name, result in checks.items():
        safe_checks[name] = {
            k: v
            for k, v in result.items()
            if k not in {"stdout"}
        }
    record = {
        "record_type": "runtime_snapshot",
        "run_id": run_id,
        "started_at_utc": started,
        "ended_at_utc": utc_now(),
        "environment": {
            "environment_id_fingerprint_sha256": (
                hashlib.sha256(args.environment_id.encode()).hexdigest()[:20]
                if args.environment_id else None
            ),
            "provider": sanitize(args.provider or "", 40) or None,
            "connectivity": sanitize(args.connectivity or "", 40) or None,
            "observed_phase": sanitize(args.observed_phase or "", 40) or None,
            "spec_revision": sanitize(args.spec_revision or "", 40) or None,
            "network_policy_state": sanitize(args.network_policy_state or "", 40) or None,
        },
        "git": {
            "expected_branch": BRANCH,
            "branch": sanitize(checks["branch"].get("stdout", "").strip(), 120),
            "head": sanitize(head, 80),
            "remote_sha": remote_sha,
            "remote_matches_head": bool(remote_sha and head == remote_sha),
            "dirty_file_count": dirty["count"],
            "dirty_paths": dirty["paths"],
        },
        "review_ledger": {
            **local_counts,
            "changed_pass_rows_vs_remote_ledger": local_unpushed_pass,
            "basis_note": "ledger statuses/hashes only; not semantic-review proof",
        },
        "resources": {
            "disk": short_lines(checks["disk"], count=3),
            "memory": short_lines(checks["memory"], count=4),
            "load": short_lines(checks["load"], count=1),
            "processes_pid_comm_cpu_mem_only": process_lines,
        },
        "checks": safe_checks,
    }
    failed_checks = overall_failures(checks, record["git"]["branch"], remote_sha, head)
    record["overall_status"] = "failed" if failed_checks else "ok"
    record["failed_checks"] = failed_checks
    line = (json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    rotate_bounded(line)

    print(json.dumps({
        "log_path": str(LOG.relative_to(ROOT)),
        "run_id": run_id,
        "branch": record["git"]["branch"],
        "head": record["git"]["head"],
        "remote_sha": remote_sha,
        "dirty_file_count": dirty["count"],
        "v2_pass": local_counts.get("pass"),
        "changed_pass_rows_vs_remote_ledger": local_unpushed_pass,
        "overall_status": record["overall_status"],
        "failed_checks": record["failed_checks"],
        "log_size_bytes": LOG.stat().st_size,
    }, ensure_ascii=False))
    return 0 if not failed_checks else 1


if __name__ == "__main__":
    raise SystemExit(main())
