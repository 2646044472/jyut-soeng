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
- Content and metadata were committed locally as `fd243a7fbc3b74e0bf3f50f5b03fbb901d60a8f9` (`Review six Cantonese food stories`), pushed by ordinary fast-forward from `30a205e`, and then verified with `git ls-remote` at that exact SHA. Local `HEAD` matched the remote target at verification time.
- Continue with eligible non-family-core cards in `long_food_shopping_03.json` after index 89. Do not count any card unless its language and comedy review is complete and source, ledger, and app mirror are synchronized.


## Active continuation — 2026-10-29, shopping batch 5

- Independent worktree: `C:\Users\bankey\Documents\Codex\2026-10-29\task\jyut-soeng-v2-worktree`; desktop repository remains untouched.
- Before this batch, local and remote target branch were both `6149100d765939152f3f2af24242a4c27ed1739f`; the remote target ref was checked immediately before preparing the batch.
- Completed V2 review for `content/sentence_bank/long_food_shopping_04.json` zero-based index 11. Reworked the misplaced yoghurt promotion sign into a price-tag investigation that escalates when coworkers send more shelf-tag photos and appoint the narrator a mock “supermarket price-tag inspector.” This workplace-shopping plot differs from approved transaction and bill-sharing stories.
- Reviewed Cantonese, contextual Jyutping, Simplified Chinese gloss, and `故事练习：` prompt. Corrected contextual readings including 乳酪 `jyu5 lok6`, 只限 `zi2 haan6`, 埋單 `maai4 daan1`, 十分鐘 `sap6 fan1 zung1`, and 轉行 `zyun2 hang4`; all 268 Han characters align with 268 Jyutping syllables.
- Current approved-story trigram Jaccard maximum was 0.0144. Updated the V2 status/hash, rebuilt the app bundle, and verified exact source-to-app text, Jyutping, gloss, usage tip, `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), progress report regenerated, and `git diff --check` passed. V2 total: 1,642 pass / 3,358 needs_revision / 0 pending. Unit tests were not run in this batch.
- Batch commit `ca0908c66726c8526f8dd1a652460025d9337146` (`Review Cantonese supermarket promotion story`) was pushed by ordinary fast-forward from `6149100`. Post-push `git ls-remote` confirmed the target branch at exactly `ca0908c66726c8526f8dd1a652460025d9337146`; local `HEAD` matched at verification time.
- Continue with distinct, non-family-core stories. Index 90 in this file is a used-toaster trial plot and is too close to approved index 89’s used-rice-cooker trial; leave it `needs_revision`. Avoid family-interaction-core cards.


## Active continuation — 2026-10-30, delivery batch 6

- Independent worktree: `C:\Users\bankey\Documents\Codex\2026-10-29\task\jyut-soeng-v2-worktree`; the Desktop repository remains untouched.
- Before this batch, local and remote target branch were both `1caf5a70eb96a69d47d1e2a8b3fef14923e45db3`; the remote target ref was checked before editing.
- A draft rewrite of `long_food_shopping_05.json` index 2 introduced a delivery navigation loop, but it overlaps the approved wrong-address delivery plot in `long_food_shopping_09.json` index 96. I restored index 2 to its original source row and kept it `needs_revision`.
- Completed V2 review for `content/sentence_bank/long_food_shopping_05.json` zero-based index 94 instead. The revised story turns bottles rolling in a rain-softened delivery carton into repeated door-knocking; a neighbor joins the handoff, asks whether the water has gone to sleep when it stops knocking, and the narrator leaves a sign for the next delivery. This is distinct from the nearest approved plots after inspecting the top trigram matches.
- Reviewed Cantonese, contextual Jyutping, complete Simplified Chinese gloss, and `故事练习：` prompt. Han/Jyutping alignment is 270/270. Highest approved-story trigram Jaccard was 0.0128. Updated the current V2 hash/status, rebuilt the app bundle, and verified exact source text, Jyutping, gloss, practice tip, `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), progress report regenerated, and `git diff --check` passed. V2 total is 1,643 pass / 3,357 needs_revision / 0 pending. Unit tests were not run in this batch.
- Batch commit `64d3b17c0ca6fd306e83dd5ed0f1045af10ad2e7` (`Review Cantonese water delivery story`) was pushed by ordinary fast-forward from `1caf5a7`. Post-push `git ls-remote` confirmed the target branch at exactly `64d3b17c0ca6fd306e83dd5ed0f1045af10ad2e7`; local `HEAD` matched at verification time.
- Continue with distinct non-family-core stories; do not pass the reverted index 2 unless its delivery plot is made distinct from the approved wrong-address story.


## Active continuation — 2026-10-30, market batch 7

- Independent worktree: `C:\Users\bankey\Documents\Codex\2026-10-29\task\jyut-soeng-v2-worktree`; Desktop repository remains untouched.
- Before this batch, local and remote target branch were both `a016cdf207d6da178f078cd6503a996cb4c96cad`; the remote target ref was checked before commit.
- Completed V2 review for `content/sentence_bank/long_food_shopping_06.json` zero-based index 85. The roommate’s “winter melon installments” joke now runs through the vendor weighing and labeling the two portions, separate meals, a “final installment paid” shopping-list note, and the callback that a watermelon could be bought in four installments.
- Reviewed Cantonese, contextual Jyutping, complete Simplified Chinese gloss, and `故事练习：` prompt. Han/Jyutping alignment is 226/226. Highest trigram Jaccard against previously approved stories was 0.0132; the nearest lexical match is unrelated.
- Updated the V2 hash/status, rebuilt the app bundle, and verified exact source text, Jyutping, gloss, usage tip, `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), progress report regenerated, and `git diff --check` passed. Current V2 total: 1,644 pass / 3,356 needs_revision / 0 pending. Unit tests were not run in this batch.
- Batch commit `661ada89137c955afc80ac5aef7d4d1826ac68cd` (`Review Cantonese winter melon story`) was pushed by ordinary fast-forward from `a016cdf`. Post-push `git ls-remote` confirmed the target branch at exactly `661ada89137c955afc80ac5aef7d4d1826ac68cd`; local `HEAD` matched at verification time.
- Continue screening for distinct, non-family-core stories.

## Active continuation — 2026-10-30, market batch 8

- Continued in the independent worktree `C:\Users\bankey\Documents\Codex\2026-10-29\task\jyut-soeng-v2-worktree`; the Desktop repository remains untouched. Local HEAD started at `ce6c0571ccf09db7d6c05e10958d2ff88f32be8e`.
- Completed V2 review for `content/sentence_bank/long_food_shopping_07.json` zero-based index 90. A curry puff’s flaky crumbs become a rising “performance curve” during a quarterly meeting; the manager adds a tasting budget and schedules a blind test; at the next meeting coworkers arrive with a ruler to measure the crumbs, and the manager asks which curry puff will draw the chart.
- Checked Cantonese, contextual Jyutping, complete Simplified Chinese gloss, practice prompt, and category fit. Corrected 枱 to `toi2`. Han/Jyutping alignment is 229/229. The top trigram Jaccard match against V2-approved stories was 0.0152 and involved an unrelated snack-packing plot.
- Updated the V2 status/hash and rebuilt the app bundle. Source sentence, Jyutping, gloss, usage tip, blank `exampleSentence`, `entryType=sentence`, and `qualityPriority=1` were checked in the corresponding bundle entry.
- `python tools/validate_content.py` passed (8,000 entries), `python tools/story_quality_progress.py --output STORY_QUALITY_CHECKLIST.md` completed, and `git diff --check` passed. Current V2 count: 1,645 pass / 3,355 needs_revision / 0 pending. Unit tests were not run.
- The GitHub connector listed `codex/macau-story-upgrade-batch-progress` at `ce6c0571ccf09db7d6c05e10958d2ff88f32be8e`; local branch name `codex/macau-story-upgrade-batch-progress-resume` is not a remote branch. The ordinary fast-forward push succeeded, and `git ls-remote` confirmed the target ref at `c8e921a4d9aeafb4f21a6e665301d2d3506ebe28`.
- Continue reviewing distinct non-family-core cards across the full 5,000-card scope.


## Active continuation — 2026-10-30, market batch 9

- Continued in the same independent worktree; before this batch the verified remote target was `c8e921a4d9aeafb4f21a6e665301d2d3506ebe28`.
- Completed V2 review for `content/sentence_bank/long_food_shopping_07.json` zero-based index 96. A loose frozen pea rolls from a punctured bag to the freezer door, leading the nephew and staff to discover the door ajar; the nephew calls it a runaway who led them to the fault, asks whether it should pay separately at checkout, and records that it rejoined its team on the shopping list.
- Grocery shopping remains central and is category-aligned. Reviewed Cantonese, contextual Jyutping, full Simplified Chinese gloss, and practice tip. Han/Jyutping alignment is 255/255. Highest approved-story trigram Jaccard was 0.0185; the closest match concerns frozen seafood being unavailable and has a different plot.
- Updated the V2 status/hash, rebuilt the app bundle, and verified exact sentence, Jyutping, gloss, usage tip, blank `exampleSentence`, `entryType=sentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), progress report regeneration completed, and `git diff --check` passed. Current V2 count: 1,646 pass / 3,354 needs_revision / 0 pending. Unit tests were not run.
- Continue reviewing distinct non-family-core cards across the full 5,000-card scope.


