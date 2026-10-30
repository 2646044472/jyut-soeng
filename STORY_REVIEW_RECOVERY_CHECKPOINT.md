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

## Active continuation - 2026-10-30, secondhand oven stage-light callback batch 53

- Continued from clean HEAD `46db007c6b01052cafa4b52322ca62837fe3a8ab`; GitHub branch was verified at the same SHA. Desktop worktree remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 65. Kept the safe process: cut power when the lamp flickers, find and disclose the loose extension-board connection, test the oven, then unplug and cool it before handover. The mother mistakes the two flashes for stage lighting; the buyer asks whether the “stage light” comes with the oven, paying off the quip.
- Compared with approved secondhand-oven transaction stories; this lamp/extension-board callback is distinct. Reviewed Cantonese, contextual Jyutping (256 Han / 256 syllables), full Simplified Chinese gloss and practice tip.
- Updated V2 hash/status and rebuilt app assets; source/app sentence, Jyutping, gloss and tip match, with `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), checklist regenerated, and `git diff --check` passed. V2 count: 1,681 pass / 3,319 needs_revision / 0 pending. Unit tests were not run.
- Indices 56–63 retain their current ledger decisions and were not changed in this batch. Continue reviewing all 5,000 cards.

## Active continuation - 2026-10-30, hot-joke ice-cream verdict batch 54

- Continued from clean HEAD `45269483cb6c3c9cf49fbd1d5f391c60aacf593a`; GitHub branch was verified at the same SHA. Desktop worktree remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 56. The niece jokes that her “hot jokes” melted the ice cream; the store’s temperature log identifies a freezer fault instead. The replacement-photo caption “fridge guilty, joke innocent” pays off the false explanation. No one tastes the softened product; the package/time are recorded, the freezer is checked and affected stock is paused.
- Compared with the approved family ice-cream photo and sleeve-stain story; the cold-chain verdict and joke-alibi mechanism is distinct. Reviewed Cantonese, contextual Jyutping (273 Han / 273 syllables), full Simplified Chinese gloss and practice tip.
- Updated V2 hash/status and rebuilt app assets; source/app sentence, Jyutping, gloss and tip match, with `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), checklist regenerated, and `git diff --check` passed. V2 count: 1,682 pass / 3,318 needs_revision / 0 pending. Unit tests were not run.
- Indices 57–63 retain their current ledger decisions and were not changed in this batch. Continue reviewing all 5,000 cards.

## Active continuation - 2026-10-30, soy-milk “morning encouragement” batch 55

- Continued from clean HEAD `7b943943cf97129d88841890c7b9e8024a473700`; GitHub branch was verified at the same SHA. Desktop worktree remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 57. Kept the soy milk sealed until the same-price exchange. The store’s “早晨加油” sticker now drives the office payoff: a coworker turns “加油” into meeting encouragement and extends “微甜” to the morning meeting, asking for an on-time finish.
- Compared with other retail-return stories; the office breakfast / morning-meeting wordplay is distinct. Reviewed Cantonese, contextual Jyutping (282 Han / 282 syllables), full Simplified Chinese gloss and practice tip.
- Updated V2 hash/status and rebuilt app assets; source/app sentence, Jyutping, gloss and tip match, with `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), checklist regenerated, and `git diff --check` passed. V2 count: 1,683 pass / 3,317 needs_revision / 0 pending. Unit tests were not run.
- Indices 58–63 retain their current ledger decisions and were not changed in this batch. Continue reviewing all 5,000 cards.

## Active continuation - 2026-10-30, soy-milk nose inspector batch 56

- Continued from clean HEAD `c5c27ff5e177fcf8eb3200dc063ac41e2bfc494a`; GitHub branch was verified at the same SHA. Desktop worktree remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 59. Preserved the no-tasting response, documentation, batch withdrawal, refund and refrigeration advice. The brother’s “nose before the alarm” quip becomes a self-appointed early-shift inspector: he checks the replacement package seal and date, asks when his nose can clock out, and is told the checklist is sufficient.
- Compared with neighboring dairy-return plots; the family nose-inspector shift callback is distinct. Reviewed Cantonese, contextual Jyutping (268 Han / 268 syllables), full Simplified Chinese gloss and practice tip.
- Updated V2 hash/status and rebuilt app assets; source/app sentence, Jyutping, gloss and tip match, with `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/validate_content.py` passed (8,000 entries), checklist regenerated, and `git diff --check` passed. V2 count: 1,684 pass / 3,316 needs_revision / 0 pending. Unit tests were not run.
- Indices 60–63 retain their current ledger decisions and were not changed in this batch. Continue reviewing all 5,000 cards.

## Active continuation - 2026-10-30, full-fat / omniscience callback batch 57

- Continued from clean local HEAD `974871a9af2187d85384ebd976e5185ad334eb08`. Before editing, the authorized remote branch `origin/codex/macau-story-upgrade-batch-progress-resume` was read successfully and matched that SHA. The Desktop checkout remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 60. Kept the unopened low-fat/full-fat exchange and changed the color-band reminder into a Cantonese homophone payoff: `全脂／全知`. After replacing color marks with written words on the list, the aunt asks whether the narrator is now omniscient; the answer is “我唔全知，但我知要睇字.”
- Reviewed colloquial Cantonese, contextual Jyutping (226 Han characters / 226 syllables), the full Simplified Chinese gloss, and practice tip. The plot was compared with nearby retail-return stories and is distinct by its fat-level/omniscience wordplay.
- Updated the V2 decision and current row hash, rebuilt app assets, and confirmed exact source/app matches for sentence, Jyutping, gloss, and usage tip; app metadata is `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/build_assets.py`, `python tools/validate_content.py` (8,000 entries), `python tools/story_quality_progress.py --output STORY_QUALITY_CHECKLIST.md`, and `git diff --check` passed. Current V2 total: 1,685 pass / 3,315 needs_revision / 0 pending. No unit tests were run.
- Next: continue semantic and language review from index 62 in this source file; preserve the remaining 5,000-card scope.


## Active continuation - 2026-10-30, soy-sauce newspaper desk batch 58

- Continued from clean local HEAD `2d0046f688afba497a44890b0b637114ea5012ab`; immediately before preparing this batch, `git ls-remote` confirmed the authorized target branch at the same SHA. The Desktop checkout remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 62. Retained leak isolation, photos, batch/receipt records, same-batch inspection, shelf hold, warehouse bottle checks, and exchange of a sealed replacement. Removed the unnecessary home leak test. The father turns the absorbent old newspaper into a mock soy-sauce column: cracked bottle headline, “kitchen nearly became an oilfield” subhead, and a callback appointing him reporter for the next trace.
- Reviewed colloquial Cantonese, contextual Jyutping (278 Han / 278 syllables), full Simplified Chinese gloss, and practice tip. The newspaper reporting payoff was compared with nearby return stories and is distinct.
- Updated V2 hash/status and rebuilt app assets. Exact source/app sentence, Jyutping, gloss, and tip match; metadata is `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/build_assets.py`, `python tools/validate_content.py` (8,000 entries), `python tools/story_quality_progress.py --output STORY_QUALITY_CHECKLIST.md`, and `git diff --check` passed. Current V2 total: 1,686 pass / 3,314 needs_revision / 0 pending. No unit tests were run.
- Next: continue from index 63 and preserve the full 5,000-card review scope.


## Active continuation - 2026-10-30, tofu-casting callback batch 59

- Continued from clean local HEAD `1f92e20b31f7d4b05190257f0a3fac86255e954e`; immediately before preparing this batch, `git ls-remote` confirmed the authorized target branch at the same SHA. The Desktop checkout remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 63 from a family dinner into a coworker meal in the company kitchen. Kept the sealed tofu package, receipt, same-price exchange, store’s explanation of firm versus soft tofu, and use of the soft tofu in fish soup. A coworker jokes that the upright firm tofu is a guest actor who will not enter the soup; after the exchange, soft tofu is cast as the lead and firm tofu as a frying-pan cameo. The “next episode” line asks shoppers to check the label before cooking.
- Screened against the approved fish-market tofu-pitch story and the office instant-soup deadline misunderstanding. Their vendor-promotion and project-tracking mechanisms differ from this tofu-type return and film-casting callback. Reviewed colloquial Cantonese, contextual Jyutping (234 Han / 234 syllables), complete Simplified Chinese gloss, and practice tip.
- Updated the V2 hash/status and rebuilt app assets. Exact source/app sentence, Jyutping, gloss, and tip match; metadata is `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/build_assets.py`, `python tools/validate_content.py` (8,000 entries), `python tools/story_quality_progress.py --output STORY_QUALITY_CHECKLIST.md`, and `git diff --check` passed. Current V2 total: 1,687 pass / 3,313 needs_revision / 0 pending. No unit tests were run.
- Indices 64–66 are already pass; continue from index 67 and preserve the full 5,000-card review scope.


## Active continuation — 2026-10-30, cooler-capacity handover batch 60

- Resumed from local `HEAD` `8ecf84e4591db1f326dc5a2089e005893fb353f7`; immediately before editing, `git ls-remote` confirmed `origin/codex/macau-story-upgrade-batch-progress-resume` at the same SHA. The Desktop repository remains untouched.
- Replaced `content/sentence_bank/long_food_shopping_01.json` zero-based index 67. The previous new-blender safety-interlock plot overlapped the still-unapproved index 70 blender story and also repeated the adjacent secondhand appliance run. The replacement is a secondhand cooler-box capacity negotiation: 24 250 ml cans fit without two ice packs, but only 18 fit with them. Buyer and seller agree on a price adjustment and a clearer listing; a hiking-group “ice included?” exchange pays off as a “who covers the carrying?” wordplay gag.
- Reviewed colloquial Cantonese, contextual Jyutping (259 Han / 259 syllables), complete Simplified Chinese gloss, and practice tip. Compared adjacent secondhand appliance stories and searched the corpus for cooler/ice-pack plots.
- Updated the V2 row hash/status and rebuilt the app bundle. Exact source/app sentence, Jyutping, gloss, and tip match; metadata is `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/build_assets.py`, `python tools/validate_content.py` (8,000 entries), `python tools/story_quality_progress.py --output STORY_QUALITY_CHECKLIST.md`, and `git diff --check` passed. V2 remains 1,688 pass / 3,312 needs_revision / 0 pending.
- Next audit: zero-based index 68, which remains `needs_revision`; screen its used-coffee-machine story before revising it.


## Remote confirmation — 2026-10-30

- Content batch commit `c7d1384cd443a925ca8d5fede342bdb8f0eae951` was pushed by ordinary fast-forward to `origin/codex/macau-story-upgrade-batch-progress-resume`; a subsequent `git ls-remote` returned the same SHA. Local `HEAD` matched, and the worktree was clean at verification.
- V2 total remains 1,688 pass / 3,312 needs_revision / 0 pending. Continue at `content/sentence_bank/long_food_shopping_01.json` zero-based index 68; keep the remaining 5,000-card objective in scope.


## Active continuation — 2026-10-30, office-chair height callback batch 61

- Continued from verified local/remote checkpoint commit `571f791106eca9ca80460c484c0fbd3dacc0494b`; the Desktop repository remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 68. Replaced the repetitive used-coffee-machine leak/repair transaction with a secondhand office-chair purchase. The seated buyer mistakes normal downward adjustment for a defect; the seller demonstrates the height lever, the buyer confirms the lift and swivel, and the coworkers turn the chair’s height into a “chair promoted, person not” office callback.
- Reviewed colloquial Cantonese, contextual Jyutping (228 Han / 228 syllables), complete Simplified Chinese gloss, and practice tip. Screened for existing office-chair / height-control plots.
- Updated the V2 row hash/status and rebuilt the app bundle. Exact source/app sentence, Jyutping, gloss, and tip match for indexes 67 and 68; metadata is `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/build_assets.py`, `python tools/validate_content.py` (8,000 entries), `python tools/story_quality_progress.py --output STORY_QUALITY_CHECKLIST.md`, and `git diff --check` passed. Current V2 total: 1,689 pass / 3,311 needs_revision / 0 pending.
- Next audit: zero-based index 69, which remains `needs_revision`; screen the used-rice-cooker story against the surrounding used-appliance sequence before revising it.


## Active continuation — 2026-10-30, secondhand-wallet stamp-card callback batch 62

- Continued from local/remote `HEAD` `51f3b064a4bb236cfd016539b1ba5802af468b85`; the Desktop repository remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 69. Replaced the repetitive used-rice-cooker defect/cancellation story with a secondhand wallet handover. After the buyer returns the forgotten near-complete café stamp card, the seller redeems a free milk tea and gives it to the buyer; “interest / account balance” returns on the receipt that goes into the new wallet.
- Screened the nearby used-appliance stories and searched wallet/stamp-card plots. The corpus has a family grocery-promotion story with a stamp card that earns a rice cooker, but its plot and callback differ from this honest-return/free-drink handover.
- Reviewed colloquial Cantonese, contextual Jyutping (232 Han / 232 syllables), complete Simplified Chinese gloss, and practice tip. Updated the V2 row hash/status and rebuilt the app bundle. Exact source/app sentence, Jyutping, gloss, and tip match for indexes 67–69; each has `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/build_assets.py`, `python tools/validate_content.py` (8,000 entries), `python tools/story_quality_progress.py --output STORY_QUALITY_CHECKLIST.md`, and `git diff --check` passed. Current V2 total: 1,690 pass / 3,310 needs_revision / 0 pending.
- Next audit: zero-based index 70, which remains `needs_revision`; screen the used-blender safety-interlock plot against the new distinct batch and surrounding secondhand stories.


## Active continuation — 2026-10-30, pinhole-curtain pointer gag batch 63

- Continued from local/remote `HEAD` `f4786eab7e60c8acfdbcc89ce0b3912f383b37b3`; the Desktop repository remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 70. Replaced the repetitive blender safety-interlock story with a secondhand blackout curtain whose disclosed pinhole sends a moving sunspot across a whiteboard. Volunteers mistake the dot for the presenter’s laser pointer and stand when it reaches “lunch break”; the director asks if another hole can cue the end of day, paying off the disclosed defect and negotiated discount.
- Screened against curtain stories elsewhere in the corpus; those concern reducing window glare and do not use the pinhole as a moving false pointer. Reviewed colloquial Cantonese, contextual Jyutping (235 Han / 235 syllables), complete Simplified Chinese gloss, and practice tip.
- Updated the V2 row hash/status and rebuilt the app bundle. Exact source/app sentence, Jyutping, gloss, and tip match for indexes 67–70; each has `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- `python tools/build_assets.py`, `python tools/validate_content.py` (8,000 entries), `python tools/story_quality_progress.py --output STORY_QUALITY_CHECKLIST.md`, and `git diff --check` passed. Current V2 total: 1,691 pass / 3,309 needs_revision / 0 pending.
- Next audit: zero-based index 71, which remains `needs_revision`; compare its used-oven troubleshooting story with index 65 before revising.


