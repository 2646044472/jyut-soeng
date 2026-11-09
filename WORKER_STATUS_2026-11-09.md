# Worker Status — 2026-11-09

## Latest verified checkpoint

- Repository: `2646044472/jyut-soeng`; branch: `codex/macau-story-upgrade-batch-progress-resume`. Before this checkpoint, local HEAD and a fresh `git ls-remote` both showed `1a4844fc744d3faf0d514d64baee884354c9f837` on the resume branch. The original `codex/macau-story-upgrade-batch-progress` branch is separate at `3839000bf6829de38abb3027a48174b2c00cd83d`; it was not changed.
- Original source set remains 5,000 cards with IDs, order, categories, metadata and drafts retained. Active/excluded manifest is exactly 2,000/3,000 and disjoint. No cards were deleted.
- Active oral re-audit: **1,679 pass / 27 needs_revision / 294 pending**. Active V2 ledger: **2,000 pass / 0 needs_revision / 0 pending**. Corpus-wide V2: **2,296 pass / 2,704 needs_revision / 0 pending**. There are **50 new active oral pass transitions** versus HEAD `1a4844f`, with no oral-pass regressions.
- This batch integrated and rechecked 50 pass transitions, including `long_family_finance_services_10[41]`, `long_food_shopping_13`, `long_health_services_07/08`, plus active food and health batches. Revisions corrected incomplete Mandarin glosses, non-Mandarin prompts, mixed-script Cantonese, Jyutping readings/spacing, an unsafe mushroom instruction, unsafe gas-cylinder handling, and unclear egg-salad preparation. Original card IDs/categories and metadata were preserved; family/money-centered items received sparse-selection topic flags.
- `story_quality_progress.py` refreshed the checklist; `build_assets.py` generated **5,000 bundle entries**; `validate_content.py --require-story-upgrade --min-sentences 2000` passed for all 5,000 entries; `git diff --check` passed. The complete application/unit-test suites have **not** run because final library selection is still in progress. No APK, release, tag, deployment or publication occurred.
- Oral and V2 hashes were synchronized after each source change. The app content mirror was rebuilt from source. External candidate drafts and original source snapshots remain preserved in the working tree; draft-only changes are intentionally not part of the checkpoint commit.
- Root is the sole repository writer. Subagents returned read-only reviews and candidate text only; there are no active subagent writes. Effective model/effort receipts are unavailable, so GPT-6 Luna/high execution is not claimed.
- Next action: stage only reviewed source rows, ledgers, generated checklist/mirror, and this checkpoint note; commit/push to the resume branch, then verify the pushed SHA independently. Continue reviewing the remaining 294 active pending cards and 27 active revisions. Do not publish a release or APK until the user’s roughly 500-pass milestone and final selection/testing conditions are met.

## Earlier work log

The notes below record earlier checkpoints and may be superseded by the verified counts and test results above. Candidate drafts remain in their original external draft locations; no source file or draft was reset or cleaned.

## Workers

The main agent is the sole repository writer and owns card acceptance, ledgers, mirrors, validation, commits, and push. Subagents write only external drafts or report candidate screening.

| Worker | Card scope / work | Status | Model / reasoning evidence |
| --- | --- | --- | --- |
| `/root` | Integrated and manually reviewed the current batch; verified active membership, hashes, source/mirror consistency, and remote SHA. | Running; sole repo writer. | System identifies the Codex runtime as GPT-6. The available context does not expose a model variant or reasoning-strength setting; Luna/high is not verified. |
| `/root/batch73_drafts_a` | Drafted `long_food_shopping_18[13]` / `...18-0014` (accepted earlier) and `long_home_family_08[11]` / `...08-0012` (accepted this turn); both drafts remain external. | Completed. | No model/effort receipt exposed by the collaboration interface; actual model and strength unverified. |
| `/root/batch73_drafts_b` | Screened `long_home_family_08[49]` / `...08-0050` and other candidates; no new draft met the requested distinctness screen. | Completed; no repo changes. | No model/effort receipt exposed; actual model and strength unverified. |
| `/root/batch73_drafts_c` | Screened active pending home-source cards for a roommate/neighbour story that preserves the category; rejected mismatched or duplicate candidates. | Completed; no new draft. | No model/effort receipt exposed; actual model and strength unverified. |
| `/root/active2000_batch74_drafts` | Screened active/pending/V2-pass workplace, roommate, commute, or community cards. | Completed; no draft because its candidate screen found no compliant card. | Spawn requested `gpt-6-luna` with `high` reasoning through explicit tool parameters. The spawn result returned the worker name only, so the effective model/effort is not independently confirmed. |

