package dev.local.yuecal.data

import android.content.Context
import androidx.room.Room
import androidx.test.platform.app.InstrumentationRegistry
import kotlinx.coroutines.runBlocking
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class ReviewedSentencePriorityTest {
    private val context: Context
        get() = InstrumentationRegistry.getInstrumentation().targetContext

    @Test
    fun newSentenceQueryPrioritizesReviewedBeforeLimitAndExcludesStudiedAndInactive() = runBlocking {
        val database = Room.inMemoryDatabaseBuilder(context, AppDatabase::class.java).build()
        try {
            val dao = database.entryDao()
            dao.upsertEntries(listOf(
                entry("old", false), entry("story1", true), entry("story2", true),
                entry("studied-story", true), entry("inactive-story", true).copy(isActive = false),
                entry("word", false).copy(entryType = "word"),
            ))
            database.progressDao().upsertProgress(progress("studied-story"))
            val first = dao.getNewEntriesByType("sentence", 2)
            assertEquals(setOf("story1", "story2"), first.map { it.id }.toSet())
            assertTrue(first.all { it.storyReviewed })
            val withFallback = dao.getNewEntriesByType("sentence", 10)
            assertEquals(3, withFallback.size)
            assertEquals("old", withFallback.last().id)
            assertEquals(listOf("word"), dao.getNewEntriesByType("word", 10).map { it.id })
        } finally {
            database.close()
        }
    }

    @Test
    fun versionFourUpgradePreservesExistingEntriesAndLearningProgress() = runBlocking {
        val name = "reviewed-story-migration-test.db"
        context.deleteDatabase(name)
        context.openOrCreateDatabase(name, Context.MODE_PRIVATE, null).use { old ->
            old.execSQL("""CREATE TABLE calibration_entries (
                id TEXT NOT NULL PRIMARY KEY, displayText TEXT NOT NULL, promptText TEXT NOT NULL,
                answerJyutping TEXT NOT NULL, gloss TEXT NOT NULL, notes TEXT NOT NULL,
                usageTip TEXT NOT NULL, exampleSentence TEXT NOT NULL, exampleTranslation TEXT NOT NULL,
                entryType TEXT NOT NULL, category TEXT NOT NULL, groupId TEXT NOT NULL, tone INTEGER NOT NULL,
                audioAsset TEXT, sourceLabel TEXT NOT NULL, sortOrder INTEGER NOT NULL,
                createdAt INTEGER NOT NULL, updatedAt INTEGER NOT NULL, isActive INTEGER NOT NULL)""")
            for (column in listOf("displayText", "answerJyutping", "groupId")) {
                old.execSQL("CREATE INDEX index_calibration_entries_$column ON calibration_entries ($column)")
            }
            old.execSQL("""CREATE TABLE review_progress (
                entryId TEXT NOT NULL PRIMARY KEY, repetitions INTEGER NOT NULL, intervalDays INTEGER NOT NULL,
                easeFactor REAL NOT NULL, nextReviewEpochDay INTEGER NOT NULL, lastReviewedAt INTEGER,
                totalCorrect INTEGER NOT NULL, totalAttempts INTEGER NOT NULL, streak INTEGER NOT NULL)""")
            old.execSQL("""CREATE TABLE study_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, sessionId TEXT NOT NULL, entryId TEXT NOT NULL,
                selectedAnswer TEXT NOT NULL, correctAnswer TEXT NOT NULL, isCorrect INTEGER NOT NULL,
                quality INTEGER NOT NULL, answeredAt INTEGER NOT NULL, responseMillis INTEGER NOT NULL)""")
            for (column in listOf("sessionId", "entryId")) {
                old.execSQL("CREATE INDEX index_study_attempts_$column ON study_attempts ($column)")
            }
            old.execSQL("INSERT INTO calibration_entries VALUES ('legacy', '舊句', '', 'gau6 geoi3', '旧句', '', '', '', '', 'sentence', '日常', 'legacy', 0, NULL, 'builtin', 1, 1, 1, 1)")
            old.execSQL("INSERT INTO review_progress VALUES ('legacy', 3, 7, 2.5, 123, 42, 4, 5, 2)")
            old.version = 4
        }
        val database = Room.databaseBuilder(context, AppDatabase::class.java, name)
            .addMigrations(MIGRATION_4_5).build()
        try {
            val existing = database.entryDao().getEntryById("legacy")!!
            assertFalse(existing.storyReviewed)
            val progress = database.progressDao().getProgress("legacy")!!
            assertEquals(3, progress.repetitions)
            assertEquals(7, progress.intervalDays)
            database.entryDao().upsertEntries(listOf(existing.copy(displayText = "升級故事", storyReviewed = true)))
            assertEquals(progress, database.progressDao().getProgress("legacy"))
            assertTrue(database.entryDao().getEntryById("legacy")!!.storyReviewed)
        } finally {
            database.close()
            context.deleteDatabase(name)
        }
    }

    private fun entry(id: String, reviewed: Boolean) = CalibrationEntryEntity(
        id, id, "", "si1", "", "", "", "", "", "sentence", "", id, 0, null,
        "builtin", 1, 0, 0, true, storyReviewed = reviewed,
    )

    private fun progress(id: String) = ReviewProgressEntity(id, 2, 3, 2.5, 123, 42, 2, 2, 2)
}
