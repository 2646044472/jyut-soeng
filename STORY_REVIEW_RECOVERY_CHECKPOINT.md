# jyut-soeng V2 review recovery checkpoint

- Remote base verified: `origin/codex/macau-story-upgrade-batch-progress` at `661226fab3c703078bc7f6075df04358a46b9cf9`.
- Working copy: `C:\Users\bankey\Documents\Codex\2026-10-29\task\jyut-soeng-v2-worktree`; branch `codex/macau-story-upgrade-batch-progress-resume`.
- Preserve the pre-existing Desktop worktree at `C:\Users\bankey\Desktop\code\apps\apps\jyut-soeng-worktrees\jyut-soeng-story-current`: it had 415 untracked files and two modified app files and was not changed.
- V2 ledger started at 1,612 pass / 3,388 needs_revision / 0 pending. This batch reviewed and revised five non-family-centered cards in `content/sentence_bank/long_food_shopping_01.json` (0-based indexes 9, 31, 48, 74, 76; IDs end `0010`, `0032`, `0049`, `0075`, `0077`). Current V2 count: 1,617 pass / 3,383 needs_revision / 0 pending.
- All five cards received new distinct Cantonese stories, contextual Jyutping, Simplified Chinese glosses, and `故事练习：` usage tips. The app mirror was synced only for these five rows. No family-centered stories were edited.
- Next work: continue reviewing V2 `needs_revision` records, starting with eligible non-family-centered candidates after index 9 in `long_food_shopping_01.json`; screen category fit before editing and skip category conflicts. Family-core stories are out of scope under the user's latest instruction.
- Validation completed for this batch: default `python tools/validate_content.py` passed (8,000 entries); 7 unit tests ran, 1 skipped, OK; V2 progress report generated; `git diff --check` clean. `--min-sentences 15053` fails because the validator counts 5,000 curated daily sentence entries, so do not change its threshold without a grounded repo requirement.
- Cloud worktree's four uncommitted edits (three Jyutping source changes plus three app mirror Jyutping changes) were not assumed transferred and remain unverified; do not overwrite or merely refresh their hashes. They are separate follow-up checks.
- No commit or push recorded at checkpoint creation.