## Active continuation — 2026-10-30, takeaway batch 10

- Continued in the independent worktree; before this batch the remote target was verified at `70704d13497f1450cdcd03c7059f701c7b15ea5a`.
- Completed V2 review for `content/sentence_bank/long_food_shopping_08.json` zero-based index 2. In a workplace takeaway scene, a coworker nearly pours a separated chili-oil packet into a shared clear soup; colleagues mark a tiny “ask first” restricted zone, and the next day the coworker labels his packet and gets a mock safety-pass joke.
- Category remains takeaway communication and the workplace exchange is central. Reviewed Cantonese, contextual Jyutping, full Simplified Chinese gloss, and practice tip. Han/Jyutping alignment is 240/240. Highest approved-story trigram Jaccard was 0.0126; the nearest lexical match was an unrelated anonymous Q&A scene.
- Updated V2 status/hash, rebuilt the app bundle, and verified the exact sentence, Jyutping, gloss, usage tip, blank `exampleSentence`, `entryType=sentence`, and `qualityPriority=1` mirror.
- `python tools/validate_content.py` passed (8,000 entries), progress report regeneration completed, and `git diff --check` passed. Current V2 count: 1,647 pass / 3,353 needs_revision / 0 pending. Unit tests were not run.
- Batch commit `4f8c4e6cf55070d9d871496dbc79d9c8a10c8ccc` (`Review Cantonese takeaway communication story`) was pushed by ordinary fast-forward from `70704d1`; `git ls-remote` confirmed the target ref at the same SHA.
- Continue reviewing distinct non-family-core cards across the full 5,000-card scope.


## Active continuation — 2026-10-30, office drink batch 11

- Continued in the independent worktree; before this batch the remote target was verified at `73f207a44ea9984104b00d1a1f58d0dea1620a9d`.
- Completed V2 review for `content/sentence_bank/long_food_shopping_08.json` zero-based index 50. A new coworker drinks the wrong no-sugar milk tea and explains that he “drank no sugar,” not “heard no sugar” in the meeting conclusion; the callback makes the manager ask to remove “meeting conclusion: half-sugar” from the minutes.
- Company drink ordering remains central. Reviewed Cantonese, contextual Jyutping, full Simplified Chinese gloss, and practice tip. Han/Jyutping alignment is 228/228. Highest approved-story trigram Jaccard was 0.0112.
- Updated V2 status/hash, rebuilt the app bundle, and verified exact sentence, Jyutping, gloss, usage tip, blank `exampleSentence`, `entryType=sentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), progress report regeneration completed, and `git diff --check` passed. Current V2 count: 1,648 pass / 3,352 needs_revision / 0 pending. Unit tests were not run.
- Batch commit `e6c37df520a16e672beeb1602bb88449e525b893` (`Review Cantonese company drink order story`) was pushed by ordinary fast-forward from `73f207a`; `git ls-remote` confirmed the target ref at the same SHA.
- Continue reviewing distinct non-family-core cards across the full 5,000-card scope.


## Active continuation — 2026-10-30, delayed tea batch 12

- Continued in the independent worktree; before this batch the remote target was verified at `e6c37df520a16e672beeb1602bb88449e525b893`.
- Completed V2 review for `content/sentence_bank/long_food_shopping_08.json` zero-based index 61. After coworkers brew tea and finish their meeting, the delayed delivery arrives at adjournment; Ah Mei calls it “散會茶” and says next time she will ask when the meeting ends.
- Workplace takeaway communication remains central. Reviewed Cantonese (including changing the Mandarin-influenced 看 to 睇), contextual Jyutping, full Simplified Chinese gloss, and practice tip. Han/Jyutping alignment is 243/243. Highest approved-story trigram Jaccard was 0.0166; nearest lexical match is a distinct breakfast-order story.
- Updated V2 status/hash, rebuilt the app bundle, and verified exact sentence, Jyutping, gloss, usage tip, blank `exampleSentence`, `entryType=sentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), progress report regeneration completed, and `git diff --check` passed. Current V2 count: 1,649 pass / 3,351 needs_revision / 0 pending. Unit tests were not run.
- Batch commit `a45c2c4e5dee85675ec3cfc46ce9a9e48bae137e` (`Review Cantonese delayed tea delivery story`) was pushed by ordinary fast-forward from `e6c37df`; `git ls-remote` confirmed the target ref at the same SHA.
- Continue reviewing distinct non-family-core cards across the full 5,000-card scope.


## Active continuation — 2026-10-30, syrup order batch 13

- Continued in the independent worktree; before this batch the remote target was verified at `7efb820d1f7187b0742ec9021f71a2d170dac7c3`.
- Completed V2 review for `content/sentence_bank/long_food_shopping_08.json` zero-based index 10. A wrongly syruped coffee is remade and marked “糖漿暫離”; the coworker treats the label literally, saves the syrup a seat, and asks if it has officially resigned.
- Takeaway drink ordering remains central. Reviewed Cantonese, contextual Jyutping, full Simplified Chinese gloss, and practice tip. Han/Jyutping alignment is 251/251. Highest approved-story trigram Jaccard was 0.0147.
- Updated V2 status/hash, rebuilt the app bundle, and verified exact sentence, Jyutping, gloss, usage tip, blank `exampleSentence`, `entryType=sentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), progress report regeneration completed, and `git diff --check` passed. Current V2 count: 1,650 pass / 3,350 needs_revision / 0 pending. Unit tests were not run.
- Batch commit `19fb9a36153e2368f61232b11f36b0dd9841a41f` (`Review Cantonese syrup order story`) was pushed by ordinary fast-forward from `7efb820`; `git ls-remote` confirmed the target ref at the same SHA.
- Continue reviewing distinct non-family-core cards across the full 5,000-card scope.


## Active continuation — 2026-10-30, switched delivery batch 14

- Continued in the independent worktree; before this batch the remote target was verified at `3c85c22b40811ff408f6cca8947b691ac56172b4`.
- Completed V2 review for `content/sentence_bank/long_food_shopping_08.json` zero-based index 85. Two recipients verify the swapped beef orders before exchanging them; the guard draws a seat-number route on the lobby board and appoints himself the next delivery treasure-hunt host.
- Online food delivery remains central. Reviewed Cantonese, contextual Jyutping, full Simplified Chinese gloss, and practice tip. Han/Jyutping alignment is 263/263. Highest approved-story trigram Jaccard was 0.0183.
- Updated V2 status/hash, rebuilt the app bundle, and verified exact sentence, Jyutping, gloss, usage tip, blank `exampleSentence`, `entryType=sentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), progress report regeneration completed, and `git diff --check` passed. Current V2 count: 1,651 pass / 3,349 needs_revision / 0 pending. Unit tests were not run.
- Batch commit `350d9f8a6be39d0e424f366ffb08fa383654b4e0` (`Review Cantonese switched beef delivery story`) was pushed by ordinary fast-forward from `3c85c22`; `git ls-remote` confirmed the target ref at the same SHA.
- Continue reviewing distinct non-family-core cards across the full 5,000-card scope.


