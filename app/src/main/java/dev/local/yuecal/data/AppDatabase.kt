package dev.local.yuecal.data

import androidx.room.Dao
import androidx.room.Database
import androidx.room.Embedded
import androidx.room.Entity
import androidx.room.Index
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.PrimaryKey
import androidx.room.Query
import androidx.room.Relation
import androidx.room.RoomDatabase
import androidx.room.Transaction
import androidx.room.migration.Migration
import androidx.sqlite.db.SupportSQLiteDatabase
import kotlinx.coroutines.flow.Flow

@Entity(
    tableName = "calibration_entries",
    indices = [
        Index(value = ["displayText"]),
        Index(value = ["answerJyutping"]),
        Index(value = ["groupId"]),
    ],
)
data class CalibrationEntryEntity(
    @PrimaryKey val id: String,
    val displayText: String,
    val promptText: String,
    val answerJyutping: String,
    val gloss: String,
    val notes: String,
    val usageTip: String,
    val exampleSentence: String,
    val exampleTranslation: String,
    val entryType: String,
    val category: String,
    val groupId: String,
    val tone: Int,
    val audioAsset: String?,
    val sourceLabel: String,
    val sortOrder: Int,
    val createdAt: Long,
    val updatedAt: Long,
    val isActive: Boolean,
)

@Entity(tableName = "review_progress")
data class ReviewProgressEntity(
    @PrimaryKey val entryId: String,
    val repetitions: Int,
    val intervalDays: Int,
    val easeFactor: Double,
    val nextReviewEpochDay: Long,
    val lastReviewedAt: Long?,
    val totalCorrect: Int,
    val totalAttempts: Int,
    val streak: Int,
)

@Entity(tableName = "study_attempts", indices = [Index(value = ["sessionId"]), Index(value = ["entryId"])])
data class StudyAttemptEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val sessionId: String,
    val entryId: String,
    val selectedAnswer: String,
    val correctAnswer: String,
    val isCorrect: Boolean,
    val quality: Int,
    val answeredAt: Long,
    val responseMillis: Long,
)

data class EntryWithProgress(
    @Embedded val entry: CalibrationEntryEntity,
    @Relation(parentColumn = "id", entityColumn = "entryId")
    val progress: ReviewProgressEntity?,
)

@Dao
interface EntryDao {

    @Query("SELECT COUNT(*) FROM calibration_entries WHERE isActive = 1")
    fun observeEntryCount(): Flow<Int>

    @Query("SELECT COUNT(*) FROM calibration_entries WHERE isActive = 1 AND entryType = :entryType")
    fun observeEntryCountByType(entryType: String): Flow<Int>

    @Transaction
    @Query(
        """
        SELECT * FROM calibration_entries
        WHERE isActive = 1
        ORDER BY CASE WHEN sourceLabel = 'generated' THEN 1 ELSE 0 END ASC, sortOrder ASC, displayText ASC
        """,
    )
    fun observeLibraryEntries(): Flow<List<EntryWithProgress>>

    @Transaction
    @Query(
        """
        SELECT * FROM calibration_entries
        WHERE isActive = 1
          AND (
               displayText LIKE '%' || :query || '%'
           OR answerJyutping LIKE '%' || :query || '%'
           OR gloss LIKE '%' || :query || '%'
           OR notes LIKE '%' || :query || '%'
           OR usageTip LIKE '%' || :query || '%'
           OR exampleSentence LIKE '%' || :query || '%'
           OR exampleTranslation LIKE '%' || :query || '%'
          )
        ORDER BY CASE WHEN sourceLabel = 'generated' THEN 1 ELSE 0 END ASC, sortOrder ASC, displayText ASC
        LIMIT :limit
        """,
    )
    fun observeSearchResults(query: String, limit: Int): Flow<List<EntryWithProgress>>

    @Query(
        """
        SELECT e.* FROM calibration_entries e
        JOIN review_progress p ON e.id = p.entryId
        WHERE e.isActive = 1
          AND p.nextReviewEpochDay <= :today
        ORDER BY
          p.nextReviewEpochDay ASC,
          COALESCE(p.lastReviewedAt, 0) ASC,
          e.displayText ASC
        LIMIT :limit
        """,
    )
    suspend fun getDueEntries(today: Long, limit: Int): List<CalibrationEntryEntity>

