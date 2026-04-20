package dev.local.yuecal.domain

import java.time.LocalDate

data class CalibrationEntry(
    val id: String,
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
    val statusLabel: String,
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
    val dueWordEntries: Int = 0,
    val dueExpressionEntries: Int = 0,
    val incomingReviewEntries: Int = 0,
    val newWordEntries: Int = 0,
    val newExpressionEntries: Int = 0,
    val wordEntries: Int = 0,
    val expressionEntries: Int = 0,
    val startedEntries: Int = 0,
    val totalAttempts: Int = 0,
    val totalCorrect: Int = 0,
    val dailyLearnGoal: Int = 10,
    val dailyReviewGoal: Int = 0,
) {
    val accuracyPercent: Int
        get() = if (totalAttempts == 0) 0 else ((totalCorrect * 100.0) / totalAttempts).toInt()
}

enum class SessionMode {
    Learn,
    Review,
}

enum class StudyQuestionType {
    FillJyutping,
    MultipleChoice,
    ExpressionCard,
}

data class StudyQuestion(
    val entryId: String,
    val type: StudyQuestionType,
    val displayText: String,
    val promptText: String,
    val answerJyutping: String,
    val gloss: String,
    val options: List<String> = emptyList(),
    val audioAsset: String?,
    val category: String,
    val notes: String,
    val usageTip: String,
    val exampleSentence: String,
    val exampleTranslation: String,
    val sourceLabel: String,
)

data class StudySession(
    val sessionId: String,
    val mode: SessionMode,
    val title: String,
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
    val dailyLearnGoal: Int = 10,
    val builtInSeedVersion: String = "",
)

data class ImportResult(
    val sourceLabel: String,
    val version: String,
    val importedCount: Int,
)

fun EntryProgress?.isInReviewQueue(): Boolean = this != null && repetitions > 0

fun EntryProgress?.needsReviewBy(day: Long): Boolean = this != null && nextReviewEpochDay <= day

fun EntryProgress?.needsReviewToday(today: Long = todayEpochDay()): Boolean = needsReviewBy(today)

fun EntryProgress?.statusLabel(today: Long = todayEpochDay()): String = when {
    this == null -> "未开始"
    repetitions <= 0 && needsReviewToday(today) -> "待巩固"
    repetitions <= 0 -> "学习中"
    needsReviewToday(today) -> "待复习"
    else -> "已排程"
}

fun todayEpochDay(): Long = LocalDate.now().toEpochDay()