Latest update: the collaboration tool completed batch74 without a draft after finding no eligible cards under its narrow workplace/commute/community screen; no repository change came from it. Batch73-A delivered `long_home_family_08[11]` as an external roommate draft. Root compared it with active passes on lost chore rotas and dishes cleared too early, adjusted `水槽` to colloquial `鋅盤` / `sing1 pun2`, then independently checked all four fields and accepted the card. Root subsequently improved the closing callback and manually synchronized Jyutping, Mandarin gloss and practice prompt. Current SHA-256: `5299e226a5b1e99a660abb0b7f25eb492fe2ed9b6a41bee8b4dc201aa59111a8`. Batch73-B reported that its candidate screen was too narrow and produced no draft; both A and B are now complete. The 08[11] draft remains preserved in the external DevWork draft folder.

The collaboration view exposes these canonical worker names, but no separate numeric worker IDs. Existing follow-up runs A/B/C cannot be reconfigured without interrupting them, and their runtime model/effort receipts are not exposed. The new D worker was launched with explicit `gpt-6-luna` / `high` parameters; the tool did not return a runtime confirmation.

Batch75 rechecked three active/pending/V2-pass candidates against current canonical hashes, all exact matches. `long_food_shopping_16[2]` centers on fish-market inspection/sign-off; `[4]` reuses a step-count/after-meal walk mechanism near an active seaside-route story; `long_food_shopping_19[33]` uses vegetable queues/attendance, near an active roll-call story. No draft was created because each would risk preserving the repeated mechanism. No repository or ledger change came from these screenings. Batch75 workers were requested as Luna/high, but their effective model/effort was not confirmed by tool receipts.

Batch76 revalidated three more exact-hash active/pending/V2-pass candidates. `long_food_shopping_15[9]` repeats label/list mix-ups in a frozen pickup; `18[18]` repeats frozen peas spilling and being chased from active `07[96]`; `14[20]` repeats cookie-map/chocolate-marker navigation already called out in its ledger notes. No draft qualified, and no repo or ledger status changed.

Latest continuation requested external drafts for all six active `needs_revision` cards, in three pairs. The first pass from agents A and C produced no drafts after locating further overlap; root then told both to radically replace the story mechanism while preserving ID/category/metadata and to deliver a complete four-field draft. Agent B is still working. This scope change addresses the repeated screening dead end. Root also improved already-passed `long_home_family_08[11]` by changing the final beat to the roommate asking whether the sink itself belongs on the chore chart; rechecked 256 Han / 256 Jyutping syllables and synchronized both ledger hashes and the app mirror. Full content build, 5,000-entry validator and diff check passed afterward. No unit tests or Android build ran.

No GPU was used. No unit-test suite or Android build was run for this checkpoint. `build_assets.py` and `validate_content.py --require-story-upgrade --min-sentences 2000` completed successfully after the new card; the validator checked 5,000 content entries. The new card is 256 Han characters / 256 Jyutping syllables, and both oral/V2 ledger hashes match its source row. `git diff --check` is clean. The latest-history thread API again returned a durable-host unavailable error; the old task was not restarted. The worktree remains at 41 net new passes, below the ~50-card checkpoint; no commit/push or release has been made.


## Checkpoint update — 2026-11-09 (50-pass threshold)

- Correctly integrated and independently reviewed `long_food_shopping_18[19]`; the soup story matches its tofu-and-soup category. All four fields and contextual Jyutping passed manual review, with an independent second review. Updated current oral and V2 hashes/statuses and rebuilt the app mirror.
- Active oral re-audit is now **1,516 pass / 0 needs_revision / 484 pending**; active V2 is **2,000 pass / 0 needs_revision / 0 pending**; corpus V2 is **2,296 pass / 2,704 needs_revision / 0 pending**. The previous top-line corpus values were stale; this checkpoint corrects them.
- Since the remote base, there are **50 active oral pass transitions**. Rechecked active selection counts and hashes. Remote fetch confirmed branch base still `71c8bae11e1a80b8a381c678c9522726795c6d42`; changes are ready for the 50-pass checkpoint commit/push.
- `python3 tools/story_quality_progress.py --output STORY_QUALITY_CHECKLIST.md`, `python3 tools/build_assets.py`, and `git diff --check` succeeded. Full validator and test suites remain unrun for this checkpoint; no APK/release/tag/deployment.


### Follow-on work since commit `d1b2645`

- Added eleven active oral passes: food cards `06[39,58,62]`, `07[7,14,25]`, `08[78,82,90]`, and household service cards `10[12,16]`. Each received manual four-field review; `06[39]` and `07[7]` had specific Jyutping/continuity issues corrected before approval; `10[16]` received independent final confirmation after two tone/word-reading fixes.
- Current active oral count: **1,527 pass / 0 needs_revision / 473 pending**. Active V2: **2,000 pass / 0 needs_revision / 0 pending**. Corpus V2: **2,296 pass / 2,704 needs_revision / 0 pending**. Eleven new pass transitions are unpushed, below the 50-pass checkpoint.
- `10[16]` had a temporary candidate status during external review; its final source, V2 ledger, oral ledger and asset mirror now share the same hash. `10[12]` and `10[16]` are roommate-based to keep the service category while shifting humor to everyday behavior.