## Active continuation — 2026-10-30, oven-demo queue callback batch 64

- Continued from verified local/remote checkpoint `a0458f005149d6ba58e4c5d6a36af8e6b5241d3f`; work began from a clean independent worktree, leaving the Desktop checkout untouched.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 71. Replaced the repetitive secondhand-oven troubleshooting report with a home demonstration: neighbors smell a test egg tart and mistake the oven inspection for a shop opening, then ask whether they need to pre-order after the oven is sold. The closing “只係開爐，冇開舖” callback resolves that mix-up.
- Screened approved index 65 (lamp flicker mistaken for stage lighting) and approved `long_food_shopping_04.json` index 14 (damaged wiring and safe cancellation), plus other oven/tart stories. Their plot mechanisms differ from this neighbor queue and shop-opening misunderstanding. Reviewed colloquial Cantonese, contextual Jyutping (309 Han / 309 syllables), full Simplified Chinese gloss, and practice tip.
- Updated the V2 row hash/status and rebuilt the app assets. Source/app sentence, Jyutping, gloss, and tip must match exactly; generated metadata should remain `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`.
- Current expected V2 total after regeneration: 1,692 pass / 3,308 needs_revision / 0 pending. Next, continue to the next eligible `needs_revision` card while screening category and plot duplication, preserving the 5,000-card scope.


## Active continuation — 2026-10-30, handcart and large-pot wordplay batch 65

- Continued from verified local/remote checkpoint `d33f29ae2ab17ef29f22a0618294d87bab041b7d` in the independent worktree; the Desktop checkout remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 72. Replaced the mild recovery-exercise ending with two connected wordplay beats: a seller assumes “有車” means a private car when the buyer means a handcart, and a broken lift turns the oversized soup pot into “大煲／大鑊.”
- Preserved safe handling: the buyer checks the pot, secures it on a handcart, avoids a warned slippery alley for a handrailed route, and tests it with half a pot of water; the seller with a back injury does not lift or push the load. Screened approved oven stories at indexes 65 and 71 and other pot/elevator plots; the used-pot transport and wordplay mechanism is distinct. Reviewed colloquial Cantonese, contextual Jyutping (306 Han / 306 syllables), complete Simplified Chinese gloss, and practice tip.
- Updated the V2 row hash/status; next rebuild app assets, verify exact source/app fields and all content gates, then commit and push. Expected progress after regeneration: 1,693 pass / 3,307 needs_revision / 0 pending.


## Active continuation — 2026-10-30, cracked-juicer photo-filter callback batch 66

- Continued from verified local/remote checkpoint `5d6c9a88627b9c8ff687716c3a7253cfd9a86578` in the independent worktree; the Desktop checkout remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 73. The seller's listing photo used a different, intact cup; after the buyer finds a crack, they check the model and call a parts shop, learning the replacement is discontinued. The seller corrects the listing. The close distinguishes a photo filter from a juicer's filtering action.
- Preserved the safety step: the manual warns against operating a cracked cup, so the pair does not plug it in or attempt a powered test. Screened other juicer/filter stories; no same mechanism was found. Reviewed colloquial Cantonese, contextual Jyutping (260 Han / 260 syllables), complete Simplified Chinese gloss, and practice tip.
- Updated the V2 row hash/status; next rebuild app assets, verify source/app mirrors and content gates, then commit and push. Expected progress after regeneration: 1,694 pass / 3,306 needs_revision / 0 pending.

## Active continuation — 2026-10-30, used-coat reminder callback batch 67

