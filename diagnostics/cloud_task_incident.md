# Cloud task executor incident note

Observation date: 2026-10-28 UTC

Task branch: `codex/macau-story-upgrade-batch-progress`

Last verified code/remote SHA: `e0f820da067ed52b7c9ad88e00d8e064728403fe`

## Evidence from this task

- On the preceding turn, a read-only `exec_command` failed before `pwd`/Git could run with the exact message: `No usable execution environment is available. Wait for an environment to become available before using this tool.` The exact failure time is unknown. A task message around 03:39 UTC conveyed the failure; that message time is not evidence of when it occurred.
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

The logger runs after shell access returns. Future failures that occur before the logger can start will still require an out-of-band task note or runtime-side log; this script cannot record an executor that never launched it.

## Follow-up snapshot and logger corrections

- A second successful snapshot ran at 2026-10-28 03:48 UTC. It saw the expected branch and matching local/remote SHA `2def675cc7bfd627323b3e5f48ed848f2f618f0a`, with 1,290 V2 ledger passes and no changed passing rows versus the remote ledger. Every fixed check exited 0. The earlier unavailability remains a single transient observation; no root cause is established.
- The logger no longer appends a historical failure event with an inferred timestamp. Historical timing remains described here as unknown. New snapshots record an overall status and return nonzero when required checks fail. URL queries/fragments and recognized token formats are redacted from error text.
- The V2 mechanical audit identified 13 rows in `long_family_finance_services_05.json` previously marked pass despite deterministic failures. They were reopened and then repaired/re-reviewed: indices 26, 31, 39, 41, 42, 43, 45, 46, 48, 49, 76, 95, and 97. Corrections replaced unaligned `DJ` with Cantonese wording and matching Jyutping, restored eleven required story-tip prefixes, and replaced an unspoken em dash with a mechanically aligned comma. All 13 current rows pass the deterministic audit, their V2 hashes were updated, and the total remains 1,290 pass / 3,710 needing revision. This mechanical status is not a substitute for the full-corpus quality work.

## Resource snapshot

At 2026-10-28 03:59:50 UTC, the checkout container reported AMD EPYC 9V74 80-Core Processor as its CPU model and exposed 5 logical CPUs. `/sys/fs/cgroup/cpu.max` was `400000 100000`, equivalent to a 4-CPU quota; host-visible CPU counts do not establish a dedicated allocation. Host-visible memory was 33 GiB total / 32 GiB available, while the cgroup memory cap was 32 GiB and current use about 69 MiB. The checkout filesystem was 32 GiB total / 30 GiB available. `nvidia-smi` and `rocm-smi` were not installed, so GPU availability is unknown. The diagnostic logger now records host-visible CPU model/count, cgroup CPU/memory limits and current use, and whether those GPU query tools exist.

## Work after the diagnostic snapshot

After the snapshot, the main agent completed the individual four-field review of `long_food_shopping_19.json[27]`, corrected the Jyutping for 抱 to `pou5`, and prepared its source/ledger update. The diagnostic JSONL is a point-in-time record and still correctly reports the earlier 1,289 pass count; the row is not included in that snapshot.


## 2026-10-29 intermittent exec-server outage

- Three calls failed before shell execution: two `exec-server transport disconnected` errors (the second reported session recovery timing out after 25 seconds) and a later `No usable execution environment is available` error. The affected calls were one edit invocation for `long_food_shopping_17[7]` and two read-only probes. All three failed at process creation; none of their command bodies ran. The attempted card edit was subsequently completed and saved in the repo.
- Exact per-error timestamps were not captured by the executor. The first successful recovery probe emitted `2026-10-29 05:12:42 UTC`; the failures occurred before that. I recorded the events with null exact timestamps and this explicit bound in `cloud_task_runtime.jsonl` rather than inferring exact times.
- The cloud environment status endpoint reported `connected/running` and policy `enforced` after recovery. The post-recovery resource check showed about 30 GiB free on the 32 GiB workspace filesystem and about 16 GiB memory available. `ps` showed only defunct Git processes; no active Git push was running. The status/resource check at 05:12:42 succeeded, and a current status read at 05:13 UTC again reported connected/running.
- No network/security settings were changed, and no workspace reset, cleanup, archive, or rebuild was performed. The cause remains undetermined; diagnostics support an intermittent executor transport/availability fault rather than disk or memory exhaustion.
