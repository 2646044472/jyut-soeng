package dev.local.yuecal.ui

import dev.local.yuecal.domain.CalibrationEntry
import org.junit.Assert.assertEquals
import org.junit.Test

class SentenceReaderSelectorTest {

    @Test
    fun selectsAStableDailyWindow() {
        val entries = (1..12).map { entry("sentence-%02d".format(it)) }

        assertEquals(
            listOf("sentence-05", "sentence-06", "sentence-07", "sentence-08"),
            selectDailySentenceEntries(entries, epochDay = 1, limit = 4).map { it.id },
        )
        assertEquals(
            selectDailySentenceEntries(entries, epochDay = 1, limit = 4),
            selectDailySentenceEntries(entries.shuffled(), epochDay = 1, limit = 4),
        )
    }

    @Test
    fun wrapsWhenTheDailyWindowReachesTheEnd() {
        val entries = (1..5).map { entry("sentence-%02d".format(it)) }

        assertEquals(
            listOf("sentence-02", "sentence-03", "sentence-04", "sentence-05"),
            selectDailySentenceEntries(entries, epochDay = 4, limit = 4).map { it.id },
        )
    }

    private fun entry(id: String) = CalibrationEntry(
        id = id,
        displayText = id,
        promptText = "prompt",
        answerJyutping = "si1",
        gloss = "意思",
        notes = "",
        usageTip = "使用场景",
        exampleSentence = id,
        exampleTranslation = "",
        entryType = "sentence",
        category = "日常",
        groupId = id,
        tone = 1,
        audioAsset = null,
        sourceLabel = "curated",
        statusLabel = "未开始",
    )
}