- Continued from verified local/remote checkpoint `56fc10f2cae4700ef6d1828527ea5c7a7aa34f39` in the independent worktree; the Desktop repository remains untouched. Zero-based index 74 was already a V2 pass and needed no edit.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 75. Replaced the overlapping used-table/loose-screw repair with a secondhand coat whose pockets contain repeated shopping notes to buy milk and a final note that the refrigerator is full. The seller jokes that the coat includes a reminder service; after following the garment-care label, the buyer writes the same reminder and discovers their own forgetfulness, completing the callback.
- Compared against the earlier, unapproved wobbly-chair story at `long_food_shopping_04.json` index 90, approved `long_home_family_08.json` index 141 (wrong-item purchase followed by adding reminders to a list), and approved `long_food_shopping_01.json` indexes 17 and 28 (pastry handling and a faulty cart). The pocket-note discovery and buyer-inherits-the-reminder callback are distinct. Reviewed colloquial Cantonese, contextual Jyutping (281 Han/281 syllables), complete gloss, public handoff, garment-label washing, and practice tip.
- Rebuilt app assets and verified the matching entry’s sentence, Jyutping, gloss, and tip exactly; metadata remains `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`. `python tools/validate_content.py` validated 8,000 entries; `python tools/story_quality_progress.py --output STORY_QUALITY_CHECKLIST.md` reported 1,695 pass / 3,305 needs_revision / 0 pending; `git diff --check` passed.
- Content commit: `77b3a268eb9069883eac4cf260df4a8688e3590c`. Recovery-checkpoint commit, ordinary fast-forward push, and remote SHA verification follow. Next eligible card: zero-based index 77; index 76 is already a V2 pass.

## Active continuation — 2026-10-30, zero-fare and missing-cutlery callback batch 68

- Continued from verified local/remote checkpoint `010b6ad674756cb594759a2a948fbe1b2e87a76a` in the independent worktree; the Desktop repository remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 77. An overcareful coworker allocates the zero-dollar delivery fee exactly, then discovers he chose no cutlery and the office drawer has only three pairs for four people. A teammate gives him an unopened backup pair; he stocks four spare pairs, paying off the equal-split calculation with the closing “four pairs divided by four.”
- Compared with approved adjacent index 76 (a duplicate dim sum order and unclaimed final piece), approved index 78 (weak-signal payments and transfer screenshots), and other approved meal-bill stories. They do not share the zero-fee/cutlery-shortage callback. Reviewed colloquial Cantonese, contextual Jyutping (276 Han/276 syllables), full gloss, and practice tip.
- Rebuilt app assets and verified the matching entry’s sentence, Jyutping, gloss, and tip exactly; metadata remains `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`. `python tools/validate_content.py` validated 8,000 entries; `python tools/story_quality_progress.py --output STORY_QUALITY_CHECKLIST.md` reported 1,696 pass / 3,304 needs_revision / 0 pending; `git diff --check` passed.
- Content commit: `da6dd23ffe58e5717296224e8befd447368133d9`. Recovery-checkpoint commit, ordinary fast-forward push, and remote SHA verification follow. Next eligible card: zero-based index 79; index 78 is already a V2 pass.

## Active continuation — 2026-10-30, late dinner bill callback batch 69

- Continued from local content commit `4bbbd76453f96b1fbb1929ccc893e178e9e6beba` in the independent worktree; the Desktop repository remains untouched. The prior verified remote tip was `d28f341d20fe17aa2749631b5195d833a0518c76`.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 79. The late-arriving guest does not eat the main course and pays no share of it; the birthday guest treats the table to muhkwood pudding while he pays only for his own coffee. Their three-bus-transfer story loops back through the “pudding stop” and “main-course stop” to land the bill-splitting joke fairly.
- Compared against approved `long_food_shopping_08.json` index 30, whose restaurant-name mix-up is a different joke mechanism. Reviewed colloquial Cantonese and contextual Jyutping (224 Han characters / 224 syllables), complete Simplified Chinese gloss, and practice tip.
- Rebuilt the app mirror and verified sentence, Jyutping, gloss, and practice tip match the source exactly; metadata is `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`. `python tools/validate_content.py` validated 8,000 entries; `python tools/story_quality_progress.py --output STORY_QUALITY_CHECKLIST.md` reported 1,697 pass / 3,303 needs_revision / 0 pending; `git diff --check` passed.
- Content commit: `4bbbd76453f96b1fbb1929ccc893e178e9e6beba`. Next eligible card: zero-based index 80, which remains `needs_revision`; indexes 81 and 82 also need revision. Record this checkpoint, push it with the content commit, and verify the remote ref before continuing.

## Active continuation — 2026-10-30, empty chair and “加一” callback batch 70

- Continued in the independent worktree after the batch 69 recovery checkpoint; the Desktop repository remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 80. At a New Port hotpot meal, Ah Keung reads “加一” on the service-fee line as one extra diner, reserves an empty chair, and searches the order sheet for the imaginary fifth guest. The entrance notice explains the Macau usage; he checks the fee and pays correctly. His friend closes with “張凳走咗，加一都唔會跟住走,” paying off both meanings.
- Compared with approved adjacent indexes 76–79: the extra dim-sum plate, zero-fee/cutlery allocation, weak-signal transfer, and fair late-arrival split use different mechanisms. Reviewed colloquial Cantonese, contextual Jyutping (245 Han/245 syllables; the counting verb 數 is `sou2`), complete Simplified Chinese gloss, and story-specific practice tip.
- Rebuilt the app mirror and confirmed exact sentence, Jyutping, gloss, and tip agreement; metadata is `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`. `python tools/validate_content.py` validated 8,000 entries; `python tools/story_quality_progress.py --output STORY_QUALITY_CHECKLIST.md` reports 1,698 pass / 3,302 needs_revision / 0 pending; `git diff --check` passed.
- Content commit: `2060e929c04ee8b4597441b3184571c0c06c956c`. Next eligible card: zero-based index 81, still `needs_revision`; index 82 also needs revision. Continue the complete 5,000-card review.

## Active continuation — 2026-10-30, misplaced shrimp-ball receipt callback batch 71

- Continued in the independent worktree after batch 70; the Desktop repository remains untouched.
- Reworked `content/sentence_bank/long_food_shopping_01.json` zero-based index 81. Four coworkers find an unserved shrimp-ball charge, check meal photos and ask the cashier to verify the order. A one-digit table-selection error sent the dish to the neighboring table and its charge to theirs; the manager removes the wrong item and reprints the receipt before they pay. The shrimp ball becomes an imaginary “coworker” who clocked in at two tables, then the group-chat line closes the callback.
- Compared with approved index 76 (a delayed repeat order that produced an extra plate at this table): this card has no extra dish delivered here; it concerns a mistaken POS table number and a charge corrected before payment. Also screened approved indexes 77–80 (cutlery/zero fee, transfer signal, fair late-arrival split, and the service-fee/empty-chair misunderstanding). Reviewed colloquial Cantonese, contextual Jyutping (275 Han/275 syllables; 名=`ming4`, 店長 長=`zoeng2`), complete Simplified Chinese gloss, and event-specific practice tip.
- Rebuilt the app mirror and confirmed exact sentence, Jyutping, gloss, and tip agreement; metadata is `entryType=sentence`, blank `exampleSentence`, and `qualityPriority=1`. `python tools/validate_content.py` validated 8,000 entries; `python tools/story_quality_progress.py --output STORY_QUALITY_CHECKLIST.md` reports 1,699 pass / 3,301 needs_revision / 0 pending; `git diff --check` passed.
- Content commit: `9c34a6d2bcd648de060c3e1f5a67a74345efa635`. Next eligible card: zero-based index 82, still `needs_revision`; continue the complete 5,000-card review.

## Active continuation — 2026-10-30, watermelon office-new-hire callback batch 72

- Resumed from the verified remote `codex/macau-story-upgrade-batch-progress-resume` at `2a96b67ba34059e05750a2a5c9296c786b9562fa`; this branch is 112 commits ahead of and 0 behind the current original goal branch at `3839000bf6829de38abb3027a48174b2c00cd83`. Continued only on `-resume`; did not sync the original goal branch.
- Preserved the older dirty checkout unchanged at `/workspace/jyut-soeng`. Exported its four protected uncommitted files into `/workspace/jyut-soeng-protected-local.patch`; verified `git apply --reverse --check` and SHA-256 `7133402e9718b4fbac1f912ec40f50cfe1055b21383c3d3db7d6a7346d0e86f7`. The four paths remain uncommitted in the older checkout, not included in this worktree.
- Rewrote `content/sentence_bank/long_food_shopping_03.json` index 82 (`食物保存與過敏`) as a nonfamily office snack story. A missing cut-fruit date keeps the coworkers from opening it; one colleague gives the “watermelon new hire” an employee badge, chair, and afternoon-tea roll-call entry; after verifying the store record and exchanging it, the group fills in its expiry date and collects its badge, ending on the fruit’s one-day resignation / clock-out callback. Food remains sealed until verification and cold-storage reminders are explicit. Distinct from the family leftover-watermelon story in `long_food_shopping_02[140]`; the new plot is labeling and workplace onboarding wordplay.
- Reviewed all four fields. Body is 257 Han / 257 Jyutping syllables, `audit()` returns no failures, glossary and tip match, V2 row hash is `a1694cb77db6754d0cb1df1ef2cb74df8be051acb40578a6ea640c4aa6823523`. Rebuilt the app asset; its matching entry `sentence-bank-long_food_shopping_03-0083` matches sentence, Jyutping, gloss, tip, and category. Only that entry changed in `content.json`.
- `python tools/validate_content.py` validated 8,000 entries; progress helper/checklist succeeds at 1,700 pass / 3,300 needs_revision / 0 pending; `git diff --check` passed. Next card in this file is index 83 (`needs_revision`); screen for family-centered content and semantic overlap before rewriting.

