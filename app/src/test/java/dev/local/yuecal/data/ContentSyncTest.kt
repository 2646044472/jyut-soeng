package dev.local.yuecal.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class ContentSyncTest {

    @Test
    fun replacedManagedEntryMigratesToIncomingIdAndRemovedEntryGetsArchived() {
        val plan = ManagedEntrySyncPlanner.plan(
            existingEntries = listOf(
                entry(
                    id = "old-sik6-faan6",
                    displayText = "食饭",
                    answerJyutping = "sik6 faan6",
                    sourceLabel = "github",
                ),
                entry(
                    id = "obsolete-hei2-san1",
                    displayText = "起身",
                    answerJyutping = "hei2 san1",
                    sourceLabel = "builtin",
                ),
            ),
            incomingEntries = listOf(
                asset(
                    id = "new-sik6-faan6",
                    displayText = "食饭",
                    answerJyutping = "sik6 faan6",
                ),
            ),
        )

        assertEquals("new-sik6-faan6", plan.aliasTargetByEntryId["old-sik6-faan6"])
        assertTrue("old-sik6-faan6" in plan.archiveEntryIds)
        assertTrue("obsolete-hei2-san1" in plan.archiveEntryIds)
    }

    @Test
    fun localImportEntryDoesNotGetFoldedIntoManagedSyncPlan() {
        val plan = ManagedEntrySyncPlanner.plan(
            existingEntries = listOf(
                entry(
                    id = "local-sik6-faan6",
                    displayText = "食饭",
                    answerJyutping = "sik6 faan6",
                    sourceLabel = "local-import",
                ),
            ),
            incomingEntries = listOf(
                asset(
                    id = "github-sik6-faan6",
                    displayText = "食饭",
                    answerJyutping = "sik6 faan6",
                ),
            ),
        )

        assertTrue(plan.aliasTargetByEntryId.isEmpty())
        assertTrue(plan.archiveEntryIds.isEmpty())
    }

    @Test
    fun mergedReviewProgressPreservesTotalsAndEarliestNextReview() {
        val merged = ReviewProgressMerger.merge(
            targetId = "shared-entry",
            records = listOf(
                ReviewProgressEntity(
                    entryId = "old-entry",
                    repetitions = 2,
                    intervalDays = 3,
                    easeFactor = 2.5,
                    nextReviewEpochDay = 120,
                    lastReviewedAt = 1_700_000_000_000,
                    totalCorrect = 2,
                    totalAttempts = 3,
                    streak = 2,
                ),
                ReviewProgressEntity(
                    entryId = "new-entry",
                    repetitions = 4,
                    intervalDays = 10,
                    easeFactor = 2.7,
                    nextReviewEpochDay = 140,
                    lastReviewedAt = 1_800_000_000_000,
                    totalCorrect = 4,
                    totalAttempts = 5,
                    streak = 4,
                ),
            ),
        ) ?: error("Expected merged progress")

        assertEquals("shared-entry", merged.entryId)
        assertEquals(4, merged.repetitions)
        assertEquals(10, merged.intervalDays)
        assertEquals(120, merged.nextReviewEpochDay)
        assertEquals(1_800_000_000_000, merged.lastReviewedAt)
        assertEquals(6, merged.totalCorrect)
        assertEquals(8, merged.totalAttempts)
        assertEquals(4, merged.streak)
    }

    private fun asset(
        id: String,
        displayText: String,
        answerJyutping: String,
        entryType: String = "word",
    ): ContentEntryAsset = ContentEntryAsset(
        id = id,
        displayText = displayText,
        promptText = displayText,
        answerJyutping = answerJyutping,
        entryType = entryType,
    )

    private fun entry(
        id: String,
        displayText: String,
        answerJyutping: String,
        sourceLabel: String,
        isActive: Boolean = true,
        entryType: String = "word",
    ): CalibrationEntryEntity = CalibrationEntryEntity(
        id = id,
        displayText = displayText,
        promptText = displayText,
        answerJyutping = answerJyutping,
        gloss = "",
        notes = "",
        usageTip = "",
        exampleSentence = "",
        exampleTranslation = "",
        entryType = entryType,
        category = "",
        groupId = answerJyutping.substringBefore(' '),
        tone = answerJyutping.lastOrNull()?.digitToIntOrNull() ?: 0,
        audioAsset = null,
        sourceLabel = sourceLabel,
        sortOrder = 1,
        createdAt = 0,
        updatedAt = 0,
        isActive = isActive,
    )
}
