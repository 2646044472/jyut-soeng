package dev.local.yuecal.domain

import java.time.LocalDate

data class CalibrationEntry(
    val id: String,
    val displayText: String,
    val promptText: String,
    val answerJyutping: String,
    val gloss: String,
    val notes: String,
    val category: String,
    val groupId: String,
    val tone: Int,
    val audioAsset: String?,
    val sourceLabel: String,
    val dueNow: Boolean,
)

data class EntryProgress(
    val repetitions: Int = 0,
    val intervalDays: Int = 0,
    val easeFactor: Double = 2.5,
    val nextReviewEpochDay: Long = todayEpochDay(),
    val lastReviewedAt: Long? = null,
    val totalCorrect: Int = 0,
    val totalAttempts: Int = 0,
    val streak: Int = 0,
)

data class DashboardSummary(
    val totalEntries: Int = 0,
    val dueEntries: Int = 0,
    val startedEntries: Int = 0,
    val totalAttempts: Int = 0,
    val totalCorrect: Int = 0,
    val dailyGoal: Int = 20,
) {
    val accuracyPercent: Int
        get() = if (totalAttempts == 0) 0 else ((totalCorrect * 100.0) / totalAttempts).toInt()
}

data class StudyQuestion(
    val entryId: String,
    val displayText: String,
    val promptText: String,
    val answerJyutping: String,
    val options: List<String>,
    val audioAsset: String?,
    val category: String,
    val notes: String,
)

data class StudySession(
    val sessionId: String,
    val questions: List<StudyQuestion>,
)

data class SubmissionOutcome(
    val isCorrect: Boolean,
    val correctAnswer: String,
    val updatedProgress: EntryProgress,
    val quality: Int,
)

data class AppSettings(
    val autoplayAudio: Boolean = true,
    val remindersEnabled: Boolean = true,
    val dailyGoal: Int = 24,
    val builtInSeedVersion: String = "",
)

data class ImportResult(
    val sourceLabel: String,
    val version: String,
    val importedCount: Int,
)

fun todayEpochDay(): Long = LocalDate.now().toEpochDay()