## Active continuation — 2026-10-30, “走糖／走單” tea-shop callback batch 73

- Continued after verified `-resume` commit `8971fbf9d5102b5a09af3b2ef7d6c6898a487d3d`; the original goal branch remains untouched and has not been synchronized.
- Screened `long_food_shopping_03[83]` and skipped it because its office-food registration/employee gag substantially overlaps batch 72; `[84]` is family-centered; `[85]` is a repetitive expired-promotion price dispute; `[91]` foregrounds a buyer’s daughter and a routine secondhand bag inspection. These rows were not counted as passes.
- Rewrote `content/sentence_bank/long_food_shopping_04.json[34]` (`茶餐廳`) as a nonfamily tea-shop dialogue. “走糖” is mistaken for sugar that has disappeared, nearby customers check their cups, and the customer asks if the sugar jar is registered; the waiter nearly relabels it “走單,” leading to the paid/not-left callback. Distinct from the previous watermelon date / office onboarding story. No safety issue; one customer is explicitly offered a sip.
- Reviewed all four fields and contextual Jyutping, including `認真` = `jing6 zan1`; 266 Han / 266 Jyutping, `audit()` empty. Gloss and story-tip match; row hash `bc396b0eab65fe49410c3d599cd39d326fcf068c5b111c3e745035b0fc7572f6`.
- App asset regenerated; `python tools/validate_content.py` validated 8,000 entries; progress helper/checklist succeeds at 1,701 pass / 3,299 needs_revision / 0 pending; `git diff --check` passed. App entry should mirror source fields. Next plausible nonfamily rewrite: `long_food_shopping_04[40]` (coworker salad lunch), after screening for a substantially different comic mechanism. Avoid the family-centered rows 35–39.

## Active continuation — 2026-10-30, salad dressing arrives before lunch batch 74

- Continued from pushed `-resume` SHA `baade596339364b6861665407434a92ef6de514d`; original goal branch remains untouched.
- Rewrote `content/sentence_bank/long_food_shopping_04.json[40]` (`超市購物`) as a nonfamily coworker lunch: after a store exchange for leaking dressing, coworkers treat the wet bag as having eaten before the salad, mark it “already served,” ask whether it wants corn, and stop the narrator from feeding it again. The joke escalates through the actual lunch setup, separate dressing, and cleanup; distinct from the watermelon date label and “走糖” wordplay. Body 233 Han / 233 Jyutping; all four fields reviewed; row audit empty; hash `e55a23c027a0e2d063998af9b78934745b3a0c45bdaa5f365127f58aa64f2e73`.
- Rebuilt assets and validated 8,000 entries; quality progress and checklist report 1,702 pass / 3,298 needs_revision / 0 pending; `git diff --check` passed. App mirror verification and remote push still to complete for this batch.
- Next rows 41 and 42 are family-centered and should remain untouched. Index 43 is a friend picnic with nut-allergy precautions; maintain explicit cross-contact caution and do not create unsafe advice if selecting it. Continue screening for nonfamily variety and semantic overlap.

## Remote comparison correction and active continuation — 2026-10-30, queue-slip chase batch 75

- **Correction to earlier checkpoint statements:** the earlier “112 ahead” and “115 ahead” figures used a stale local `origin/codex/macau-story-upgrade-batch-progress` tracking ref at `661226fab3c703078bc7f6075df04358a46b9cf9`. After fetching both exact remote branch heads, the original goal is `3839000bf6829de38abb3027a48174b2c00cd83d` and `-resume` was `708d032a707fd5d0b4370e54e3ff4a768ba6ac6c`; `git rev-list --left-right --count target...resume` reports `0 33`. Thus the handoff’s ahead-30 comparison was the correct order of magnitude; current resume has three more commits since that snapshot. The original branch has not been changed.
- Continued from that clean, verified `-resume` head. Rewrote `content/sentence_bank/long_health_services_01.json[65]` (`辦證服務`) as a nonfamily service-center scene. A freshly printed queue slip is blown across the hall; the narrator chases it, several people mistake the chase for a called number and queue behind, then the friend closes with “we were chasing one piece of paper.” They reach the correct counter and keep the slip pinned down. The plot uses a human queue misunderstanding, distinct from the prior food/object jokes. No concrete legal or government procedure is asserted.
- Read all four fields, retained category, and checked contextual Jyutping. 235 Han / 235 syllables; audit empty; V2 hash `38d7c9cccc17948248b14a36c717c92581a5ac4cfe4df92d5411dc0cb3f9524e`. The app entry `sentence-bank-long_health_services_01-0066` matches sentence, Jyutping, gloss, tip and category.
- After saving, V2 progress is 1,703 pass / 3,297 needs_revision / 0 pending. `build_assets.py`, `validate_content.py` (8,000 entries), progress helper/checklist and `git diff --check` pass. Push and post-push branch verification pending.

## Active continuation — 2026-10-30, roommate shoe-cabinet obstacle callback

- Continued from verified remote `5dbfd7084f6345405a5a2b37991f0872e19816d2` in the isolated `-resume` worktree. The original target branch remains `3839000bf6829de38abb3027a48174b2c00cd83d`; exact comparison at the previous checkpoint was target...resume = `0 34`. The old ahead-115 reading came from stale local tracking and is not used.
- Reworked `content/sentence_bank/long_home_family_01.json` zero-based index 29 (category `租屋`, roommate plot). The paper shoe-cabinet mock-up exposes the unmeasured door handle; a mistakenly oversized delivery is verified against the order and exchanged; next morning the roommate leaves slippers in the path, and the narrator jokes that the new cabinet cannot fix the roommate's habit of leaving shoes out. The close resolves the obstacle course by having the roommate put them away. No family-centered story or category metadata change.
- Compared against adjacent rental stories in the same source and phrase searches in the sentence bank; the physical doorway measurement / repeated shoe-leaving callback differs from the nearby suction-rack and chore-chart stories. Manually reviewed colloquial Cantonese, contextual Jyutping (229 Han / 229 syllables), full Simplified Chinese gloss, and `故事练习：` retelling tip. Source and app mirror fields match exactly; non-language metadata retained.
- Updated both review ledgers with the current source hash and a V2 pass only after the four-field read. `python3 tools/build_assets.py`, `python3 tools/validate_content.py` (8,000 entries), `python3 tools/story_quality_progress.py --output STORY_QUALITY_CHECKLIST.md`, and `git diff --check` passed. Progress is 1,704 pass / 3,296 needs_revision / 0 pending.
- This worktree's only intended content delta is this card and its review/checkpoint assets. Next action: commit and normally push only to `codex/macau-story-upgrade-batch-progress-resume`, verify the exact remote SHA and unchanged target ref, then continue from a new non-family candidate. Original dirty checkout and protected patch remain untouched.

## Audit correction and active continuation — 2026-10-30, neighbor water-shutoff / drip-clock story

- Reconciled the pass-count concern from a verified commit-by-commit read: parent `708d032` was 1,702/5,000; `5dbfd7084f6345405a5a2b37991f0872e19816d2` changed only the reviewed V2 status/hash for `content/sentence_bank/long_health_services_01.json` index 65 (1,703); `9443d4b122a6edeb37d3f6eedf9510926b5e787e` then changed only the reviewed V2 status/hash for `content/sentence_bank/long_home_family_01.json` index 29 (1,704). Both rows have distinct source hashes and semantic notes. No other pass was added between those exact commits.
- The index-29 row's original category is `租屋`, and its original sentence already concerns roommates jointly measuring a shoe cabinet; the V2 revision retained the category and remained a roommate/home logistics plot, not a family relationship plot. It is compatible with the user's no-family-core instruction and was not a relabeling workaround.
- Exact live target comparison before this next card: target `3839000bf6829de38abb3027a48174b2c00cd83d` ... resume `9443d4b122a6edeb37d3f6eedf9510926b5e787e` = 0/35, with merge base equal to the target SHA. The earlier ahead-115 figure came from stale local tracking and is corrected; the original target branch remains untouched.
- Reworked `content/sentence_bank/long_home_family_01.json` zero-based index 56, category `鄰里`. The neighbor gives advance water-storage advice; the narrator labels buckets by use. A leak before the planned stoppage leads to safely closing the tap valve and contacting management; the neighbor's metal basin makes the drips sound like a clock, a plastic basin becomes the “silent alarm,” and the repaired leak “resigns” before the phone alarm takes over. The neighbor relationship and property-maintenance scenario fit the retained category and do not center on family.
- Manually reviewed all four fields: 270 Han characters / 270 contextual Jyutping syllables, complete Simplified Chinese gloss, and exact `故事练习：` retelling tip. The pronunciation-to-character alignment was checked manually; source and generated app mirror match exactly, with all non-language metadata preserved. `build_assets.py`, `validate_content.py` (8,000 entries), `story_quality_progress.py`, and `git diff --check` passed. V2 progress is 1,705 pass / 3,295 needs_revision / 0 pending.
- Original checkout remains untouched with its four pre-existing modified paths, and protected patch SHA-256 remains `7133402e9718b4fbac1f912ec40f50cfe1055b21383c3d3db7d6a7346d0e86f7`. Next: commit and push this card only to the `-resume` branch, confirm the live SHA and unchanged original target, then continue another non-family card. Goal remains all 5,000 V2 reviews.

## Active continuation — 2026-10-30, second-hand insulated lunch-bag interview callback

