package dev.local.yuecal.domain

import org.junit.Assert.assertEquals
import org.junit.Test

class ReviewTargetPlannerTest {

    @Test
    fun returnsZeroWhenNothingHasBeenStudied() {
        assertEquals(0, ReviewTargetPlanner.targetForToday(dueEntries = 5, studiedEntries = 0))
    }

    @Test
    fun dailyTargetOnlyCountsAlreadyDueReviews() {
        assertEquals(10, ReviewTargetPlanner.targetForToday(dueEntries = 10, studiedEntries = 20))
    }

    @Test
    fun dailyTargetStaysZeroWhenNothingIsDueYet() {
        assertEquals(0, ReviewTargetPlanner.targetForToday(dueEntries = 0, studiedEntries = 8))
    }

    @Test
    fun neverExceedsDueItemsOrAlreadyStudiedEntries() {
        assertEquals(2, ReviewTargetPlanner.targetForToday(dueEntries = 2, studiedEntries = 3))
    }

    @Test
    fun extraPracticeOnlyUsesAlreadyStudiedEntries() {
        assertEquals(2, ReviewTargetPlanner.extraPracticeTarget(studiedEntries = 8))
    }

    @Test
    fun extraPracticeStaysWithinSmallBonusWindow() {
        assertEquals(4, ReviewTargetPlanner.extraPracticeTarget(studiedEntries = 40))
    }

    @Test
    fun sessionTargetDoesNotMixBonusItemsIntoDueReviewRounds() {
        assertEquals(
            0,
            ReviewTargetPlanner.sessionTarget(
                dueEntries = 0,
                studiedEntries = 8,
                hasDueReviewsToday = true,
            ),
        )
    }
}
