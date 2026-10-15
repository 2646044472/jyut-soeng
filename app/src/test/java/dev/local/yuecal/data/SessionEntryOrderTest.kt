package dev.local.yuecal.data

import dev.local.yuecal.domain.SessionMode
import kotlin.random.Random
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class SessionEntryOrderTest {
    @Test
    fun sentenceLearningKeepsReviewedStoriesAheadOfFallbackInStableOrder() {
        val entries = listOf(entry("old1"), entry("story1", true), entry("old2"), entry("story2", true))
        repeat(20) { seed ->
            val selected = orderSessionEntries(entries, SessionMode.Learn, "sentence", Random(seed))
            assertTrue(selected.take(2).all { it.storyReviewed })
            assertTrue(selected.drop(2).none { it.storyReviewed })
            assertEquals(listOf("story1", "story2", "old1", "old2"), selected.map { it.id })
            assertEquals(entries.map { it.id }.toSet(), selected.map { it.id }.toSet())
        }
    }

    @Test
    fun otherSessionsKeepTheirExistingShufflePolicy() {
        val entries = listOf(entry("old"), entry("story", true))
        for ((mode, type) in listOf(SessionMode.Review to "sentence", SessionMode.Learn to "word")) {
            assertEquals(entries.shuffled(Random(7)), orderSessionEntries(entries, mode, type, Random(7)))
        }
    }

    private fun entry(id: String, reviewed: Boolean = false) = CalibrationEntryEntity(
        id, id, "", "si1", "", "", "", "", "", "sentence", "", id, 0, null,
        "builtin", 1, 0, 0, true, storyReviewed = reviewed,
    )
}