- Continued from verified `-resume` tip `47f4243868892881efedc20a649df8879cca33c5`; original goal branch stays untouched at `3839000bf6829de38abb3027a48174b2c00cd83d`.
- Reworked `content/sentence_bank/long_food_shopping_03.json` zero-based index 91, retained category `二手交易`. The buyer is a neighbor choosing a used bag for her own lunch, not a family-centered plot. Her prior experience of lingering fish smell and a jammed zipper motivates several checks; rain prompts a joking “waterproof test,” which the seller corrects because this bag is not waterproof. They discover a loose corner seam, pause the exchange, the seller goes home for a sewing kit and repairs it, then the buyer tests the zipper and lunch-box fit. The final “bag interview” line pays off the staged inspection, with the buyer admitting she still has to pass the daily test of remembering her lunch.
- Fixed the source's prior “unopened set” versus chipped bowl inconsistency indirectly by using a different candidate; no edits to other cards. Compared the mechanism with approved second-hand juicer/photo, used-coat pocket reminders, and food-bag spill stories; the testing progression, rain misinterpretation, disclosed repair, and interview callback differ.
- Four-field manual review: 254 Han / 254 context-matched Jyutping syllables, Simplified Chinese gloss, and personalized tip beginning exactly `故事练习：`. Source/app mirror fields and category match; metadata retained. `build_assets.py`, `validate_content.py` (8,000 entries), `story_quality_progress.py`, and `git diff --check` passed. V2 status now 1,706 pass / 3,294 needs_revision / 0 pending.
- Next: commit and push to `codex/macau-story-upgrade-batch-progress-resume`; verify live remote SHA and unchanged goal branch. Continue non-family candidates, skipping family-centered content and semantically overlapping plots. Preserve the original checkout and its protected patch.

## Post-commit verification — 2026-10-30

- Card index 91 is committed as `28d56fdac35e2d06a932839de02408d8961d052f` (`Turn lunch bag resale into a product interview`) and pushed to the `-resume` branch; `git ls-remote` returned the same SHA. The target branch is still `3839000bf6829de38abb3027a48174b2c00cd83d`; exact target...resume comparison is 0/37, merge base equals target. Worktree clean.
- V2 status: 1,706/5,000 pass, 3,294 need revision, 0 pending. Overall mechanical audit is 5,000/5,000 and is not semantic approval. Content build and 8,000-entry validation passed.
- Protected original checkout remains untouched with its same four modified paths; protected patch SHA-256 remains `7133402e9718b4fbac1f912ec40f50cfe1055b21383c3d3db7d6a7346d0e86f7`.
- Next card not yet selected. Avoided `long_food_shopping_03.json` index 32 (office croissant sharing resembles approved `long_food_shopping_06.json` index 45) and `long_food_shopping_04.json` index 74 (price-label inspection overlaps index 81); also screened herb-exchange candidates against an existing family-centered balcony-herb plot. Select a fresh needs-revision row whose category and actual plot support a non-family story, compare plot/relationship/conflict/payoff with existing cards, then continue the 5,000-card V2 goal.

## Active continuation — 2026-10-30, salmon-skin map callback

- Continued from clean remote/checkpoint commit `e838db57abe35b8a7b43813514d1831570b463f1`; original target remains at `3839000bf6829de38abb3027a48174b2c00cd83d`.
- Reworked `content/sentence_bank/long_food_shopping_06.json` zero-based index 55 (category `街市買餸`). The fish-market purchase and roommate lunch premise stays within the category. A timed pan turn makes the salmon skin tear into two “islands”; the roommate identifies the peninsula and Taipa, pieces them together, then extends the map joke through new islands, a scallion bridge that breaks when the fish is eaten, and the last distant island disappearing into lunch. The running gag escalates from one shape comparison to a dinner-table map that keeps losing geography.
- Compared against all `地圖` and salmon/fish-skin occurrences in the story corpus; no other card uses this fish-skin / reassembled-island chain. Roommate relation is non-family. Reviewed all four fields, context Jyutping (266 Han / 266 syllables), complete Simplified Chinese gloss and `故事练习：` tip. App fields and metadata match exactly.
- `build_assets.py`, `validate_content.py` (8,000 entries), `story_quality_progress.py` and `git diff --check` passed. V2 progress is 1,707 pass / 3,293 needs_revision / 0 pending. Next: commit/push to `-resume`, verify remote SHA and unchanged target, then continue non-family candidates. Goal remains 5,000.

## Active continuation — 2026-10-30, milk-return evidence lineup

- Continued from clean, verified `-resume` commit `762ce9ff15b2b4cd620feac37238369883b91e79`; live original target remains `3839000bf6829de38abb3027a48174b2c00cd83d`.
- Reworked `content/sentence_bank/long_food_shopping_04.json` index 58 (category `網購退貨`). A pair of leaking cartons prompts the roommate to stage the proof photos like a lost-property lineup; the ruler becomes the host, then the roommate blocks the order number and has to pose as a human scale. At pickup, the courier asks whether anyone else needs returning, paying off the staged “return the roommate” joke. The remaining intact milk is handled according to its label. The plot remains a non-family roommate scene and preserves category and metadata.
- Manually reviewed the four fields and corrected the contextual reading of `助理` to `zo6 lei5`. Body is 246 Han / 246 Jyutping syllables; Simplified gloss and exact-prefix practice tip included. Search found no other use of the lost-property lineup / returning-roommate / scale gag. V2 and language review hashes now match `000385215baab6fddc8724d258d039115e29d853a47a44547e0f7f250782e2c2`.
- `build_assets.py`, `validate_content.py` (8,000 entries), progress/checklist refresh, and `git diff --check` pass. V2 status is 1,708/5,000 pass, 3,292 need revision, 0 pending; mechanical 5,000/5,000 remains only a structural count.
- This checkpoint is awaiting commit/push and live remote verification. Keep original target untouched, preserve the protected four-file checkout and patch, then continue another non-family candidate after verification.

## Pass-count reconciliation — 1705 to 1708

The 1,705 baseline already included `content/sentence_bank/long_home_family_01.json[56]` (neighbor water-leak/drip-clock story; commit `47f4243868892881efedc20a649df8879cca33c5`). The next three unique V2 pass rows account for 1706→1708:

- 1706: `content/sentence_bank/long_food_shopping_03.json[91]` — second-hand lunch bag product interview; commit `28d56fdac35e2d06a932839de02408d8961d052f`.
- 1707: `content/sentence_bank/long_food_shopping_06.json[55]` — salmon-skin Macau/Taipa map callback; commit `762ce9ff15b2b4cd620feac37238369883b91e79`.
- 1708: `content/sentence_bank/long_food_shopping_04.json[58]` — milk-return evidence lineup and roommate “return” callback; commit `64f4288a48e378264265afba672cf679e305df8a`.

The V2 ledger contains one pass record for each row and its current source hash. The mechanical 5,000/5,000 result is not a semantic pass. Current live `-resume` is `64f4288a48e378264265afba672cf679e305df8a`; the original goal branch remains unchanged at `3839000bf6829de38abb3027a48174b2c00cd83d`.

## Active continuation — 2026-10-30, temporary-wallet receipt callback

- Continued after the verified 1,708/5,000 baseline. Reworked `content/sentence_bank/long_food_shopping_01.json[82]`, category `埋單分賬`, as a friends-at-lunch story. The narrator forgets their wallet and has a nearly dead phone; a friend pays, lends a charging cable, and the bank transfer remains “processing.” The friend warns against repeating it, keeps the receipt as the temporary wallet, and the next-day completion message lets the receipt “retire.” This replaces the source’s duplicate convenience-store charging scene with one escalating payment/receipt callback. No family-centered story or category change.
- Compared across the corpus for wallet/transfer-pending/receipt-retirement mechanisms; no other matching plot chain found. Manually reviewed all four fields and Jyutping (229 Han / 229 syllables); Simplified gloss and exact-prefix `故事练习：` tip included. The generated app story entry matches source sentence, Jyutping, gloss, tip, and category; its `exampleSentence` remains empty per the story-entry schema.
- V2 hash: `64053679dffe6d59e52f01ff05a1f6b37c76dff4b372e47ef2cdc8a99961d050`. V2 status is now 1,709 pass / 3,291 needs revision / 0 pending. Mechanical 5,000/5,000 does not replace semantic review.
- `build_assets.py`, `validate_content.py` (8,000 entries), progress/checklist refresh, mirror assertions, and `git diff --check` pass. Commit/push and remote verification pending.

## Active continuation — 2026-10-30, neighborhood orange relay

- Continued from 1,709/5,000. Reworked `content/sentence_bank/long_food_shopping_17.json[6]`, retained category `街坊輪流代買日常食材`. Several neighbors rotate grocery help for an upstairs neighbor with an injured foot. The shared list says oranges are already stocked, but the next helper reads that as a request to replenish; the pile grows. The group labels the oranges “only out, never in,” shares them around, then gets a final callback about planting the seeds. The scene stays community/neighborhood-centered, not family-centered.
- Compared orange references in the story corpus; existing orange scenes do not use this shared-list misunderstanding / return-loop mechanism. Manually reviewed the four fields and contextual Jyutping (240 Han / 240 syllables); full Simplified gloss and exact-prefix practice tip included. Verified `扭 nau2`, `硬 ngaang6`, and `停 ting4`; app entry matches all four language fields and category.
- V2 hash `ce36d737322451fa6ff8fbec9566bd9aa04fe2b827ba7cbe88574ae70fe19ffb`. Current progress is 1,710/5,000 pass / 3,290 needs revision / 0 pending. This is the second new pass after the 1,708 baseline: the prior pass is `content/sentence_bank/long_food_shopping_01.json[82]` (commit `ae9caff86abf70ca70eea8b919edc045d50e2a44`).
- `build_assets.py`, `validate_content.py` (8,000 entries), mirror assertions, quality progress/checklist, and `git diff --check` passed. Push verification pending.

