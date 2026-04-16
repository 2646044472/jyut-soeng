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
    val createdAt: Long,
    val updatedAt: Long,
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

    @Query("SELECT COUNT(*) FROM calibration_entries")
    fun observeEntryCount(): Flow<Int>

    @Query("SELECT COUNT(*) FROM calibration_entries WHERE entryType = :entryType")
    fun observeEntryCountByType(entryType: String): Flow<Int>

    @Transaction
    @Query("SELECT * FROM calibration_entries ORDER BY displayText ASC")
    fun observeLibraryEntries(): Flow<List<EntryWithProgress>>

    @Transaction
    @Query(
        """
        SELECT * FROM calibration_entries
        WHERE displayText LIKE '%' || :query || '%'
           OR answerJyutping LIKE '%' || :query || '%'
           OR gloss LIKE '%' || :query || '%'
           OR notes LIKE '%' || :query || '%'
           OR usageTip LIKE '%' || :query || '%'
           OR exampleSentence LIKE '%' || :query || '%'
           OR exampleTranslation LIKE '%' || :query || '%'
        ORDER BY displayText ASC
        LIMIT :limit
        """,
    )
    fun observeSearchResults(query: String, limit: Int): Flow<List<EntryWithProgress>>

    @Query(
        """
        SELECT e.* FROM calibration_entries e
        LEFT JOIN review_progress p ON e.id = p.entryId
        WHERE p.entryId IS NULL OR p.nextReviewEpochDay <= :today
        ORDER BY COALESCE(p.nextReviewEpochDay, 0) ASC, e.displayText ASC
        LIMIT :limit
        """,
    )
    suspend fun getDueEntries(today: Long, limit: Int): List<CalibrationEntryEntity>

    @Query(
        """
        SELECT e.* FROM calibration_entries e
        LEFT JOIN review_progress p ON e.id = p.entryId
        WHERE e.entryType = :entryType
          AND (p.entryId IS NULL OR p.nextReviewEpochDay <= :today)
        ORDER BY COALESCE(p.nextReviewEpochDay, 0) ASC, e.displayText ASC
        LIMIT :limit
        """,
    )
    suspend fun getDueEntriesByType(entryType: String, today: Long, limit: Int): List<CalibrationEntryEntity>

    @Query("SELECT * FROM calibration_entries ORDER BY RANDOM() LIMIT :limit")
    suspend fun getFallbackEntries(limit: Int): List<CalibrationEntryEntity>

    @Query("SELECT * FROM calibration_entries WHERE entryType = :entryType ORDER BY RANDOM() LIMIT :limit")
    suspend fun getFallbackEntriesByType(entryType: String, limit: Int): List<CalibrationEntryEntity>

    @Query(
        """
        SELECT e.* FROM calibration_entries e
        LEFT JOIN review_progress p ON e.id = p.entryId
        WHERE e.entryType = :entryType
          AND p.entryId IS NULL
        ORDER BY e.displayText ASC
        LIMIT :limit
        """,
    )
    suspend fun getNewEntriesByType(entryType: String, limit: Int): List<CalibrationEntryEntity>

    @Query("SELECT * FROM calibration_entries WHERE id = :id LIMIT 1")
    suspend fun getEntryById(id: String): CalibrationEntryEntity?

    @Query("SELECT * FROM calibration_entries WHERE groupId = :groupId ORDER BY tone ASC")
    suspend fun getByGroup(groupId: String): List<CalibrationEntryEntity>

    @Query("SELECT * FROM calibration_entries ORDER BY displayText ASC")
    suspend fun getAllEntries(): List<CalibrationEntryEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertEntries(entries: List<CalibrationEntryEntity>)
}

@Dao
interface ProgressDao {

    @Query(
        """
        SELECT COUNT(*) FROM calibration_entries e
        LEFT JOIN review_progress p ON e.id = p.entryId
        WHERE p.entryId IS NOT NULL AND p.nextReviewEpochDay <= :today
        """,
    )
    fun observeDueCount(today: Long): Flow<Int>

    @Query(
        """
        SELECT COUNT(*) FROM calibration_entries e
        LEFT JOIN review_progress p ON e.id = p.entryId
        WHERE e.entryType = :entryType
          AND p.entryId IS NOT NULL
          AND p.nextReviewEpochDay <= :today
        """,
    )
    fun observeDueCountByType(entryType: String, today: Long): Flow<Int>

    @Query(
        """
        SELECT COUNT(*) FROM calibration_entries e
        LEFT JOIN review_progress p ON e.id = p.entryId
        WHERE e.entryType = :entryType
          AND p.entryId IS NULL
        """,
    )
    fun observeNewCountByType(entryType: String): Flow<Int>

    @Query(
        """
        SELECT COUNT(*) FROM calibration_entries e
        LEFT JOIN review_progress p ON e.id = p.entryId
        WHERE p.entryId IS NOT NULL AND p.nextReviewEpochDay <= :today
        """,
    )
    suspend fun dueCountNow(today: Long): Int

    @Query("SELECT COUNT(*) FROM review_progress WHERE repetitions > 0")
    fun observeStartedCount(): Flow<Int>

    @Query("SELECT * FROM review_progress WHERE entryId = :entryId LIMIT 1")
    suspend fun getProgress(entryId: String): ReviewProgressEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertProgress(progress: ReviewProgressEntity)
}

@Dao
interface SessionDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAttempt(attempt: StudyAttemptEntity)

    @Query("SELECT COUNT(*) FROM study_attempts")
    fun observeAttemptsCount(): Flow<Int>

    @Query("SELECT SUM(CASE WHEN isCorrect THEN 1 ELSE 0 END) FROM study_attempts")
    fun observeCorrectCount(): Flow<Int?>
}

@Database(
    entities = [CalibrationEntryEntity::class, ReviewProgressEntity::class, StudyAttemptEntity::class],
    version = 2,
    exportSchema = false,
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun entryDao(): EntryDao
    abstract fun progressDao(): ProgressDao
    abstract fun sessionDao(): SessionDao
}