## Active continuation — 2026-10-30, secondhand deduplication check

- Continued in the independent worktree; the remote target before this review was `0e6f288edb0f857b25568b853d47477ad824c78a`.
- Rejected the proposed comedy rewrite for `content/sentence_bank/long_food_shopping_09.json` zero-based index 8 after comparing it with the approved secondhand toaster trial in `long_food_shopping_03.json` index 90. The item and plot were duplicates despite a different final joke, so the original row was restored and remains `needs_revision`; the V2 pass count did not increase.
- Updated the row hash/notes, rebuilt the app bundle from canonical content, and verified `python tools/validate_content.py` (8,000 entries), progress report regeneration, and `git diff --check`. The source row remains correctly aligned with its Jyutping.
- Current V2 count remains 1,651 pass / 3,349 needs_revision / 0 pending. Unit tests were not run.
- Correction commit `df5587f9b6f08ea0b89987305b2bcc95fc6dfac1` (`Reject duplicate secondhand toaster story`) was pushed by ordinary fast-forward from `0e6f288`; `git ls-remote` confirmed the target ref at the same SHA.
- Continue screening distinct non-family-core stories; require plot-level uniqueness, not just a changed punchline.

## Active continuation — 2026-10-30, basil storage batch 15

- Continued in the independent worktree; before this batch, local and remote target refs matched at `6e46cfaf85242210794fa5b38f1a0fa117f7e15f`.
- Replaced `content/sentence_bank/long_food_shopping_09.json` zero-based index 16 with a distinct workplace basil-preservation story. A coworker mistakes the basil water cup for dishes, starts the dishwasher, then treats the basil as a rotating intern and adds it to the duty roster; the closing joke leaves the cup on night duty. The food-preservation category remains central.
- Reviewed Macau Cantonese, contextual Jyutping (226 Han characters / 226 syllables), Simplified Chinese gloss, and practice tip. Plot-level trigram screening against approved cards had a maximum Jaccard score of 0.0169.
- Updated the V2 hash and status, rebuilt the app bundle, verified exact source-to-app mirrors and `qualityPriority=1`, regenerated the checklist, and passed `python tools/validate_content.py` (8,000 entries) and `git diff --check`.
- Current V2 total: 1,652 pass / 3,348 needs_revision / 0 pending. Unit tests were not run.
- Content commit `9b081f0ea1e645f3ab00bda404df7ee6db3078bc` (`Review Cantonese basil storage story`) was pushed by ordinary fast-forward. GitHub connector and `git ls-remote` both confirmed the target branch at that SHA.
- Continue reviewing distinct non-family-core stories across the full 5,000-card scope.

## Active continuation — 2026-10-30, honey selection batch 16

- Continued in the independent worktree; before this batch, local and remote target refs matched at `8537cb3ce71a295a201164d7364eb23c7acfe8e0`.
- Replaced `content/sentence_bank/long_food_shopping_09.json` zero-based index 75 with a distinct supermarket honey-selection story for a workplace baking group. A crystallized jar is mistaken for spoiled, the label is checked, a neighboring shopper imitates a phone-light inspection as barcode scanning, and the jar gets a “snow-scene honey” note before baking confirms it is fine. The shopping and product-selection category remains central.
- Reviewed Macau Cantonese, contextual Jyutping (229 Han characters / 229 syllables), Simplified Chinese gloss, and practice tip. The closest approved-story trigram Jaccard score was 0.0186; the approved honey bulk-order story concerns leaky jar seals and has a different plot.
- Updated the V2 hash/status, rebuilt the app bundle, verified exact source-to-app mirrors and `qualityPriority=1`, regenerated the checklist, and passed `python tools/validate_content.py` (8,000 entries) and `git diff --check`.
- Current V2 total: 1,653 pass / 3,347 needs_revision / 0 pending. Unit tests were not run.
- Content commit `3b55886` (`Review Cantonese crystallized honey story`) was pushed by ordinary fast-forward. The follow-on checkpoint commit `c6e54ca43524439fdd03d69bac44b74dd710a001` was also pushed and confirmed with `git ls-remote`.
- Continue reviewing distinct non-family-core stories across the full 5,000-card scope.

## Active continuation — 2026-10-30, king oyster mushroom batch 17

- Continued in the independent worktree; before this batch, local and remote target refs matched at `338ee264be87ec524d919592fa77a1aeddcfa3c7`.
- Replaced `content/sentence_bank/long_food_shopping_09.json` zero-based index 76 with a cooking-class group shopping for king oyster mushrooms. One classmate interprets “chicken-leg mushroom” literally, separates chicken from mushrooms in the basket, and writes a label that makes another group ask where the meat is. Mushroom selection and cooking-class shopping remain central; the story avoids family-interaction focus.
- Reviewed Macau Cantonese and revised written phrasing for natural spoken Cantonese; contextual Jyutping aligns at 237 Han characters / 237 syllables. Simplified Chinese gloss and practice tip were checked. The nearest lexical trigram match was an unrelated coworker farewell cake story (Jaccard 0.0200).
- Updated the V2 status/hash, rebuilt the app bundle, verified exact source-to-app mirrors and `qualityPriority=1`, regenerated the checklist, and passed `python tools/validate_content.py` (8,000 entries) and `git diff --check`.
- Current V2 total: 1,654 pass / 3,346 needs_revision / 0 pending. Unit tests were not run.
- Content commit `d2f82db` (`Review Cantonese king oyster mushroom story`) was pushed by ordinary fast-forward. The checkpoint update follows this content commit.
- Continue reviewing distinct non-family-core stories across the full 5,000-card scope.

## Active continuation — 2026-10-30, egg-roll gift batch 18