## Active continuation — 2026-10-30, emergency snack politeness loop

- Continued from the verified 1,710/5,000 baseline. Reworked `content/sentence_bank/long_food_shopping_13.json[12]` (`行山前買小食飲品`), retaining the category and friend-group hike. The group passes one wrapped emergency energy bar among their bags because each says to save it for the most tired person; at every rest stop the same “you eat first” answer repeats, so they reach the summit with it still unopened. They share it there and add a rule assigning the bar to whoever first defers. The callback is about polite human deferral, distinct from the work-hike allergen-label plot in `long_food_shopping_18.json[41]` and from the existing sports relay story. Damp crackers are not eaten; they are separately packed and carried down for disposal.
- Four fields manually reviewed; body 279 Han / 279 Jyutping syllables, full Simplified gloss and exact-prefix practice tip. App story entry matches source text, Jyutping, gloss, tip and category; story schema keeps `exampleSentence` empty.
- V2 hash `44e35a3d7e06870f03b636fc1e83ed3262366f7b415cb5431fabf88f68741eff`. Count is 1,711 pass / 3,289 needs revision / 0 pending. `build_assets.py`, `validate_content.py` (8,000 entries), `story_quality_progress.py`, mirror assertion and `git diff --check` passed. Commit/push pending.

## Active continuation — 2026-10-30, remote meeting volume spill

- Continued from 1,711/5,000. Reworked `content/sentence_bank/long_health_services_07.json[1]` (`耳垢清理安排`) into a workplace aftermath while preserving the medical scenario: ENT examination, telling the clinician immediately if treatment hurts, and not using cotton swabs for several days afterward. Since the narrator had raised laptop volume while one ear was blocked, they forget to lower it for a video meeting; coworkers answer a remote colleague’s greeting, and the supervisor calls it a “live audience.” A reminder on the laptop pays off the volume mistake. No family-centered interaction.
- Manually reviewed four fields and contextual Jyutping (238 Han / 238 syllables), full Simplified gloss and exact-prefix practice tip. App entry matches sentence, Jyutping, gloss, tip and category. V2 hash `6568d880f344ba4f9982168b268c316bbbbc8cc3e42e9938708ebb532d636b7e`.
- V2 progress is 1,712/5,000 pass / 3,288 needs revision / 0 pending. `story_quality_progress.py`, `build_assets.py`, `validate_content.py` (8,000 entries), app mirror assertion and `git diff --check` passed. Commit/push pending.

## Active continuation — 2026-10-30, dental appointment roadwork loop

- Continued from the 1,712/5,000 baseline. Reworked `content/sentence_bank/long_health_services_02.json[29]` (`牙科預約`). The clinic moves a cleaning appointment from lunch to afternoon and warns of roadworks; temporary route signs send the narrator back to the same market stall, whose owner recognizes the vegetable bag. The narrator calls to confirm the side-street entrance, reaches the clinic early, and the receptionist’s market question pays off the loop. Keeps the appointment logistics and adds no treatment advice. No family-centered interaction.
- Screened `content/sentence_bank/long_food_shopping_13.json[9]` but skipped it: its spicy/mild hotpot and roommate-preference plot closely overlaps `long_food_shopping_14.json[9]`; no edit or pass counted for the skipped card.
- Manually reviewed all four fields and contextual Jyutping (226 Han / 226 syllables), full Simplified gloss and exact-prefix practice tip. App story entry matches sentence, Jyutping, gloss, tip and category. V2 hash `77bba79bff50d2fb235c2eaa6b9872015880b48e40f724b19933568cf29f6e7e`.
- V2 progress is 1,713/5,000 pass / 3,287 needs revision / 0 pending. `story_quality_progress.py`, `build_assets.py`, `validate_content.py` (8,000 entries), mirror assertion and `git diff --check` passed. Commit/push pending.

## Active continuation — 2026-10-30, spare chopsticks mistaken for an invitation

- Continued from the verified 1,713/5,000 baseline. Reworked `content/sentence_bank/long_food_shopping_01.json[25]` (`外賣訂餐`). In the rain, the delivery rider cannot find the entrance and offers a napkin; back at the door, the narrator finds an extra pair of chopsticks. An upstairs neighbor mistakes them for an invitation and brings a dish; a second neighbor follows the food smell to borrow chopsticks. The line “筷子夠，凳就要自己拎” pays off the growing dinner group. Preserves the warm delivery/neighbor beat without family-centered interaction or category changes.
- Searched for repeated extra-chopstick/invitation or neighbor-join-meal mechanisms; no matching plot chain found. Manually reviewed all four fields and contextual Jyutping (273 Han / 273 syllables); full Simplified gloss and exact-prefix practice tip. App entry matches sentence, Jyutping, gloss, tip and category. V2 hash `018f3ad5bd878aaca53c2d0642be080a0ae72b3870ce7eed512759a0b42bedfa`.
- V2 progress is 1,714/5,000 pass / 3,286 needs revision / 0 pending. `story_quality_progress.py`, `build_assets.py`, `validate_content.py` (8,000 entries), app mirror assertion and `git diff --check` passed. Commit/push pending.


## Active continuation — 2026-10-30, lunch receipt shareholders meeting

- Continued from the verified 1,714/5,000 baseline and selected `content/sentence_bank/long_food_shopping_01.json[83]` (`埋單分賬`), a non-family colleague lunch. The earlier split between meat/vegetarian dishes and individually named drinks, a tofu mix-up, and a missed tea charge formed a routine accounting chain. Reworked the payoff: new colleague 阿美 draws a seat chart to trace the tea; the waiter asks whether they are eating or holding a shareholders’ meeting, and 阿明 appoints her chairperson to approve future tea. Preserves the colleague setting and category.
- Manually reviewed all four fields and the new Jyutping. Body is 273 Han characters / 273 Jyutping tokens; Simplified gloss is complete, usage tip has the exact `故事练习：` prefix. V2 hash `08d5140b291f7355eb9f64099e0b0ce03c300564f3ea8c1ee2a2d489706bfe3d`.
- Also corrected the previous checkpoint’s `long_food_shopping_01.json[25]` character/syllable note from 273/272 to 273/273; no story content changed.
- Current ledger progress: 1,715/5,000 semantic passes; 3,285 need revision; 0 pending. `story_quality_progress.py`, `build_assets.py`, `validate_content.py`, mirror assertions, and `git diff --check` are to be rerun before commit. Current branch remains `codex/macau-story-upgrade-batch-progress-resume`; original branch is protected and untouched.


## Active continuation — 2026-10-30, thermos leak false alarm

- Continued from 1,715/5,000 and reworked `content/sentence_bank/long_food_shopping_02.json[59]` (`日常退換貨`), a non-family coworker story. The replacement thermos had passed an upside-down test, but the bag was still wet the next day. A second shop check shows the cup is dry; opening the bag lining reveals tea left from the first leak. The reveal repairs the cause-and-effect; after the bag dries, the paper towels “finally get off duty.”
- Manually reviewed all four fields and contextual Jyutping; 230 Han characters / 230 syllables, full Simplified gloss and exact `故事练习：` tip. V2 hash `eeac99860c9ac963f1fe89b31e98dc764c92790afd54f8c20287a57426d0b186`.
- A first bookkeeping-script attempt did not persist its in-memory edits; progress validation correctly caught the stale hash. No ledger-only change was made. The corrected write persisted source and ledgers, and their hashes now match. Current expected progress is 1,716/5,000; checks and push pending.


## Active continuation — 2026-10-30, picnic cucumber escape

- Continued from 1,716/5,000 with `content/sentence_bank/long_food_shopping_02.json[65]` (`日常退換貨`), non-family friend picnic. Kept the safe return of an unused chipped glass box and the store clarification that the rough spot was folded protective film. Strengthened the loose cucumber at the picnic into the punchline: the lunchbox is securely sealed, yet the cucumber slips away while the lid is open; friends joke that next time the food must be counted before lunch.
- Manually reviewed four fields and Jyutping; 229 Han characters / 229 syllables, complete Simplified gloss and exact `故事练习：` tip. Hash `b77635af8180d9cc28b93239c29848fb3199c9dd94bf6450041602830606ff29`. Current expected progress 1,717/5,000; build, validation, commit and push pending.


## Active continuation — 2026-10-30, croissant applause mix-up

- Continued from 1,717/5,000. The next ledger row `long_family_finance_services_06.json[61]` is explicitly a father/parents retirement-payment scene, so skipped it without edits or counting. Selected `content/sentence_bank/long_food_shopping_03.json[32]` (`麵包店`), a non-family coworker tea break. Reworked it so coworkers eat crisp croissants during a video meeting; the remote team mistakes the pastry crunch for applause, and the late coworker triggers a second “unanimous vote” mishearing. A corpus search found a separate watch-ticking story with applause, but its plot is a household’s interrupted listening attempt, not a food-noise/meeting misunderstanding.
- Manually reviewed all four fields and contextual Jyutping; 248 Han characters / 248 syllables, complete Simplified gloss, exact `故事练习：` tip. V2 hash `f2d8e301e5a50216ef239b30c7404403dfe8503cb49bf2fd3f9c6ca03c20bca0`. Current expected progress 1,718/5,000; validation and push pending.


