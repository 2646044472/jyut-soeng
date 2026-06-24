package dev.local.yuecal.domain

import kotlin.math.roundToInt

private const val MIN_EXTRA_REVIEW_ENTRIES = 2
private const val MAX_EXTRA_REVIEW_ENTRIES = 4
const val REVIEW_SESSION_ENTRY_LIMIT = 50

data class ReviewSessionTargets(
    val wordLimit: Int,
    val expressionLimit: Int,
) {
    val total: Int
        get() = wordLimit + expressionLimit
}

object ReviewTargetPlanner {

    fun targetForToday(
        dueEntries: Int,
        studiedEntries: Int,
    ): Int {
        val studied = studiedEntries.coerceAtLeast(0)
        if (studied == 0) return 0
        return dueEntries.coerceAtLeast(0).coerceAtMost(studied)
    }

    fun extraPracticeTarget(
        studiedEntries: Int,
    ): Int {
        val studied = studiedEntries.coerceAtLeast(0)
        if (studied == 0) return 0
        return minOf(
            studied,
            maxOf(MIN_EXTRA_REVIEW_ENTRIES, studied / 5),
            MAX_EXTRA_REVIEW_ENTRIES,
        )
    }

    fun sessionTarget(
        dueEntries: Int,
        studiedEntries: Int,
        hasDueReviewsToday: Boolean,
    ): Int = if (hasDueReviewsToday) {
        targetForToday(
            dueEntries = dueEntries,
            studiedEntries = studiedEntries,
        )
    } else {
        extraPracticeTarget(
            studiedEntries = studiedEntries,
        )
    }

    fun sessionTargets(
        wordDueEntries: Int,
        wordStudiedEntries: Int,
        expressionDueEntries: Int,
        expressionStudiedEntries: Int,
        hasDueReviewsToday: Boolean,
    ): ReviewSessionTargets {
        val rawWordLimit = sessionTarget(
            dueEntries = wordDueEntries,
            studiedEntries = wordStudiedEntries,
            hasDueReviewsToday = hasDueReviewsToday,
        )
        val rawExpressionLimit = sessionTarget(
            dueEntries = expressionDueEntries,
            studiedEntries = expressionStudiedEntries,
            hasDueReviewsToday = hasDueReviewsToday,
        )
        return capSessionTargets(
            wordLimit = rawWordLimit,
            expressionLimit = rawExpressionLimit,
        )
    }

    fun capSessionTargets(
        wordLimit: Int,
        expressionLimit: Int,
        limit: Int = REVIEW_SESSION_ENTRY_LIMIT,
    ): ReviewSessionTargets {
        val safeWordLimit = wordLimit.coerceAtLeast(0)
        val safeExpressionLimit = expressionLimit.coerceAtLeast(0)
        val safeLimit = limit.coerceAtLeast(0)
        val total = safeWordLimit + safeExpressionLimit
        if (total <= safeLimit) {
            return ReviewSessionTargets(
                wordLimit = safeWordLimit,
                expressionLimit = safeExpressionLimit,
            )
        }
        if (safeLimit == 0) {
            return ReviewSessionTargets(wordLimit = 0, expressionLimit = 0)
        }
        if (safeWordLimit == 0) {
            return ReviewSessionTargets(
                wordLimit = 0,
                expressionLimit = safeExpressionLimit.coerceAtMost(safeLimit),
            )
        }
        if (safeExpressionLimit == 0) {
            return ReviewSessionTargets(
                wordLimit = safeWordLimit.coerceAtMost(safeLimit),
                expressionLimit = 0,
            )
        }

        var cappedWordLimit = (safeLimit * (safeWordLimit.toDouble() / total))
            .roundToInt()
            .coerceIn(1, minOf(safeWordLimit, safeLimit))
        var cappedExpressionLimit = safeLimit - cappedWordLimit

        if (cappedExpressionLimit == 0 && safeLimit > 1) {
            cappedExpressionLimit = 1
            cappedWordLimit -= 1
        }
        if (cappedExpressionLimit > safeExpressionLimit) {
            val overflow = cappedExpressionLimit - safeExpressionLimit
            cappedExpressionLimit = safeExpressionLimit
            cappedWordLimit = (cappedWordLimit + overflow).coerceAtMost(safeWordLimit)
        }
        if (cappedWordLimit > safeWordLimit) {
            val overflow = cappedWordLimit - safeWordLimit
            cappedWordLimit = safeWordLimit
            cappedExpressionLimit = (cappedExpressionLimit + overflow).coerceAtMost(safeExpressionLimit)
        }

        return ReviewSessionTargets(
            wordLimit = cappedWordLimit,
            expressionLimit = cappedExpressionLimit,
        )
    }
}