- Continued in the independent worktree; before this batch, local and remote target refs matched at `88a81da416bdafd69d800b0c8c3b235e3b181a21`.
- Replaced `content/sentence_bank/long_food_shopping_09.json` zero-based index 86 with a supermarket souvenir-purchase story. Coworkers choose egg rolls for a two-bus trip, compare flavors and dates, switch a short-dated tin, and keep the gift dry in heavy rain. The recipient mistakes the tin for a stationery box; after sharing the egg rolls, it becomes a pen holder, paying off the weight joke. The story uses a different character from the preceding honey card and has a distinct travel/packaging plot.
- Reviewed Macau Cantonese, contextual Jyutping (265 Han characters / 265 syllables), Simplified Chinese gloss, and practice tip. Updated the source hash/status and exact app mirror with `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), the checklist was regenerated, and `git diff --check` passed. Unit tests were not run.
- Current V2 total: 1,655 pass / 3,345 needs_revision / 0 pending.
- Content commit `020e04b` (`Review Cantonese egg roll gift story`) was pushed by ordinary fast-forward. The checkpoint update follows this content commit.
- Continue reviewing distinct non-family-core stories across the full 5,000-card scope.

## Active continuation — 2026-10-30, avocado ripening batch 19

- Continued in the independent worktree; before this batch, local and remote target refs matched at `0b0753e7ab60b2520eb5d9342c8e4c1d7849fdd0`.
- Replaced `content/sentence_bank/long_food_shopping_10.json` zero-based index 6 with a workplace avocado-selection story. One avocado ripens in a paper bag beside bananas while another stays on the desk; a coworker records their firmness as a playful weather report, with a manager callback at the end. Fresh produce selection and ripening remain central; no approved avocado-specific plot was found.
- Reviewed Macau Cantonese, contextual Jyutping (246 Han characters / 246 syllables), Simplified Chinese gloss, and practice tip. The nearest lexical trigram match was an unrelated sourdough office lunch story (Jaccard 0.0173).
- Updated V2 status/hash, rebuilt the app bundle, verified exact source-to-app mirrors and `qualityPriority=1`, regenerated the checklist, and passed `python tools/validate_content.py` (8,000 entries) and `git diff --check`.
- Current V2 total: 1,656 pass / 3,344 needs_revision / 0 pending. Unit tests were not run.
- Content commit `3d8685d` (`Review Cantonese avocado ripening story`) was pushed by ordinary fast-forward. The checkpoint update follows this content commit.
- Continue reviewing distinct non-family-core stories across the full 5,000-card scope.

## Active continuation — 2026-10-30, tomato noodle batch 20

- Continued in the independent worktree `C:\Users\bankey\Documents\Codex\2026-10-29\task\jyut-soeng-v2-worktree`; the Desktop worktree remains untouched. Before this batch, local HEAD and the target remote branch were both `c7f23360600939cef4984658b38ca91633bc9d8d`.
- Replaced `content/sentence_bank/long_food_shopping_10.json` zero-based index 3 with a distinct shared-apartment tomato beef noodle story. A neighbor asks to borrow soy sauce, gets soup to taste, and advertises it in the corridor group; the roommate turns the unexpected queue into an improvised condiment-rental service. The cooking category stays central and family interaction is no longer the story core.
- Reviewed Macau Cantonese, all 278 contextual Jyutping syllables against 278 Han characters, complete Simplified Chinese gloss, and practice tip. Screened the core noodle/neighbor premise against approved stories; no matching tomato-beef-noodle or soy-sauce-borrowing plot was found.
- A separate candidate at index 5 remains `needs_revision`: its olive-oil leak and replacement core was too close to an approved olive-oil leak/exchange story in `long_food_shopping_10.json` index 32, even though a proposed office-meeting ending differed.
- Updated V2 status/hash, rebuilt the app bundle, verified exact source-to-app mirrors, blank `exampleSentence`, `entryType=sentence`, and `qualityPriority=1`, then regenerated the checklist. `python tools/validate_content.py` passed (8,000 entries), and `git diff --check` passed. Current V2 total: 1,657 pass / 3,343 needs_revision / 0 pending. Unit tests were not run.
- Content commit: `ef3632e` (`Review Cantonese tomato noodle story`). Recovery checkpoint is being committed separately; continue reviewing eligible distinct cards across the full 5,000-card scope.

## Active continuation — 2026-10-30, market phone batch 21

- Continued in the independent worktree; before this batch, local HEAD and the target remote branch were both `b13d43852fcc52ab90c760fdf773326f67d18537`. The Desktop worktree remains untouched.
- Replaced `content/sentence_bank/long_food_shopping_11.json` zero-based index 0. A market vendor pauses the fish stall’s ice knocking so a coworker’s call can be heard; the phone rings from the shopper’s own bag under the Chinese kale. The vendor pretends to weigh the phone and quotes it free while charging for the kale. Market shopping remains central.
- Reviewed Macau Cantonese, contextual Jyutping (276 Han characters / 276 syllables), complete Simplified Chinese gloss, and practice tip. Screened approved stories for the missing-phone and phone-under-market-bag premise; no matching plot was found.
- Updated V2 status/hash, rebuilt the app bundle, verified exact source-to-app mirrors, blank `exampleSentence`, `entryType=sentence`, and `qualityPriority=1`, and regenerated the checklist. `python tools/validate_content.py` passed (8,000 entries), and `git diff --check` passed. Current V2 total: 1,658 pass / 3,342 needs_revision / 0 pending. Unit tests were not run.
- Content commit: `04bfb21` (`Review Cantonese market phone story`). Recovery checkpoint is being committed separately; continue reviewing distinct cards across the full 5,000-card scope.


## Active continuation — 2026-10-30, milk-bottle skyline batch 22

- Continued in the independent worktree `C:\Users\bankey\Documents\Codex\2026-10-29\task\jyut-soeng-v2-worktree`; the Desktop worktree remains untouched. Before this batch, local HEAD and `origin/codex/macau-story-upgrade-batch-progress` were both `eeb0d2afd8c98d582740a036b231b4bde06960d8`.
- Reworked `content/sentence_bank/long_food_shopping_11.json` zero-based index 2. The squat local-milk bottle now pays off at the school presentation: classmates line the bottles up as Macau's skyline, and the daughter calls the all-low-rise display a milk building. Supermarket dairy remains central; the plot is not a family conflict.
- Reviewed Macau Cantonese, contextual Jyutping (272 Han characters / 272 syllables), complete Simplified Chinese gloss, and matching practice tip. No approved story matched the milk-building/skyline joke; maximum character-trigram Jaccard similarity against other approved stories was 0.0165.
- Updated the V2 status/hash, rebuilt the app bundle, verified exact source-to-app mirrors for sentence, Jyutping, gloss and practice tip, blank `exampleSentence`, `entryType=sentence`, and `qualityPriority=1`. The mechanical story audit reported no failures; `python tools/validate_content.py` passed (8,000 entries), the checklist was regenerated, and `git diff --check` passed. Unit tests were not run.
- Current V2 total: 1,659 pass / 3,341 needs_revision / 0 pending. Commit and remote verification are the remaining steps for this batch.


## Active continuation — 2026-10-30, office potluck birthday batch 23

- Continued in the independent worktree; local HEAD and the target remote were `7a03e38e6778b1da8a888e474c75da9633032332` before this batch. The Desktop worktree remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_13.json` zero-based index 90, an office sushi potluck. The opening now establishes that the meal is for the manager's birthday. After coworkers eat mango pieces from the fruit-letter 快, leaving 生日樂, the manager jokes that the happiness has been eaten. The supermarket run is incidental; the office lunch and food are central.
- Reviewed Macau Cantonese and contextual Jyutping (290 Han characters / 290 syllables), including the changed opening and punchline; checked complete Simplified Chinese gloss and event-specific tip. Similar birthday fruit-card stories in other categories use different family/cake plots; no matching office potluck joke was found. Maximum character-trigram Jaccard against approved stories was 0.0095.
- Updated the V2 hash/status, rebuilt the app bundle, verified exact source-to-app text/Jyutping/gloss/tip, blank `exampleSentence`, `entryType=sentence`, and `qualityPriority=1`. The mechanical audit had no failures; `python tools/validate_content.py` passed (8,000 entries), checklist regenerated, and `git diff --check` passed. Unit tests were not run.
- Current V2 total: 1,660 pass / 3,340 needs_revision / 0 pending. Content commit: `a64146aa74d1ddc081e1a3993b2a91e9d6a0d023`; the checkpoint commit and remote verification remain.


## Active continuation — 2026-10-30, handmade dumpling shop batch 24