## Active continuation — 2026-10-30, noodle bowl version testing

- Continued from 1,718/5,000 with `content/sentence_bank/long_food_shopping_03.json[46]` (`辦公室午餐`), non-family coworkers. Kept the request for pickled greens on the side and made 阿健’s gradual additions build into a software-testing bit: he records each portion, calls the meal “still in the test version,” then asks the shop to stamp “version one” while they have eaten only half the bowl. Removed unrelated frozen-soymilk and restaurant-recommendation beats. No health/safety claims added.
- Manually reviewed all four fields and Jyutping; 252 Han characters / 252 syllables, complete Simplified gloss and exact `故事练习：` tip. Hash `f5d74765780704aa68cc7a9c6c5edd7593bbd4ae54c746219f4d5c9b2906d844`. Current expected count 1,719/5,000; checks and push pending.


## Active continuation — 2026-10-30, coffee identity meeting

- Continued from 1,719/5,000. The next ledger card `long_family_finance_services_06.json[61]` is a parents/pension story and remains skipped per the no-family constraint. Reworked `content/sentence_bank/long_food_shopping_04.json[18]` (`茶餐廳外賣`), a non-family coworker coffee pickup. A same-name order swaps hot/cold labels; the coworker buys egg tarts while they wait, then writes a name-plus-temperature check into the meeting record. The manager changes the agenda to “drink identity check,” and the button is that the coffee never attended the meeting, but the team held another meeting for it.
- Manually reviewed all four fields and Jyutping; 309 Han characters / 309 syllables, full Simplified gloss, exact `故事练习：` tip. V2 hash `5c561943794ef5f12ea2b1a7bb3631ed89b887a947e49eacbe01b83cf2d09e98`. Build/validation passed; current expected count 1,720/5,000. Commit and push pending.


## Active continuation — 2026-10-30, second-hand cooker pop-up demo

- Continued from 1,720/5,000 with `content/sentence_bank/long_food_shopping_04.json[28]` (`二手交易`), a non-family sale. The mall outlet fails, so security sends buyer and seller to a second test area. The working cooker attracts waiting customers asking model/capacity questions; seller and buyer answer together, turning the check into an impromptu product launch. The guard’s explicit “when is the next launch?” gets the new-teapot callback. Keeps a small-water test only, no unsafe use advice.
- Manually reviewed all four fields and contextual Jyutping; 224 Han characters / 224 syllables, complete Simplified gloss and exact `故事练习：` prefix. Hash `4caecf9552d892436fb0121504119e7a4698b92e456d0edf74c4d87e340d96df`. Current expected progress 1,721/5,000; validation passed, commit/push pending.


## Active continuation — 2026-10-30, early guest as an ingredient

- Continued from 1,721/5,000. Skipped the next allergy-centered needs-revision cards rather than deriving jokes from safety precautions. Reworked `content/sentence_bank/long_food_shopping_04.json[85]` (`煮食`), a friend dinner, not family-centered. The host runs out of honey and improvises lemon-herb wings; the friend arrives early, the wings dry at the edges and are rescued. When asked for the recipe, the friend lists his own early arrival as an “ingredient,” then asks whether coming an hour early earns two more wings; the host’s heartbeat callback pays off the rushed cooking. Corpus comparison found similar chicken-wing/honey props, but no matching missing-ingredient/early-guest recipe-misclassification plot.
- Manually reviewed all four fields and contextual Jyutping; 279 Han characters / 279 syllables, complete Simplified gloss and exact `故事练习：` prefix. V2 hash `bd864cb3907e3dcd1e3ae81b7738dbb99ec26cc4d9795b2600c780d725cb2e8a`. Build and 8,000-entry validation passed. Current expected progress 1,722/5,000; commit/push pending.


## Active continuation — 2026-10-30, friend dinner and kite-line delivery

- Continued from 1,721/5,000 with two distinct non-family scenes. `content/sentence_bank/long_food_shopping_04.json[85]` (`煮食`): a friend’s early arrival becomes an “ingredient” in an improvised lemon-herb chicken-wing recipe; he asks whether arriving an hour early earns two extra wings, and the host’s heartbeat line callbacks to the rushed cooking.
- `content/sentence_bank/long_food_shopping_05.json[2]` (`外賣溝通`): a wind-blown balloon line tangles a borrowed umbrella while a courier and customer protect two milk teas; the line remains on the umbrella until return, where the front desk’s “umbrella or kite frame?” question leads to a second untangling. A corpus search found a family story with an umbrella flipped by wind and a keepsake ticket; this rewrite avoids that mechanism and has no family-centered plot. Allergy-centered candidate cards were left unchanged.
- Both cards manually reviewed across all four fields and contextual Jyutping. Card 85: 279 Han / 279 syllables, hash `bd864cb3907e3dcd1e3ae81b7738dbb99ec26cc4d9795b2600c780d725cb2e8a`. Card 05[2]: 288 Han / 288 syllables, hash `26a14cdcd1d5e1a4c8bd264b3a4194ed858fc85375d4614eaddacc57c6b75532`. Current ledger progress 1,723/5,000; build and validation passed, commit/push verified in the following commit.

## Active continuation — 2026-10-30, collecting the sauce literally

- Continued from the verified 1,723/5,000 V2 baseline. `long_food_shopping_01.json[16]` was skipped without edits because it is a family-centered peanut-allergy scene. `[21]` was screened and left needs_revision because its leaking-bag/map stain gag would repeat an approved curry-leak/map story. The bill-splitting rows `[84–89]` were screened; they repeat account-correction or birthday/allergy mechanisms and were not counted.
- Reworked `content/sentence_bank/long_food_shopping_01.json[43]`, retained category `煮食日常`, into a non-family community cooking-class scene. 阿晴 takes 「收汁」 literally and fills a measuring cup; classmates mistake it for a drink, the instructor restores the sauce, and the 「收火」 callback has her point to the stove switch. This develops one escalating verbal misunderstanding without family interaction or the previously repeated office-agenda/product-launch pattern.
- Manually reviewed the Cantonese story, contextual Jyutping one character at a time, complete Simplified gloss, and `故事练习：` usage tip. Body 243 Han characters / 243 Jyutping syllables. V2 hash `75a1bcac91ff15786c1a29f447bf550cdabeab7d216730ed0bd34c70fd931844`.
- Ledger now records 1,724/5,000 pass, 3,276 needs revision, 0 pending. Refreshed progress checklist, rebuilt assets, validated all 8,000 entries, ran tools unit tests (7 run, 1 skipped), and `git diff --check`; all passed. This one-card batch is saved locally; commit/push pending.

## Active continuation — 2026-10-30, chestnut-stall self-appointed inspector

- Rechecked `content/sentence_bank/long_food_shopping_02.json[69]` (`超市買嘢`) after the category-fit instruction. The supermarket visit is only a brief setup; the central action and punchline occur at a badminton court, so it does not sufficiently fulfill the category. Reclassified it to `needs_revision`, preserving its current row and hash `129e03365011eaa2442f1b5908c799ab2a566e2523f78444a2ed7aea1eaee21a`. Do not count it again unless rewritten around shopping.
- Reworked `content/sentence_bank/long_food_shopping_03.json[17]` (`街頭小食`) as a non-family street-stall story: a friend claims to buy the smallest portion, appoints himself chestnut inspector, draws a queue with absurd “試食要先買栗子” signage, eats the bag during “inspection,” then asks for a large portion. The central comic escalation remains at the chestnut stall and the closing contradiction pays off the small-portion setup. Preserved category and other row metadata.
- Manually reviewed all four content fields for the new card. Sentence has 231 Han characters and Jyutping has 231 tokens; source-row hash `d345e49d648e3d200093edc0330529d47ce3d252d957949752806fa735d2e06e`. Simplified gloss is complete; usage tip starts exactly `故事练习：`. Exact distinctive-phrase and chestnut/food-review searches found no same mechanism in the corpus.
- Also reworked `content/sentence_bank/long_food_shopping_03.json[71]` (`餐廳訂位`) around six coworkers whose common booking name “阿明” matches two other parties. Simultaneous responses lead the host to nearly merge groups, restaurant staff relabel the tables 明一/明二/明三, and the friend ends up better known by his phone-number suffix. This is a distinct reservation-name collision, not another food-inspection/queue story. Preserved the restaurant-reservation category. Manually reviewed four fields and contextual Jyutping; 257 Han characters / 257 syllables, source hash `0070c36be94b5062a05857f0d3dcb3c015d886abddb45b49a592add5968121a`; full Simplified gloss and exact practice-tip prefix. Corpus search found no same multi-party name-collision mechanism.
- Screened `long_food_shopping_03.json[11]` and `[23]` without edits because their current versions center a parent-child snack outing and a sibling-led pickle-sharing scene; continued to a roommate/neighborhood card instead of adapting either family-centered setup. Reworked `content/sentence_bank/long_food_shopping_03.json[25]` (`鄰里共享食物`) around a leaking meal box that prompts a borrow-and-return food relay among neighbors. Each return adds another dish, a sign assigning box-washing is changed to “加菜,” and Chen asks whether his latest dish violates the “no more dishes” sign. The food-sharing and neighbor exchange remain central; no family roles or metadata were added. Manually reviewed all four fields and Jyutping: 269 Han characters / 269 syllables, hash `6eed889cff34c9e8a02268966b334d62d464031b74de4462fe755503ae2869e4`; complete Simplified gloss, exact tip prefix, category unchanged. Distinctive phrase search found no exact relay/sign match; compared with existing neighbor-food stories, whose mechanisms are a corridor-serving queue and a rooftop tomato-dessert stall, and found no same container-relay progression.
- Cross-card re-audit withdrew `content/sentence_bank/long_food_shopping_03.json[25]` from pass. Compared with `long_food_shopping_17.json[6]`, both center a neighbor food-transfer cycle that accumulates food across households and ends with a corrective rule/sign plus a continuing-loop joke. Their immediate triggers differ (borrowed container relay vs. duplicated orange shopping), but that central circulation-and-rule payoff is too close to count as distinct. Card `[25]` remains unchanged and needs revision; its current hash still matches the ledger.
- Reworked `content/sentence_bank/long_home_family_01.json[32]` (`租屋`) as a non-family pet-rental story: a landlord worries about wall scratches, but the cat ignores its scratch board, dismantles cardboard boxes, and leaves the walls untouched. The monthly box callback culminates in the landlord asking about the extra cardboard; the narrator calls it the cat’s move-out report. Preserved the category and other row metadata. Manually reviewed all four fields and Jyutping: 246 Han characters / 246 syllables, source hash `2b734211f9003811e806795bb33eaa5837e3d6030a5dd6f082729fb62bcd73bc`; complete Simplified gloss and exact tip prefix. Search found no matching rental inspection/cat-box mechanism.
- Current unique V2 count is 1,727/5,000 pass, 3,273 needs revision, 0 pending. This turn withdrew `[25]` and added `[32]`, for net change 0; `[17]` and `[71]` remain pass. Card `[69]` stays needs_revision and its current sentence has 254 Han characters but only 252 Jyutping tokens, so do not treat it as aligned or approved. The checklist was regenerated; assets rebuilt with 8,000 entries, with `[32]` receiving `qualityPriority=1` and `[25]` no longer marked priority. `validate_content.py`, tools unit tests (7 run, 1 skipped), and `git diff --check` passed. `--require-complete` is not applicable until all 5,000 are reviewed.
- Before this checkpoint correction, `-resume` remote was `c9cb82adcde45f4934e6ea95e02a756bdaa48775`; original branch remains at `3839000bf6829de38abb3027a48174b2c00cd83d` and is untouched.