    @Query(
        """
        SELECT e.* FROM calibration_entries e
        JOIN review_progress p ON e.id = p.entryId
        WHERE e.isActive = 1
          AND e.entryType = :entryType
          AND p.nextReviewEpochDay <= :today
        ORDER BY
          p.nextReviewEpochDay ASC,
          COALESCE(p.lastReviewedAt, 0) ASC,
          e.displayText ASC
        LIMIT :limit
        """,
    )
    suspend fun getDueEntriesByType(entryType: String, today: Long, limit: Int): List<CalibrationEntryEntity>

    @Query(
        """
        SELECT e.* FROM calibration_entries e
        JOIN review_progress p ON e.id = p.entryId
        WHERE e.isActive = 1
          AND e.entryType = :entryType
          AND p.repetitions = 0
          AND p.nextReviewEpochDay <= :today
        ORDER BY
          p.nextReviewEpochDay ASC,
          COALESCE(p.lastReviewedAt, 0) ASC,
          e.sortOrder ASC,
          e.displayText ASC
        LIMIT :limit
        """,
    )
    suspend fun getLearningEntriesByType(entryType: String, today: Long, limit: Int): List<CalibrationEntryEntity>

    @Query(
        """
        SELECT e.* FROM calibration_entries e
        JOIN review_progress p ON e.id = p.entryId
        WHERE e.isActive = 1
          AND e.entryType = :entryType
          AND p.nextReviewEpochDay > :today
          AND p.nextReviewEpochDay <= :lookaheadDay
        ORDER BY
          p.nextReviewEpochDay ASC,
          COALESCE(p.lastReviewedAt, 0) ASC,
          e.displayText ASC
        LIMIT :limit
        """,
    )
    suspend fun getScheduledEntriesByType(
        entryType: String,
        today: Long,
        lookaheadDay: Long,
        limit: Int,
    ): List<CalibrationEntryEntity>

    @Query(
        """
        SELECT e.* FROM calibration_entries e
        JOIN review_progress p ON e.id = p.entryId
        WHERE e.isActive = 1
          AND e.entryType = :entryType
        ORDER BY
          p.nextReviewEpochDay ASC,
          COALESCE(p.lastReviewedAt, 0) ASC,
          e.displayText ASC
        LIMIT :limit
        """,
    )
    suspend fun getStartedReviewEntriesByType(entryType: String, limit: Int): List<CalibrationEntryEntity>

    @Query("SELECT * FROM calibration_entries WHERE isActive = 1 ORDER BY RANDOM() LIMIT :limit")
    suspend fun getFallbackEntries(limit: Int): List<CalibrationEntryEntity>

    @Query(
        """
        SELECT * FROM calibration_entries
        WHERE isActive = 1
          AND entryType = :entryType
        ORDER BY RANDOM()
        LIMIT :limit
        """,
    )
    suspend fun getFallbackEntriesByType(entryType: String, limit: Int): List<CalibrationEntryEntity>

    @Query(
        """
        SELECT e.* FROM calibration_entries e
        LEFT JOIN review_progress p ON e.id = p.entryId
        WHERE e.isActive = 1
          AND e.entryType = :entryType
          AND p.entryId IS NULL
        ORDER BY CASE WHEN e.sourceLabel = 'generated' THEN 1 ELSE 0 END ASC, RANDOM()
        LIMIT :limit
        """,
    )
    suspend fun getNewEntriesByType(entryType: String, limit: Int): List<CalibrationEntryEntity>

    @Query("SELECT * FROM calibration_entries WHERE isActive = 1 AND id = :id LIMIT 1")
    suspend fun getEntryById(id: String): CalibrationEntryEntity?

    @Query("SELECT * FROM calibration_entries WHERE isActive = 1 AND groupId = :groupId ORDER BY tone ASC")
    suspend fun getByGroup(groupId: String): List<CalibrationEntryEntity>

    @Query("SELECT * FROM calibration_entries WHERE isActive = 1 ORDER BY displayText ASC")
    suspend fun getAllEntries(): List<CalibrationEntryEntity>

    @Query("SELECT * FROM calibration_entries ORDER BY displayText ASC")
    suspend fun getAllEntriesIncludingArchived(): List<CalibrationEntryEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertEntries(entries: List<CalibrationEntryEntity>)

    @Query(
        """
        UPDATE calibration_entries
        SET isActive = 0,
            updatedAt = :updatedAt
        WHERE id IN (:entryIds)
        """,
    )
    suspend fun archiveEntries(entryIds: List<String>, updatedAt: Long)
}

@Dao
interface ProgressDao {

