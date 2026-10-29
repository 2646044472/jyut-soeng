# jyut-soeng V2 review recovery checkpoint

## Workspace

- Remote branch last successfully confirmed before proxy loss: `origin/codex/macau-story-upgrade-batch-progress` at `661226fab3c703078bc7f6075df04358a46b9cf9`.
- Clean worktree: `C:\Users\bankey\Documents\Codex\2026-10-29\task\jyut-soeng-v2-worktree`, branch `codex/macau-story-upgrade-batch-progress-resume`.
- The Desktop worktree `C:\Users\bankey\Desktop\code\apps\apps\jyut-soeng-worktrees\jyut-soeng-story-current` remains untouched; it had 415 untracked files and two modified app files.

## V2 progress

- Baseline was 1,612 pass / 3,388 needs_revision / 0 pending.
- Two local batches have reviewed ten non-family-core cards. Current V2 ledger: 1,622 pass / 3,378 needs_revision / 0 pending.
- Batch 1, local commit `0a435f2`: `long_food_shopping_01.json` zero-based indexes 9, 31, 48, 74, 76.
- Batch 2, committed at the current HEAD: same file, zero-based indexes 32, 34, 52, 61, 78. All received new distinct public/workplace stories, contextual Jyutping, Simplified Chinese glosses, and `故事练习：` tips. Categories and ordering remain unchanged. No family-core stories were rewritten.
- App bundle was rebuilt from canonical source. The full build corrected an existing mirror drift affecting 102 entries; keeping only the five newly revised entries caused 97 existing source-to-bundle assertion failures. Full generated bundle passes tests; this batch directly changed five source rows and their exact app mirrors.

## Verification

- `python tools/validate_content.py`: passed, 8,000 entries.
- `python -m unittest discover -s tools/tests -p 'test*.py'`: 7 tests ran, 1 skipped, OK.
- `git diff --check`: clean.
- Five revised source rows’ V2 hashes, app `displayText`, `answerJyutping`, `gloss`, `usageTip`, blank `exampleSentence`, `entryType=sentence`, and `qualityPriority=1` were checked against the generated bundle.
- `--min-sentences 15053` previously failed because the validator counts 5,000 curated daily sentence entries; do not change the threshold without a grounded repository requirement.

## Continue from here

- Continue the V2 semantic review from the next eligible non-family-core `needs_revision` card after `long_food_shopping_01.json` index 78. Screen category fit and semantic duplication before editing; skip family-core cards and category conflicts.
- There are two local commits beyond the remote base; neither is pushed. A new screenshot showed Hiddify as connected, but this execution environment still cannot connect to `127.0.0.1:12338`; `Test-NetConnection` and one `git ls-remote` attempt failed. Do not alter proxy/network settings or retry GitHub until the local proxy is confirmed reachable.
- Four cloud-task uncommitted edits remain unverified and were not transferred: three source Jyutping edits and three app mirror Jyutping fields. Do not overwrite them or refresh their hashes alone.

## Pause checkpoint — 2026-10-29

- Historical pause state; superseded by the active resumption update below.
- Current V2 ledger count remains 1,622 pass / 3,378 needs_revision / 0 pending. The five draft edits in `content/sentence_bank/long_food_shopping_02.json` at zero-based indexes 15, 21, 24, 32, 35 are unfinished and are NOT counted as reviewed/pass. The source file is modified in the worktree; retain it as-is for resumption. Jyutping alignment still needs manual correction (including unresolved `???` tokens in index 24); no app mirror, ledger hash, validation, checkpoint batch completion, or commit was made for this draft batch.
- Last confirmed committed local HEAD is `75af26fdcf6268b61dc3066d891fcafc088e1a40`, following local commit `0a435f2876aab9e5afacdf2a06a23dba944cd89e`; both remain unpushed.
- Resume from those five unfinished rows first, completing manual Jyutping review, semantic review, app mirror and validation before any ledger pass update. Then continue non-family-core cards only.
- Desktop worktree remains untouched. The proxy's `127.0.0.1:12338` port was last checked and was unreachable in this execution environment. Do not retry or change proxy/network settings while paused.


## Active resumption update — 2026-10-29

- GitHub access was rechecked from this Windows execution environment through Hiddify `127.0.0.1:12334`: GitHub API returned HTTP 200, and `git ls-remote` confirmed `origin/codex/macau-story-upgrade-batch-progress` at `661226fab3c703078bc7f6075df04358a46b9cf9`. No proxy or DNS settings were changed.
- Resumed the five unfinished drafts in `content/sentence_bank/long_food_shopping_02.json` at indexes 15, 21, 24, 32, and 35. All five indexes 15, 21, 24, 32, and 35 now pass human V2 review after story, contextual Jyutping, Mandarin gloss, and practice-tip review. Index 21’s duplicate navigation plot was replaced with a distinct office meeting speakerphone misunderstanding; all 253 Jyutping syllables were manually aligned and checked.
- The resumed review was committed locally as `e64e7a4810c2fcc89ef95aa94450c0a81087f621` (`Review four Cantonese story cards`) and pushed by fast-forward to the authorized remote branch. A post-push `git ls-remote` confirmed that exact remote SHA; the branch had 0 ahead / 0 behind at verification time.
- Current V2 ledger: 1,632 pass / 3,368 needs_revision / 0 pending. All five source rows have current ledger hashes; all five app mirrors are `qualityPriority=1`. IDs, order, and categories were preserved.
- `python tools/build_assets.py`, `python tools/validate_content.py` (8,000 entries), `python -m unittest discover -s tools/tests -p 'test*.py'` (7 run, 1 skipped), and `git diff --check` passed. `STORY_QUALITY_CHECKLIST.md` was regenerated to match the ledger.
- Desktop worktree remains untouched. The four unrelated cloud-task uncommitted edits remain unverified and were not transferred.
- - Second batch completed five additional cards in `content/sentence_bank/long_food_shopping_02.json`: indexes 45, 64, 68, 72, and 74. Their Jyutping lines were manually checked at 259, 235, 261, 249, and 251 syllables respectively; all source-to-app mirrors match and all five have current V2 pass hashes. Character n-gram comparisons against approved stories showed no close duplicate (top scores were below 0.02).
- Deferred but not passed during category/duplication screening: index 36 (wheelchair restaurant booking overlaps approved index 38), index 37 (birthday cake restaurant reservation overlaps index 32), index 43 (the child-parent spill incident may be family-interaction core), and index 59 (thermos leak/return resembles approved lunchbox leak story at index 62). Keep these needs_revision and revisit for distinct permitted plots; none are counted as pass.
- New V2 total: 1,632 pass / 3,368 needs_revision / 0 pending. `python tools/build_assets.py`, content validation (8,000), unit tests (7 run, 1 skipped), and `git diff --check` passed for the second batch.
- The last reviewed commit `c0586f49c338cb218cac3cb53e712467adecab87` was pushed and verified on the target branch; the worktree was clean at that point.
- Next action: continue after index 74, screen for non-family-core and semantic uniqueness, and later revisit the deferred rows above rather than treating them as completed.