- Continued in the independent worktree; local HEAD and the target remote were `121057b56563a6dadfc73910dde891180fa016b2` before this batch. The Desktop worktree remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_13.json` zero-based index 33. A new handmade dumpling shop's lunch offer grows into a night-shift group tasting; the owner sends two uncooked dumplings for a boiled-versus-pan-fried comparison, and the coworkers vote only for two more next time. The food-shop/workplace plot is distinct from approved frozen-dumpling failures and family cooking stories.
- The old V2 note described a radish-cake story, not this source row; replaced it with an accurate summary during revalidation. Checked Macau Cantonese, contextual Jyutping (295 Han characters / 295 syllables), full Simplified Chinese gloss and practice tip. The nearest approved story is an unrelated coworker spice-bravado reversal (maximum character-trigram Jaccard 0.0153).
- Updated the V2 hash/status, rebuilt the app bundle, verified exact source-to-app sentence/Jyutping/gloss/tip, blank `exampleSentence`, `entryType=sentence`, and `qualityPriority=1`. Mechanical audit had no failures; `python tools/validate_content.py` passed (8,000 entries), checklist regenerated, and `git diff --check` passed. Unit tests were not run.
- Current V2 total: 1,661 pass / 3,339 needs_revision / 0 pending. Content commit: `538b05250692e7560fda6110f14479785f5cd661`; the checkpoint commit and remote verification remain.


## Active continuation - 2026-10-30, fish-ball noodle lunch batch 25

- Continued in the independent worktree `C:\Users\bankey\Documents\Codex\2026-10-29\task\jyut-soeng-v2-worktree`; local HEAD and `origin/codex/macau-story-upgrade-batch-progress` were both `266f035c5e64401c19c31d238917c6d6159a4426` before this batch. The Desktop worktree remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_15.json` zero-based index 18. The server hears only the request for "less" and reduces the fish-ball count; a coworker jokes that the fish balls took leave. The server restores them, and a timer joke counts their return to work and the soup cooling. The story now starts at an established shop to separate its setup from the recently reviewed coworker dumpling-shop lunch.
- Checked Macau Cantonese and contextual Jyutping (271 Han characters / 271 syllables), the revised readings, full Simplified Chinese gloss, event-specific practice tip, and event order. Screened approved stories; the closest character-trigram Jaccard similarity was 0.0165 against the distinct handmade dumpling-shop lunch at `long_food_shopping_13.json` index 33.
- Updated the V2 status/hash, rebuilt the app bundle, verified exact source-to-app sentence/Jyutping/gloss/tip/category mirrors, blank `exampleSentence`, `entryType=sentence`, and `qualityPriority=1`. The mechanical story audit had no failures; `python tools/validate_content.py` passed (8,000 entries), the checklist was regenerated, and `git diff --check` passed. Unit tests were not run.
- Current V2 total: 1,662 pass / 3,338 needs_revision / 0 pending. Content commit: `8d8b9a9a74be3b3f1f382be742915f3dfc40c7cf`; recovery-checkpoint commit and remote verification remain.


## Active continuation - 2026-10-30, duplicate-screen continuation batch 26

- Continued in the independent worktree; local HEAD and `origin/codex/macau-story-upgrade-batch-progress` were both `db5d32d9b1729d650593529077fcebd7eb8f6e8e` before this review. The Desktop worktree remains untouched.
- Re-screened `content/sentence_bank/long_food_shopping_15.json` zero-based index 19 and kept it `needs_revision`. Its torn frozen-pea bag, peas rolling under an appliance, escapee-personification and supermarket exchange repeat the approved frozen-pea escape plot at `long_food_shopping_07.json` index 96. The low character-trigram similarity (0.0099) does not change the semantic overlap. Rewrote the V2 note to document the duplicate and the reason not to approve it; source content remains unchanged.
- Regenerated `STORY_QUALITY_CHECKLIST.md`; the revalidation ledger remains synchronized with source hashes. No app rebuild was needed because neither card content nor approval status changed. `git diff --check` passed; unit tests were not run.
- V2 total remains 1,662 pass / 3,338 needs_revision / 0 pending. The ledger-note and recovery-checkpoint commits and remote verification remain.


## Active continuation - 2026-10-30, melon football batch 27

- Continued in the independent worktree; local HEAD and `origin/codex/macau-story-upgrade-batch-progress` were both `effb7b3d37691b1672b3acaacbd79bbdd18f86a5` before this batch. The Desktop worktree remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_16.json` zero-based index 7. A firm melon chosen for bus travel rolls during a sudden stop and is mistaken for a ball; after the grandmother ripens it, the grandson calls the shared melon the best football because the whole team gets a piece. The callback ties fruit selection, careful transport and sharing together.
- Checked Macau Cantonese and contextual Jyutping (263 Han characters / 263 syllables), including the revised final line and tones, complete Simplified Chinese gloss and matching practice tip. Screened approved stories; maximum character-trigram Jaccard was 0.0159, with a different family-outing story as the nearest match.
- Updated V2 status/hash, rebuilt the app bundle, verified exact source-to-app sentence/Jyutping/gloss/tip/category mirrors, blank `exampleSentence`, `entryType=sentence`, and `qualityPriority=1`. The mechanical story audit had no failures; `python tools/validate_content.py` passed (8,000 entries), checklist regenerated, and `git diff --check` passed. Unit tests were not run.
- Current V2 total: 1,663 pass / 3,337 needs_revision / 0 pending. Content commit: `70eaf8bedcae487cedf155f46eab36b4f46efd92`; recovery-checkpoint commit and remote verification remain.


## Active continuation — 2026-10-30, instant-soup overtime batch 28

- Continued in the independent worktree `C:\Users\bankey\Documents\Codex\2026-10-29\task\jyut-soeng-v2-worktree`; the Desktop repository remains untouched. Before this batch, local HEAD and `origin/codex/macau-story-upgrade-batch-progress` were both `c17647f5f07c150476b30d246617695db38bbdbf`.
- Reworked `content/sentence_bank/long_food_shopping_16.json` zero-based index 23. Supermarket instant soup bought for overtime becomes a workplace deadline mix-up: coworkers turn food-use dates and flavors into an assigned project schedule, and the empty drawer earns the final on-time-delivery joke. The supermarket item and overtime use remain central; this is not a family-interaction-core story.
- Reviewed Macau Cantonese, contextual Jyutping (242 Han characters / 242 syllables), the complete Simplified Chinese gloss, and matching practice tip. Screened approved cards for semantic overlap; the nearest character-trigram match was an unrelated office lunch contest (Jaccard 0.0125).
- Updated the V2 status/hash, rebuilt `app/src/main/assets/builtin/content.json`, verified exact sentence/Jyutping/gloss/tip/category mirrors, blank `exampleSentence`, `entryType=sentence`, and `qualityPriority=1`, then regenerated the checklist. `python tools/validate_content.py` passed (8,000 entries), and `git diff --check` passed. Unit tests were not run.
- Current V2 total: 1,664 pass / 3,336 needs_revision / 0 pending. Content commit: `5f3771e06efe92421b782d55f5fc07a4a21ea296`; checkpoint commit: `b1b2127c8132c0740da70ec12c88867b1e43806e`. Both were pushed by ordinary fast-forward. `git ls-remote` confirmed the target branch at `e05288cda300a473c42caf46512a70ff763406f2`, and the GitHub connector fetched that exact commit.
- Continue reviewing distinct eligible stories across the full 5,000-card scope.


## Active continuation — 2026-10-30, office salad duplicate-screen batch 29

- Continued in the independent worktree; before this screening update, local HEAD and the target remote branch were both `e05288cda300a473c42caf46512a70ff763406f2`. The Desktop worktree remains untouched.
- Re-screened `content/sentence_bank/long_food_shopping_17.json` zero-based index 18, the office group-salad order. The closest approved character-trigram match was an unrelated coworker Thai-curry bravado story in `long_food_shopping_10.json` index 38 (Jaccard 0.0142); no semantic duplicate was found. Kept it `needs_revision` because wet labels only cause a routine order recheck, without an escalating consequence or satisfying comic reversal. Updated the ledger rationale; source content and app mirror remain unchanged.
- `python tools/validate_content.py` passed (8,000 entries), the mechanical checklist was regenerated, the V2 hash still matches the source row, and `git diff --check` passed. No app rebuild was needed. V2 total remains 1,664 pass / 3,336 needs_revision / 0 pending.
- Continue reviewing eligible distinct stories across the full 5,000-card scope.


## Active continuation — 2026-10-30, hiking sandwich batch 30

- Continued in the independent worktree; before this batch, local HEAD and the target remote branch were both `176a8b3a08aae911764ce502f26e08320ed7df4a`. The Desktop worktree remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_19.json` zero-based index 35. The hiking group forgets cutlery, cheese sticks to a thermos lid, and a friend opens a miniature kitchen to rescue the sandwich; the summit-shop callback pays off the food-and-hike setup. The supermarket sandwich ingredients stay central.
- Reviewed colloquial Macau Cantonese, contextual Jyutping (241 Han characters / 241 syllables), full Simplified Chinese gloss, and practice tip. The nearest approved character-trigram match was an unrelated clinic follow-up (Jaccard 0.0212).
- Updated the V2 status/hash, rebuilt `app/src/main/assets/builtin/content.json`, verified exact sentence/Jyutping/gloss/tip/category mirrors, blank `exampleSentence`, `entryType=sentence`, and `qualityPriority=1`. The mechanical audit had no failures; `python tools/validate_content.py` passed (8,000 entries), checklist regenerated, and `git diff --check` passed. Unit tests were not run.
- Current V2 total: 1,665 pass / 3,335 needs_revision / 0 pending. Content commit: `02bf2a4741a25eca8754f46326fb64424a130ff9`; checkpoint commit follows this update. Continue reviewing eligible distinct stories across the full 5,000-card scope.