    @Query(
        """
        SELECT COUNT(*) FROM calibration_entries e
        JOIN review_progress p ON e.id = p.entryId
        WHERE e.isActive = 1
          AND p.nextReviewEpochDay <= :today
        """,
    )
    fun observeDueCount(today: Long): Flow<Int>

    @Query(
        """
        SELECT COUNT(*) FROM calibration_entries e
        JOIN review_progress p ON e.id = p.entryId
        WHERE e.isActive = 1
          AND e.entryType = :entryType
          AND p.nextReviewEpochDay <= :today
        """,
    )
    fun observeDueCountByType(entryType: String, today: Long): Flow<Int>

    @Query(
        """
        SELECT COUNT(*) FROM calibration_entries e
        LEFT JOIN review_progress p ON e.id = p.entryId
        WHERE e.isActive = 1
          AND e.entryType = :entryType
          AND p.entryId IS NULL
        """,
    )
    fun observeNewCountByType(entryType: String): Flow<Int>

    @Query(
        """
        SELECT COUNT(*) FROM calibration_entries e
        JOIN review_progress p ON e.id = p.entryId
        WHERE e.isActive = 1
          AND p.nextReviewEpochDay = :day
        """,
    )
    fun observeIncomingCount(day: Long): Flow<Int>

    @Query(
        """
        SELECT COUNT(*) FROM calibration_entries e
        JOIN review_progress p ON e.id = p.entryId
        WHERE e.isActive = 1
          AND p.nextReviewEpochDay <= :today
        """,
    )
    suspend fun dueCountNow(today: Long): Int

    @Query(
        """
        SELECT COUNT(*) FROM calibration_entries e
        JOIN review_progress p ON e.id = p.entryId
        WHERE e.isActive = 1
          AND e.entryType = :entryType
          AND p.nextReviewEpochDay <= :today
        """,
    )
    suspend fun dueCountNowByType(entryType: String, today: Long): Int

    @Query(
        """
        SELECT COUNT(*) FROM calibration_entries e
        JOIN review_progress p ON e.id = p.entryId
        WHERE e.isActive = 1
        """,
    )
    fun observeStartedCount(): Flow<Int>

    @Query(
        """
        SELECT COUNT(*) FROM calibration_entries e
        JOIN review_progress p ON e.id = p.entryId
        WHERE e.isActive = 1
          AND e.entryType = :entryType
        """,
    )
    fun observeStartedCountByType(entryType: String): Flow<Int>

    @Query(
        """
        SELECT COUNT(*) FROM calibration_entries e
        JOIN review_progress p ON e.id = p.entryId
        WHERE e.isActive = 1
          AND e.entryType = :entryType
        """,
    )
    suspend fun startedCountNowByType(entryType: String): Int

    @Query("SELECT * FROM review_progress WHERE entryId = :entryId LIMIT 1")
    suspend fun getProgress(entryId: String): ReviewProgressEntity?

    @Query("SELECT * FROM review_progress WHERE entryId IN (:entryIds)")
    suspend fun getProgressByEntryIds(entryIds: List<String>): List<ReviewProgressEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertProgress(progress: ReviewProgressEntity)

    @Query("DELETE FROM review_progress WHERE entryId IN (:entryIds)")
    suspend fun deleteProgressByEntryIds(entryIds: List<String>)
}

@Dao
interface SessionDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAttempt(attempt: StudyAttemptEntity)

    @Query(
        """
        UPDATE study_attempts
        SET entryId = :targetEntryId
        WHERE entryId = :sourceEntryId
        """,
    )
    suspend fun reassignAttempts(sourceEntryId: String, targetEntryId: String)

    @Query("SELECT COUNT(*) FROM study_attempts")
    fun observeAttemptsCount(): Flow<Int>

    @Query("SELECT SUM(CASE WHEN isCorrect THEN 1 ELSE 0 END) FROM study_attempts")
    fun observeCorrectCount(): Flow<Int?>
}

@Database(
    entities = [CalibrationEntryEntity::class, ReviewProgressEntity::class, StudyAttemptEntity::class],
    version = 4,
    exportSchema = false,
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun entryDao(): EntryDao
    abstract fun progressDao(): ProgressDao
    abstract fun sessionDao(): SessionDao
}

val MIGRATION_3_4 = object : Migration(3, 4) {
    override fun migrate(database: SupportSQLiteDatabase) {
        database.execSQL(
            """
            ALTER TABLE calibration_entries
            ADD COLUMN isActive INTEGER NOT NULL DEFAULT 1
            """.trimIndent(),
        )
    }
}