## Active continuation — 2026-10-29, shopping stories batch 3

- Working tree: `C:\Users\bankey\Documents\Codex\2026-10-29\task\jyut-soeng-v2-worktree`, branch `codex/macau-story-upgrade-batch-progress-resume`. The desktop worktree remains untouched.
- The remote target branch `origin/codex/macau-story-upgrade-batch-progress` was read successfully at `2de9add8e0d24a1f4d0e4a67989fdac980009cff` before this batch; the local starting HEAD matched.
- Completed V2 review for `content/sentence_bank/long_food_shopping_02.json` zero-based indexes 84, 86, and 98. Rewrote the stories, reviewed all four language fields, manually checked contextual Jyutping readings against 250, 251, and 257 Han characters, and preserved array order/category.
- Index 84 is now a freezer-label and breakfast-draw story, screened against the approved lunchbox leak story. Index 86 is an oatmeal-package return with an earned shelf-inspector gag. Index 98 is a coworker roast-chicken split that escalates into a mock meeting and written minutes.
- Indexes 85 and 89 remain `needs_revision` after screening for family-interaction focus. Earlier deferred indexes 36, 37, 43, and 59 also remain `needs_revision`.
- Updated V2 hashes and notes for the three approved rows, rebuilt `app/src/main/assets/builtin/content.json`, and verified exact sentence, Jyutping, gloss, and usage-tip mirrors with `qualityPriority=1`.
- Validation passed: `python tools/validate_content.py` (8,000 entries), unit tests (7 run, 1 skipped), `python tools/story_quality_progress.py` (1,635 pass / 3,365 needs_revision / 0 pending), and `git diff --check`. Mechanical checks passed for all 5,000 scoped stories; human V2 review remains incomplete.
- Batch commit: `cf088bf1068bdcdc5c035dbccef7ae16408bf39b` (`Review three Cantonese food stories`). The authorized ordinary push succeeded by fast-forward, and a post-push `git ls-remote` confirmed `origin/codex/macau-story-upgrade-batch-progress` at the same SHA. Local `HEAD` matched the remote target at verification time.


## Active continuation — 2026-10-29, food stories batch 4

- Independent worktree: `C:\Users\bankey\Documents\Codex\2026-10-29\task\jyut-soeng-v2-worktree`; desktop repository remains untouched.
- Before this batch, local and remote target branch were both `30a205e9ff82eff7a3607017395d0e6222ec7383`. The remote target ref was read with `git ls-remote` immediately before preparing this batch.
- Rewrote and completed V2 review for `content/sentence_bank/long_food_shopping_03.json` zero-based indexes 24, 29, 37, 39, 42, and 89. These are rooftop tomato “dessert stall” escalation; a party fruit platter mistaken for a traffic roundabout; the 新居順利/新居順路 wordplay; a farewell cake’s corrected-name plaque, dead phone, and mock name certificate; a mislabeled lunch delivery turned into a fruit meeting; and a used rice cooker purchase whose measuring cup becomes a “test prop.” No family-core story was rewritten.
- Reviewed Cantonese text, simplified gloss, practice prompt, contextual Jyutping, and category fit. Adjusted the orange phrasing at index 29 and made the buyer explicit at index 89. Han/Jyutping counts: 266/266, 241/241, 244/244, 266/266, 297/297, and 271/271. Trigram Jaccard comparisons with current V2-approved stories had maxima from 0.008 to 0.017; used only as a duplicate screen alongside plot review.
- Updated all six V2 decisions and current row hashes, rebuilt `app/src/main/assets/builtin/content.json`, and checked each exact sentence, Jyutping, gloss, usage tip, `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1` mirror.
- `python tools/validate_content.py` passed (8,000 entries), `python tools/story_quality_progress.py --output STORY_QUALITY_CHECKLIST.md` completed, and `git diff --check` passed. Current clarified V2 count is 1,641 pass / 3,359 needs_revision / 0 pending. No unit tests were run in this batch.
- This batch is prepared on top of `30a205e`; commit, ordinary fast-forward push, and post-push remote SHA verification are the remaining actions for this checkpoint.
- Continue with eligible non-family-core cards in `long_food_shopping_03.json` after index 89. Do not count any card unless its language and comedy review is complete and source, ledger, and app mirror are synchronized.
