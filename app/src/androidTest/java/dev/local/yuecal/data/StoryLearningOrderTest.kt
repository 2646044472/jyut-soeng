package dev.local.yuecal.data

import androidx.room.Room
import androidx.test.platform.app.InstrumentationRegistry
import kotlinx.coroutines.runBlocking
import kotlinx.serialization.json.Json
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class StoryLearningOrderTest {
    @Test
    fun bundledStoriesLeadNewSentenceQueueAndLearnedProgressIsKept() = runBlocking {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val bundle = Json.decodeFromString<ContentBundle>(
            context.assets.open("builtin/content.json").bufferedReader().use { it.readText() },
        )
        val sentences = bundle.entries.filter { it.entryType == "sentence" }.sortedBy { it.sortOrder }
        val ready = sentences.take(55)
        assertTrue(ready.all { it.usageTip.startsWith("故事练习：") })
        val database = Room.inMemoryDatabaseBuilder(context, AppDatabase::class.java).build()
        try {
            val samples = ready + sentences.last().copy(category = "高频回应")
            database.entryDao().upsertEntries(samples.map { asset ->
                CalibrationEntryEntity(
                    id = asset.id, displayText = asset.displayText, promptText = asset.promptText,
                    answerJyutping = asset.answerJyutping, gloss = asset.gloss, notes = asset.notes,
                    usageTip = asset.usageTip, exampleSentence = asset.exampleSentence,
                    exampleTranslation = asset.exampleTranslation, entryType = asset.entryType,
                    category = asset.category, groupId = asset.groupId, tone = asset.tone,
                    audioAsset = asset.audioAsset, sourceLabel = "builtin", sortOrder = asset.sortOrder,
                    createdAt = 0, updatedAt = 0, isActive = true,
                )
            })
            assertEquals(ready.take(50).map { it.id }, database.entryDao().getNewEntriesByType("sentence", 50).map { it.id })
            val progress = ReviewProgressEntity(ready.first().id, 1, 1, 2.5, 1, 0, 1, 1, 1)
            database.progressDao().upsertProgress(progress)
            assertEquals(ready.drop(1).take(50).map { it.id }, database.entryDao().getNewEntriesByType("sentence", 50).map { it.id })
            assertEquals(progress, database.progressDao().getProgress(progress.entryId))
        } finally {
            database.close()
        }
    }
}
