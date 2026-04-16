package dev.local.yuecal.domain

import kotlin.math.max

object JudgingEngine {

    fun score(isCorrect: Boolean, responseMillis: Long): Int {
        if (!isCorrect) return 2
        return if (responseMillis in 1..3500) 5 else 4
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
                easeFactor = max(1.3, base.easeFactor - 0.2),
                nextReviewEpochDay = today + 1,
                lastReviewedAt = nowMillis,
                totalCorrect = base.totalCorrect,
                totalAttempts = base.totalAttempts + 1,
                streak = 0,
            )
        }

        val newEase = max(
            1.3,
            base.easeFactor + (0.1 - (5 - normalizedQuality) * (0.08 + (5 - normalizedQuality) * 0.02)),
        )
        val newRepetitions = base.repetitions + 1
        val newInterval = when (newRepetitions) {
            1 -> 1
            2 -> 3
            else -> (base.intervalDays * newEase).toInt().coerceAtLeast(base.intervalDays + 1)
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