## Active continuation — 2026-10-30, west-facing rental room

- Continued from the verified resume branch at `6cda8e7e8b1b78467952925deafee1ccce4e9424`; remote and local matched before editing. Original target branch remains untouched.
- Reworked `content/sentence_bank/long_home_family_01.json[27]` (category `租屋`) as a non-family roommate story. A west-facing room melts the desk chocolate and triggers a phone overheat warning; a cardboard shade makes the roommate chase the moving patch of shadow into the hallway; a removable shade resolves the heat, and the chocolate callback closes the scene. The previous version's curtain purchase/ordinary relief was marked needs-revision; the new version gives the same rental setting an escalating physical comic sequence.
- Screened approved stories for west-facing sunlight, curtains, window glare and related room-heat scenes before writing; no same plot chain found. Manually reviewed sentence, contextual Jyutping, complete Simplified Chinese gloss, and `故事练习：` tip. 237 Han characters / 237 Jyutping tokens. Source row hash: `c83ed0ca06767a42f8209e4985505c2e17968f1aa3202ed90643d6ab01972c1d`. Category, identity, order and non-language metadata preserved; generated app entry matches all four fields and has `qualityPriority=1`.
- V2 ledger now records 1,728 pass / 3,272 needs revision / 0 pending, a net +1 this continuation; no other IDs added or withdrawn. The previously identified `long_food_shopping_02.json[69]` remains needs_revision and untouched.
- `tools/build_assets.py`, `tools/validate_content.py` (8,000 entries), unit tests (7 run, 1 skipped), checklist refresh, source/app mirror assertions and `git diff --check` passed. The task remains incomplete; continue from the next eligible distinct non-family card.

## Active continuation — 2026-10-30, community meal-service feedback card

- Continued from a clean, remotely verified resume-branch baseline `06e98538e75b60909bb70b80bd38b4e7c2184e38`; original target branch and the protected original checkout remain untouched.
- Reworked `content/sentence_bank/long_health_services_01.json[81]`, retaining category `公共服務` and the neighbor / community meal-delivery setting. A weekly menu and first delivery preserve the concrete setup; after the elevator breakdown delays delivery, the center's one-smiley callback card cannot distinguish the meal, delivery and staff. Chen draws separate ratings and says she will not make one smiley apologize for the elevator; the center adds separate fields, and her Wednesday soup rating callbacks to the menu. No family-centered plot, category change, or safety/medical claim.
- Compared approved meal-delivery and food-feedback entries; none shares the form-rating / elevator-apology plot chain. Manually reviewed all four source fields and context-specific Jyutping. After a second semantic pass, clarified that Wednesday is the listed fish/vegetable/soup menu day, tightening the setup/payoff. Final sentence: 300 Han characters / 300 Jyutping tokens; gloss is complete Simplified Chinese; tip begins exactly `故事练习：`. Final V2 source hash `2bfcae965b63ab6b226e47a4fc4acd5346d4c83d8fc7c70a9744b4697fbcc9e6`. Rebuilt and reverified exact four-field app mirror, retained category, generated ID and `qualityPriority=1`; assets, 8,000-entry validation, tests (7 run, 1 skipped), and `git diff --check` passed again.
- V2 ledger is now 1,729/5,000 pass, 3,271 needs revision, 0 pending; one unique pass added, no withdrawals. Checklist refreshed; `build_assets.py`, 8,000-entry `validate_content.py`, unit tests (7 run, 1 skipped), and `git diff --check` passed. Continue with an eligible non-family work/school/travel/public-service category after a fresh plot comparison; skip family-centered or category-conflicting rows. This checkpoint is not task completion.
- Follow-up candidate screen (no edits or counts): the visible school-communication rows in `long_health_services_01.json[50–57]` center on a parent and child; transport/support candidates in `long_family_finance_services_09.json[80,82,83,86,87,89]` and `long_health_services_02.json[62]` are likewise family-centered. `long_health_services_03.json[27]` is also family-centered and its eye-rest cue overlaps an approved eye-break-at-work story. Left these rows unchanged and needs_revision. Continue screening for genuinely non-family premises that fit the stored category; do not reframe these merely by swapping a relative for a coworker.

## Active continuation — 2026-10-30, post-1,729 candidate screen

- Verified the clean resume branch at `693acaeb0312464af96bfdd4c9c0ed3ddf99c826`; live remote matched. V2 remains 1,729/5,000 pass, 3,271 needs revision, 0 pending. No new card was edited, added, or withdrawn in this screen.
- Re-screened possible non-family public-service, school, transport, and work rows by actual plot, not filename. The remaining school and transport examples examined are family-centered. `long_health_services_01.json[80]` is also household/father-centered; a possible non-family recycling-site rewrite was not selected because approved `long_family_finance_services_04.json[22]` already uses a recycling machine whose rejection spills bottles into a rolling/percussion sequence, and approved `long_family_finance_services_05.json[89]` uses cardboard jammed in a recycling-bin lid. Avoid another recycling-object obstruction gag.
- Screened current office-lunch needs-revision candidates. `long_food_shopping_03.json[41]` includes an allergen uncertainty and was left untouched rather than making safety the joke; `[43]` is still a recipe demonstration without a strong comic conflict; `[45]` is a soup-adjustment narrative that needs a distinct, genuinely funny mechanism before rewriting. Keep searching for a suitable non-family work/school/travel/public-service row and compare against approved plot mechanisms before editing. Do not treat these skips as new passes or as task completion.

## Active continuation — 2026-10-30, one-trip company-shop challenge

- Continued from verified resume branch `11beda0ce064988807584b3fdda22f7962ca8d3b`. Reworked `content/sentence_bank/long_food_shopping_13.json[2]`, preserving `買公司聚餐材料` and replacing unrelated sugar/salt and fire-alarm beats with a non-family coworker’s self-imposed no-basket challenge. A baguette, cheese, grapes, tomatoes, and crackers progressively fill his arms; a shifting grape box needs help, then the member-code scan calls for a coworker to hold it, and the cashier names the teamwork required to pay. The colleague concedes he will use a basket next time. No food safety claim or household/family plot.
- A limited 6.1-terra independent mechanism review suggested an ingredient-carrying challenge. Rechecked approved grocery/checkout stories, including the approved self-scan bag-detection story and lettuce-wrap picnic story; the former concerns an unregistered item on a scale, and the latter a torn leaf and school picnic, not this one-trip hand-carry / cashier handoff sequence. Search for `一趟`, basket, hands-full, member-code, and conveyor terms in approved shopping stories found no same chain.
- Manually reviewed all four source fields and context Jyutping. Final body: 280 Han characters / 280 Jyutping syllables; full Simplified gloss and exact `故事练习：` prefix. Final source hash `2af9a1fe64ab38ff1d9324505335ced69031efc8ecd7e25e79f61fb173ed3bbf`. Built app entry `sentence-bank-long_food_shopping_13-0003` mirrors all four fields and category and has `qualityPriority=1`.
- V2 is now 1,730/5,000 pass, 3,270 needs revision, 0 pending: one unique addition, no withdrawals. Refreshed checklist; `build_assets.py`, `validate_content.py` (8,000 entries), unit tests (7 run, 1 skipped), source/app/ledger mirror and hash assertions, and `git diff --check` passed. Task remains incomplete; continue from another eligible, meaningfully distinct non-family candidate.
