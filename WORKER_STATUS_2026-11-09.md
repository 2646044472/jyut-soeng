# Worker Status — 2026-11-09

## Latest verified checkpoint

- Repository: `2646044472/jyut-soeng`; branch: `codex/macau-story-upgrade-batch-progress-resume`.
- Source rows remain 5,000; active library selection remains exactly 2,000; excluded rows remain 3,000. All source files, IDs, order, categories, metadata and drafts are preserved.
- Oral V2 re-audit: **1,466 pass, 530 pending, 4 needs_revision** among the 2,000 selected cards. At the prior branch HEAD the active oral pass count was 1,416, so this checkpoint adds **50 net manual passes**. V2 historical ledger: 2,296 pass / 2,704 needs_revision across 5,000 source rows; this is not the current 2,000-card oral completion count.
- Selection manifest status counts and nonexclusive topic-note counts were recomputed from exact active IDs and the oral ledger. Story source hashes and app bundle were rebuilt.
- Confirmed local HEAD and `origin/codex/macau-story-upgrade-batch-progress-resume` both at `277ccafc2fc558f82acc90cc62a58ab6787ee333` before checkpoint commit. No release, tag, APK build, or deployment.
- Environment: isolated Temurin JDK 21.0.13+9 and Android command-line tools installed under `/tmp/jyut-soeng-*`; downloads passed official SHA-256 verification. SDK licenses accepted under the user's explicit authorization. No global environment, repository `local.properties`, security permissions, or drivers changed.
- Verification: `build_assets.py` generated 5,000 bundled entries; `story_quality_progress.py` updated the checklist; `validate_content.py --require-story-upgrade --min-sentences 2000` passed on 5,000 entries; Python unittest discovery ran 7 tests, 6 passed and 1 expected skip because all 5,000 stories have not migrated; `:app:testDebugUnitTest` passed (34 tasks, 1 executed, remaining up to date); `git diff --check` passed. No full 5,000-card semantic re-review is claimed.
- Main agent remained sole repository writer. No subagent wrote to the repository.

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