## Active continuation - 2026-10-30, mango label callback batch 31

- Continued in the independent worktree `C:\Users\bankey\Documents\Codex\2026-10-29\task\jyut-soeng-v2-worktree`; before this batch, local HEAD and `origin/codex/macau-story-upgrade-batch-progress` both pointed to `e8327722fe7082fb3f3cd6d31bca9133a1fffa80`. The Desktop worktree remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_19.json` zero-based index 22. At the market, a friend repeatedly adds conflicting ripeness labels to three mangoes; cutting the vendor-picked ripe mango proves the advice, and a `後日` sticker landing on the friend’s sleeve sets up his “I need until next week to ripen” callback.
- Reviewed all four fields, Macau Cantonese, contextual Jyutping (272 Han characters / 272 syllables), and category fit. The maximum character-trigram Jaccard against V2-approved stories was 0.0120; nearest hits were unrelated receipt filing and fruit-return stories. No plot-level duplicate was found.
- Updated the V2 status/hash, rebuilt `app/src/main/assets/builtin/content.json`, and verified exact source-to-app sentence/Jyutping/gloss/tip mirrors, blank `exampleSentence`, `entryType=sentence`, and `qualityPriority=1`. The mechanical checklist reported 5,000/5,000; `python tools/validate_content.py` passed (8,000 entries), the checklist was regenerated, and `git diff --check` passed. Unit tests were not run.
- Current V2 total: 1,666 pass / 3,334 needs_revision / 0 pending. Content commit: `fbcac21` (`Review Cantonese mango story card`); recovery-checkpoint commit and remote verification follow. Continue reviewing eligible distinct stories across the full 5,000-card scope.


## Active continuation - 2026-10-30, reusable-container duplicate screen batch 32

- Continued in the independent worktree; local HEAD and `origin/codex/macau-story-upgrade-batch-progress` were both `252fa1d65a011a36791d59b07864af9fed070599` before this review. The Desktop worktree remains untouched.
- Re-screened `content/sentence_bank/long_food_shopping_19.json` zero-based index 25. Its reusable-box and produce-damage plot is too close to approved `content/sentence_bank/long_family_finance_services_01.json` index 24, where fruit falls from a reusable shopping bag and bystanders rescue it. Kept the card `needs_revision` and recorded the plot overlap and lack of an independent payoff in the V2 note.
- Source content and app mirror did not change. Regenerated the mechanical checklist; `python tools/validate_content.py` passed (8,000 entries), ledger hashes remain synchronized, and `git diff --check` passed. No app rebuild or unit tests were needed.
- V2 total remains 1,666 pass / 3,334 needs_revision / 0 pending. This is a note-only ledger update; checkpoint commit and remote verification follow. Continue screening and rewriting distinct eligible stories across the full 5,000-card scope.


## Active continuation - 2026-10-30, office drink-order duplicate screen batch 33

- Continued in the independent worktree; local HEAD and the target remote branch were both `ff58f102e004f8b9d30cfc6db6c5ddcd7ab7a871` before this review. The Desktop worktree remains untouched.
- Re-screened `content/sentence_bank/long_food_shopping_14.json` zero-based index 14. The group order is mislabeled, coworkers verify the order, and the shop remakes the drink; this repeats approved wrong-drink-label-and-remake plots at `long_food_shopping_02.json` index 51 and `long_food_shopping_04.json` index 73. Kept it `needs_revision` and recorded the overlaps. No source or app content changed.
- Regenerated the mechanical checklist; `python tools/validate_content.py` passed (8,000 entries), and `git diff --check` passed. No app rebuild or unit tests were needed.
- V2 total remains 1,666 pass / 3,334 needs_revision / 0 pending. Note-only ledger and checkpoint commits follow; continue screening and rewriting distinct eligible stories across the full 5,000-card scope.


## Active continuation - 2026-10-30, hotpot cooling-station batch 34

- Resumed from clean worktree HEAD `e634719` after verifying V2 counts at 1,666 pass / 3,334 needs_revision / 0 pending.
- Reworked `content/sentence_bank/long_food_shopping_14.json` zero-based index 9. The cousin who takes the wrong mala soup becomes the group’s “cooling station” as everyone else unexpectedly competes for spicy fish balls; both the mala pot and the milk run out, and she volunteers to buy clear soup next time.
- The plot’s escalation and ending differ from approved spice-bravado, hotpot-utensil management, and food-shape stories. Reviewed Macau Cantonese, contextual Jyutping (257 Han characters / 257 syllables), complete Simplified Chinese gloss, and story-specific practice tip.
- Updated the V2 ledger hash/status, rebuilt the app bundle, and confirmed exact source-to-app sentence/Jyutping/gloss/tip matches with `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries); checklist regenerated; `git diff --check` passed. New V2 count: 1,667 pass / 3,333 needs_revision / 0 pending. Unit tests were not run.
- Content, app mirror, ledger, checklist, and this recovery note are ready for local commits. Continue reviewing distinct cards across all 5,000.


## Active continuation - 2026-10-30, tomato kindergarten batch 35

- Continued from clean HEAD `b4ae950`; verified the target remote branch was also at `b4ae9500cbb394cd2383da79c51d369366019205` before editing.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 7. The daughter treats sprouted tomato seeds as a kindergarten class: they get seats, lean toward the kitchen, and all graduate into the tomato soup. The market-produce setup now drives an escalating comic scene and a final callback.
- Reviewed colloquial Cantonese, Jyutping (220 Han characters / 220 syllables), complete Simplified Chinese gloss, and practice tip. Character-trigram screening against approved stories found no close match (closest non-self score 0.0164, an unrelated story).
- Updated V2 status/hash, rebuilt the app bundle, and verified exact source-to-app sentence/Jyutping/gloss/tip matches with `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries); checklist regenerated; `git diff --check` passed. V2 count: 1,668 pass / 3,332 needs_revision / 0 pending. Unit tests were not run.
- Source, app mirror, ledger, checklist, and recovery note are ready for local commit and remote fast-forward verification. Continue across all 5,000 cards.


## Active continuation - 2026-10-30, fried-rice inspector batch 36

- Continued from clean HEAD `c5f6f7ae1870209773d98b24c15b9d7b460bd81f`; confirmed the target remote branch matched before editing. Desktop worktree remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 15. The brother packs leftover fried rice, labels a drawn shrimp as the “waste inspector,” and the sister ends its shift by handing him the container-washing job. His request to promote the shrimp to a stricter lobster inspector pays off the callback.
- Screened against approved leftover stories, including the power-outage dinner and restaurant box mix-up; the supervising-paper-shrimp and chore-handoff mechanism is distinct. Reviewed colloquial Cantonese, Jyutping (221 Han / 221 syllables), complete Simplified Chinese gloss, and practice tip.
- Updated ledger hash/status and app bundle; exact source-to-app sentence/Jyutping/gloss/tip matches verified with `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), checklist regenerated, and `git diff --check` passed. V2 count: 1,669 pass / 3,331 needs_revision / 0 pending. Unit tests were not run.
- Content and recovery checkpoint are ready for local commit; continue reviewing all remaining cards.


## Active continuation - 2026-10-30, allergy-safety screen batch 37

