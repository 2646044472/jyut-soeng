package dev.local.yuecal.data

import kotlin.random.Random
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class SessionEntryOrderTest {
    @Test
    fun orderRandomizesEntriesWithoutDroppingThem() {
        val entries = listOf(entry("old1"), entry("story1", true), entry("old2"), entry("story2", true))
        val orders = mutableSetOf<List<String>>()
        repeat(20) { seed ->
            val selected = orderSessionEntries(entries, Random(seed))
            orders += selected.map { it.id }
            assertEquals(entries.map { it.id }.toSet(), selected.map { it.id }.toSet())
        }
        assertTrue("expected order to vary", orders.size > 1)
    }

    private fun entry(id: String, reviewed: Boolean = false) = CalibrationEntryEntity(
        id, id, "", "si1", "", "", "", "", "", "sentence", "", id, 0, null,
        "builtin", 1, 0, 0, true, storyReviewed = reviewed,
    )
}
