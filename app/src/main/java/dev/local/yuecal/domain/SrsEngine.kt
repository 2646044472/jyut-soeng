package dev.local.yuecal.domain

import kotlin.math.max

object JudgingEngine {

    fun score(
        isCorrect: Boolean,
        responseMillis: Long,
        questionType: StudyQuestionType,
    ): Int {
        if (!isCorrect) {
            return when (questionType) {
                StudyQuestionType.MultipleChoice -> 1
                StudyQuestionType.FillJyutping, StudyQuestionType.ExpressionCard -> 2
            }
        }
        return when (questionType) {
            StudyQuestionType.MultipleChoice -> {
                if (responseMillis in 1..2200) 4 else 3
            }
            StudyQuestionType.FillJyutping, StudyQuestionType.ExpressionCard -> {
                if (responseMillis in 1..4500) 5 else 4
            }
        }
    }
}

object Sm2Scheduler {

    fun next(
        current: EntryProgress?,
        quality: Int,
        today: Long = todayEpochDay(),
        nowMillis: Long = System.currentTimeMillis(),
    ): EntryProgress {
        val base = current ?: EntryProgress()
        val normalizedQuality = quality.coerceIn(0, 5)

        if (normalizedQuality < 3) {
            return base.copy(
                repetitions = 0,
                intervalDays = 1,
                easeFactor = max(1.35, base.easeFactor - 0.15),
                nextReviewEpochDay = today + 1,
                lastReviewedAt = nowMillis,
                totalCorrect = base.totalCorrect,
                totalAttempts = base.totalAttempts + 1,
                streak = 0,
            )
        }

        val newEase = max(
            1.35,
            base.easeFactor + (0.12 - (5 - normalizedQuality) * (0.07 + (5 - normalizedQuality) * 0.02)),
        )
        val newRepetitions = base.repetitions + 1
        val newInterval = when (newRepetitions) {
            1 -> 1
            2 -> 2
            3 -> 3
            4 -> 7
            else -> (base.intervalDays * (newEase + 0.18)).toInt().coerceAtLeast(base.intervalDays + 2)
        }

        return base.copy(
            repetitions = newRepetitions,
            intervalDays = newInterval,
            easeFactor = newEase,
            nextReviewEpochDay = today + newInterval,
            lastReviewedAt = nowMillis,
            totalCorrect = base.totalCorrect + 1,
            totalAttempts = base.totalAttempts + 1,
            streak = base.streak + 1,
        )
    }
}