- Re-screened `content/sentence_bank/long_food_shopping_01.json` zero-based index 16. The family correctly checks peanut-allergy risk with the kitchen and declines the dish when cross-contact cannot be ruled out. The safety handling must remain explicit; the current scene still lacks a comic turn.
- Kept the card `needs_revision` and clarified its ledger note: do not create humor by weakening allergy precautions or having anyone taste uncertain food; a later revision should draw humor from a separate, low-risk detail.
- Source and app mirror are unchanged. Checklist regenerated; `python tools/validate_content.py` passed (8,000 entries), and `git diff --check` passed. V2 totals remain 1,669 pass / 3,331 needs_revision / 0 pending.
- Commit and remote verification follow. Continue reviewing distinct cards across the full set.


## Active continuation - 2026-10-30, separated-sauce traffic batch 38

- Continued from clean HEAD `1bac524b0a61f4cfbc5747135741d316c56d135a`; confirmed remote target matched before editing.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 20. The requested separate sauces become “no-chili” and chili traffic lanes; the younger brother uses chopstick barriers, makes a zebra crossing, and issues a hand-drawn pass before the family’s “sauce traffic jam” callback.
- Screened against approved spicy-food taste reversals and food-sharing stories; the traffic-control sauce gag is distinct. Reviewed Cantonese, Jyutping (239 Han / 239 syllables), full Simplified Chinese gloss, and practice tip.
- Updated V2 hash/status and app bundle; exact source-to-app sentence/Jyutping/gloss/tip matches verified, with `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), checklist regenerated, and `git diff --check` passed. V2 count: 1,670 pass / 3,330 needs_revision / 0 pending. Unit tests were not run.
- Content and recovery note are ready for local commit and remote fast-forward verification. Continue reviewing all remaining cards.


## Active continuation - 2026-10-30, leaking soup delivery screen batch 39

- Re-screened `content/sentence_bank/long_food_shopping_01.json` zero-based index 21. The leaking soup is photographed and replaced, then the household updates the delivery address note. These steps solve the service issue but do not create a comic escalation or payoff.
- Compared it with approved `long_home_family_08.json` indexes 166 (delivery misunderstanding and address-note correction) and 171 (delivery wait interrupted by a soup near-boil). Surface details differ, but this card still follows a routine correction pattern; kept it `needs_revision` and recorded the reason.
- Source and app mirror are unchanged. Checklist regenerated; `python tools/validate_content.py` passed (8,000 entries), `git diff --check` passed. V2 remains 1,670 pass / 3,330 needs_revision / 0 pending.
- Commit and remote verification follow. Continue the full 5,000-card review.


## Active continuation - 2026-10-30, rainy delivery story screen batch 40

- Re-screened `content/sentence_bank/long_food_shopping_01.json` zero-based index 25. Rain leads to a napkin, extra chopsticks, and a neighbor sharing food; the kindness is coherent but has no comic escalation or reversal. The later platform promise to check addresses is administrative and does not pay off the meal scene.
- Kept it `needs_revision`, recording the need for a distinct joke that grows from the delivery/chopsticks while preserving the neighbor beat. Source and app mirror are unchanged.
- Checklist regenerated; `python tools/validate_content.py` passed (8,000 entries), and `git diff --check` passed. V2 remains 1,670 pass / 3,330 needs_revision / 0 pending.
- Commit and remote verification follow. Continue across all remaining cards.


## Active continuation - 2026-10-30, yogurt shift-roster batch 41

- Continued from clean HEAD `ebe07f2`; confirmed the target branch matched before editing.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 27. The sister turns expiry-date order into a yogurt shift roster, gives the fridge a clock-in station, stops Dad from letting a newer carton cut the queue, and stamps the older carton “on time” when breakfast uses it. Blueberries serve as backup and the next-shopping callback closes the office-roleplay gag.
- Compared with approved `long_food_shopping_07.json` index 25 (strawberry selection/family tasting), `long_food_shopping_13.json` index 1 (blueberry pancake guessing), and `long_family_finance_services_12.json` index 36 (bulk coffee savings/expiry arithmetic); mechanisms differ. Reviewed Cantonese, Jyutping (222 Han / 222 syllables), full Simplified gloss and practice tip. Nearest non-self trigram Jaccard was 0.0196, with no plot-level duplicate.
- Updated ledger hash/status and rebuilt app assets; exact source-to-app sentence/Jyutping/gloss/tip verified with `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), checklist regenerated, and `git diff --check` passed. V2 count: 1,671 pass / 3,329 needs_revision / 0 pending. Unit tests were not run.
- Content and checkpoint are ready for local commit and remote fast-forward verification. Continue reviewing all 5,000 cards.


## Active continuation - 2026-10-30, steamed-egg sample judge batch 47

- Continued from clean HEAD `45c42b272ebe5db9098e980746ada3a07112e043`; confirmed target remote matched before editing.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 45. Kept the bubble-skimming, covered bowl and timer sequence; the daughter signs up to judge the next shrimp version, while Dad volunteers as first taster and keeps taking spoonfuls “for fairness.” Her score sheet records the sample already half gone, and she limits his next round to one spoon.
- Compared with approved `long_home_family_04.json` index 91 (salt/sugar mistake turns egg into pudding), `long_family_finance_services_02.json` index 28 (salty coconut cake/condensation cloth), and `long_food_shopping_11.json` index 8 (blind ingredient misidentification); mechanisms differ. Reviewed Cantonese, Jyutping (254 Han / 254 syllables), complete gloss and practice tip. Closest non-self trigram Jaccard was 0.0200.
- Updated V2 hash/status and rebuilt app assets; exact source-to-app sentence/Jyutping/gloss/tip verified with `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), checklist regenerated, and `git diff --check` passed. V2 count: 1,675 pass / 3,325 needs_revision / 0 pending. Unit tests were not run.
- Content and checkpoint are ready for local commit and remote fast-forward verification. Continue reviewing all 5,000 cards.


## Active continuation - 2026-10-30, hidden-candy duplicate screen batch 44

- Re-screened `content/sentence_bank/long_food_shopping_01.json` zero-based index 40. Its nephew pockets a candy, is discovered, returns it and receives one after completing the list.
- Compared the reveal/confession chain with approved `content/sentence_bank/long_home_family_09.json` index 71, where Grandma secretly slips a sweet into a schoolbag and the family discovers it. The character roles differ, but hidden candy + discovery + honesty resolution are too close to pass. Kept index 40 `needs_revision` and recorded that the next rewrite must drop the pocketing/reveal mechanism and build from the store-manager role or list rule.
- Source and app mirror are unchanged. Checklist regenerated; `python tools/validate_content.py` passed (8,000 entries), and `git diff --check` passed. V2 remains 1,673 pass / 3,327 needs_revision / 0 pending.
- Commit and remote verification follow. Continue reviewing the full set.


## Active continuation - 2026-10-30, off-duty shopkeeper candy callback batch 46

- Continued from clean HEAD `a0bd9c42c70e9d2dc4bcc26af4caa827c661c755`; confirmed the target remote branch matched before editing.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 40 and removed the overlapping hidden-candy reveal entirely. The nephew follows the grocery list, carefully bags the food as a “shop manager,” then picks one candy only after the list is complete and asks for it to be scanned. His line—“off duty now, I’m a customer, not stock”—and the hat/shift callback complete the identity-switch gag.
- Compared against approved `long_home_family_09.json` index 71 (secret schoolbag sweet) and `long_food_shopping_01.json` index 28 (faulty cart steering shoppers to checkout); the new story has neither mechanism. Reviewed colloquial Cantonese, Jyutping (227 Han / 227 syllables, including contextual 店長 zoeng2), full Simplified gloss and tip.
- Updated V2 hash/status and rebuilt app assets; exact source-to-app sentence/Jyutping/gloss/tip verified with `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), checklist regenerated, and `git diff --check` passed. V2 count: 1,674 pass / 3,326 needs_revision / 0 pending. Unit tests were not run.
- Content and checkpoint are ready for local commit and remote fast-forward verification. Continue reviewing all 5,000 cards.


