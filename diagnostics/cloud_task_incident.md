# Cloud task executor incident note

Observation date: 2026-10-28 UTC

Task branch: `codex/macau-story-upgrade-batch-progress`

Last verified code/remote SHA: `e0f820da067ed52b7c9ad88e00d8e064728403fe`

## Evidence from this task

- On the preceding turn, a read-only `exec_command` failed before `pwd`/Git could run with the exact message: `No usable execution environment is available. Wait for an environment to become available before using this tool.` The failure time was not captured by the command logger; the user reported it at approximately 03:39 UTC.
- At the same time, `cloud_environment.environment_status` reported `connected`, `running`, and network policy `enforced`. The next direct shell probe succeeded at 03:40:18 UTC. A later one-shot diagnostic run at 03:43 UTC also succeeded; all fixed checks returned exit status 0.
- In the diagnostic run, `git ls-remote` completed in about 290 ms and confirmed the remote branch still matched local HEAD. Disk had about 30 GiB free, memory reported about 32 GiB available, and load average was 0.00. This makes resource exhaustion or a current Git/network outage less likely; it does not explain the earlier executor failure.
- The observed failure is therefore specifically consistent with a transient executor-unavailable/selection or provisioning gap before the command ran. The environment status endpoint did not reflect that transient gap. One incident is insufficient to identify a root cause.
- Story ledger snapshot: 1,289 V2 pass / 3,711 needs revision / 0 pending out of 5,000. The last verified remote ledger has no changed passing rows compared with the working ledger. Ledger labels and hashes are bookkeeping, not independent proof of language review.
- One candidate for `long_food_shopping_19.json[27]` is present in conversation but remains unapproved and was not written to the repository.

## Public reports checked

These are user reports in the public `openai/codex` issue tracker, not confirmed diagnoses or official recovery instructions:

- [#54764 — Codex cloud environments fail to publish across multiple projects; execution unavailable](https://github.com/openai/codex/issues/54764) reports cloud publish uncertainty and the same executor error across projects.
- [#54666 — Codex Cloud environment stuck offline](https://github.com/openai/codex/issues/54666) reports loss of workspace access with uncommitted changes and failed environment publishing.
- [#55654 — “No usable execution environment” across ChatGPT Work/Sites](https://github.com/openai/codex/issues/55654) reports the same message across clients, but concerns Sites/Work and is not confirmed to be this managed-cloud runtime.
- [#56517 — intermittent unavailable local executor despite connected desktop](https://github.com/openai/codex/issues/56517) describes a similar status/executor mismatch on Windows Local; that execution target differs from this cloud task.

The pages showed user reports and automated duplicate notices, not a maintainer-confirmed cause or supported fix. They support the symptom pattern only. No keepalive loop, environment reset/recreation, network-policy change, or credential inspection was used.

## Logger

`tools/cloud_task_diagnostics.py` runs a fixed, read-only snapshot. It records UTC start/end/duration and exit status per check; sanitized errors; a hashed environment identifier plus safe status fields; disk/memory/load and process names without arguments; branch/HEAD/dirty filenames; remote SHA; and V2 ledger counts/difference. It never records environment variables, process arguments, file contents, or credentials. The JSONL log rotates at 64 KiB with at most one previous copy. Diagnostic files live outside `content/` and are excluded from story-quality counts.

The logger was run once after the shell returned. Future failures that occur before the logger can start will still require an out-of-band task note or runtime-side log; this script cannot record an executor that never launched it.
