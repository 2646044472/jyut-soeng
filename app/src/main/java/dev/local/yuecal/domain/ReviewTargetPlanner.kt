package dev.local.yuecal.domain

private const val MIN_EXTRA_REVIEW_ENTRIES = 2
private const val MAX_EXTRA_REVIEW_ENTRIES = 4

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
}