## Active continuation - 2026-10-30, curry-list responsibility batch 43

- Continued from clean HEAD `c53058a50cb47c3ee25bf07b8a64054bf8d6414f`; confirmed target remote matched before editing.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 35. The weekly shopping list stays central; when Dad requests curry, his daughter writes the proposer down for ingredients, cooking and washing the pot. His handwritten “taster exempt from washing” clause is crossed out, paying off the list-as-agreement joke.
- Screened against approved grocery-list, menu and family-cooking stories; none shares this proposal-to-kitchen-duty reversal. Reviewed colloquial Cantonese, Jyutping (259 Han / 259 syllables), complete gloss and practice tip. Nearest non-self trigram Jaccard was 0.0154; no plot-level duplicate found.
- Updated V2 hash/status and rebuilt app assets; exact source-to-app sentence/Jyutping/gloss/tip verified with `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), checklist regenerated, and `git diff --check` passed. V2 count: 1,673 pass / 3,327 needs_revision / 0 pending. Unit tests were not run.
- Content and checkpoint are ready for local commit and remote fast-forward verification. Continue reviewing all 5,000 cards.


## Active continuation - 2026-10-30, supermarket traffic officer batch 42

- Continued from clean HEAD `f851576857b47113c6c10cf53b1f860e0a300cc2`; confirmed the target remote branch matched before editing.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 30. The child’s small trolley repeatedly meets the narrator’s cart in narrow aisles; their right-of-way standoff becomes a traffic jam, the scallion is used as a turn signal, and the child directs the checkout lane. The closing “traffic officer” vacation callback pays off the supermarket encounter while the shopping list and tomato-chicken soup remain central.
- Screened approved cart/trolley stories; their squeaky-wheel, moving-carton and delivery-trolley plots differ from this supermarket right-of-way scene. Reviewed Cantonese, Jyutping (223 Han / 223 syllables), complete gloss and practice tip. Nearest non-self trigram Jaccard was 0.0219; no plot-level duplicate found.
- Updated V2 hash/status and app assets; exact source-to-app sentence/Jyutping/gloss/tip verified with `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), checklist regenerated, and `git diff --check` passed. V2 count: 1,672 pass / 3,328 needs_revision / 0 pending. Unit tests were not run.
- Content and checkpoint are ready for local commit and remote fast-forward verification. Continue reviewing all 5,000 cards.

## Active continuation - 2026-10-30, chopped-coriander excuse batch 48

- Continued from clean HEAD `3839000bf6829de38abb3027a48174b2c00cd83d`; verified `origin/codex/macau-story-upgrade-batch-progress-resume` matched before editing. Desktop worktree remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 50. Removed the unrelated congee-sticking problem. The brother claims he dislikes coriander, adds two spoonfuls when the guest does, then admits he dislikes chopping it. His sister records the excuse as a recipe note; the final line teases him for pretending not to like pre-chopped coriander.
- Compared the plot mechanism with approved spicy-food/bravado stories; no approved coriander-prep excuse or recipe-label callback found. Reviewed Cantonese, contextual Jyutping (232 Han / 232 syllables), full Simplified Chinese gloss and practice tip.
- Updated V2 hash/status and rebuilt app assets; source/app sentence, Jyutping, gloss and tip match, with `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), checklist regenerated, and `git diff --check` passed. V2 count: 1,676 pass / 3,324 needs_revision / 0 pending. Unit tests were not run.
- Ready for local commit and remote fast-forward verification. Continue reviewing all 5,000 cards.

## Active continuation - 2026-10-30, breakfast shift roster batch 49

- Continued from clean HEAD `ec32c883d6472ebd40758e47c93ca42b2b9e6f64`; GitHub branch was verified at the same SHA. Desktop worktree remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 53. Kept the mold report, batch check, refund and supplier notice explicit without opening or eating the affected bread. The daughter assigns the egg tart and soy milk temporary breakfast shifts; the fresh loaf returns to work, the tart clocks out, then gets an extra shift in her stomach.
- Compared with nearby food-return stories; the breakfast shift-roster and clock-out callback is distinct. Reviewed colloquial Cantonese, contextual Jyutping (253 Han / 253 syllables), full Simplified Chinese gloss and practice tip.
- Updated V2 hash/status and rebuilt app assets; source/app sentence, Jyutping, gloss and tip match, with `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), checklist regenerated, and `git diff --check` passed. V2 count: 1,677 pass / 3,323 needs_revision / 0 pending. Unit tests were not run.
- Ready for local commit and remote fast-forward verification. Continue reviewing all 5,000 cards.

## Active continuation - 2026-10-30, folding-stool yogurt return batch 50

- Continued from clean HEAD `2a7efcf98095f7cd029a5545f2d514bf808d4e84`; GitHub branch was verified at the same SHA. Desktop worktree remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 54. Kept the yogurt sealed, reported its abnormal condition, held the batch, refunded the purchase and checked the refrigerator; nobody tastes the questionable food. The mother brings a folding stool expecting a long return, but the refund finishes before she opens it. Her daughter says the refrigerator is working overtime while the stool can take the day off; the closing line calls back to checking whether the fridge is on shift before bringing the stool.
- Compared with approved stool stories about a meeting and a water-station queue; the return-counter timing reversal is distinct. Reviewed colloquial Cantonese, contextual Jyutping (309 Han / 309 syllables), full Simplified Chinese gloss and practice tip.
- Updated V2 hash/status and rebuilt app assets; source/app sentence, Jyutping, gloss and tip match, with `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), checklist regenerated, and `git diff --check` passed. V2 count: 1,678 pass / 3,322 needs_revision / 0 pending. Unit tests were not run.
- Ready for local commit and remote fast-forward verification. Continue reviewing all 5,000 cards.

## Active continuation - 2026-10-30, halftime biscuit passing batch 51

- Continued from clean HEAD `03d333a0206bd789a063dde3b39bc58031b44714`; GitHub branch was verified at the same SHA. Desktop worktree remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 55. Kept the spicy packet sealed and exchanged it at the same price for sea-salt flavor. At halftime, the biscuits are passed around faster than the ball; the captain writes “two packs next time” on the empty bag, and the cousin records that one pack was not enough to pass around.
- Compared with approved spicy-food/bravado stories; this is an unopened wrong-flavor exchange with a soccer passing callback, not a taste-tolerance reversal. Reviewed Cantonese, contextual Jyutping (271 Han / 271 syllables), full Simplified Chinese gloss and practice tip.
- Updated V2 hash/status and rebuilt app assets; source/app sentence, Jyutping, gloss and tip match, with `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), checklist regenerated, and `git diff --check` passed. V2 count: 1,679 pass / 3,321 needs_revision / 0 pending. Unit tests were not run.
- Ready for local commit and remote fast-forward verification. Continue reviewing all 5,000 cards.

## Active continuation - 2026-10-30, almond-cake intact-piece contest batch 52

- Continued from clean HEAD `ec0a06fa17c891d452a8fbe7dbdf3d2805b7be12`; GitHub branch was verified at the same SHA. Desktop worktree remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 64. Kept the damaged-box report and same-batch inspection/replacement. At the tea visit, everyone reaches for the most intact almond cake at once and breaks it into pieces; the grandmother’s final inspection becomes the callback.
- Compared with approved fragment-sharing and mooncake stories; the intact-piece contest after a transit-damage exchange is distinct. Reviewed Cantonese, contextual Jyutping (255 Han / 255 syllables), full Simplified Chinese gloss and practice tip.
- Updated V2 hash/status and rebuilt app assets; source/app sentence, Jyutping, gloss and tip match, with `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), checklist regenerated, and `git diff --check` passed. V2 count: 1,680 pass / 3,320 needs_revision / 0 pending. Unit tests were not run.
- Indices 56–63 retain their current ledger decisions and were not changed in this batch. Continue reviewing all 5,000 cards.
