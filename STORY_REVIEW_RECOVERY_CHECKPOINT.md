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
