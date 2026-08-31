package dev.local.yuecal.ui

import dev.local.yuecal.domain.CalibrationEntry
import org.junit.Assert.assertEquals
import org.junit.Test

class LibraryFilterTest {

    @Test
    fun `filters entries by the selected category`() {
        val transit = entry(id = "transit", category = "出行场景")
        val home = entry(id = "home", category = "居家场景")

        assertEquals(listOf(transit), filterLibraryEntries(listOf(transit, home), "出行场景"))
    }

    @Test
    fun `shows every entry when no category is selected`() {
        val entries = listOf(entry(id = "one", category = "出行场景"), entry(id = "two", category = "居家场景"))

        assertEquals(entries, filterLibraryEntries(entries, null))
    }

    private fun entry(id: String, category: String) = CalibrationEntry(
        id = id,
        displayText = id,
        promptText = "prompt",
        answerJyutping = "si1",
        gloss = "意思",
        notes = "",
        usageTip = "点用",
        exampleSentence = id,
        exampleTranslation = "",
        entryType = "word",
        category = category,
        groupId = id,
        tone = 1,
        audioAsset = null,
        sourceLabel = "curated",
        statusLabel = "未开始",
    )
}
