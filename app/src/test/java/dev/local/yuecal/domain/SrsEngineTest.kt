package dev.local.yuecal.domain

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class SrsEngineTest {

    @Test
    fun perfectAnswerStartsInterval() {
        val next = Sm2Scheduler.next(current = null, quality = 5, today = 100)
        assertEquals(1, next.repetitions)
        assertEquals(1, next.intervalDays)
        assertEquals(101, next.nextReviewEpochDay)
        assertEquals(1, next.totalCorrect)
        assertEquals(1, next.totalAttempts)
    }

    @Test
    fun failedAnswerResetsSchedule() {
        val current = EntryProgress(
            repetitions = 3,
            intervalDays = 8,
            easeFactor = 2.5,
            nextReviewEpochDay = 120,
            totalCorrect = 3,
            totalAttempts = 3,
            streak = 3,
        )
        val next = Sm2Scheduler.next(current = current, quality = 2, today = 100)
        assertEquals(0, next.repetitions)
        assertEquals(1, next.intervalDays)
        assertEquals(101, next.nextReviewEpochDay)
        assertEquals(3, next.totalCorrect)
        assertEquals(4, next.totalAttempts)
        assertEquals(0, next.streak)
    }

    @Test
    fun zeroRepetitionProgressStaysInLearningQueue() {
        val progress = EntryProgress(
            repetitions = 0,
            intervalDays = 1,
            nextReviewEpochDay = 100,
        )
        assertTrue(!progress.isInReviewQueue())
        assertTrue(progress.needsReviewToday(today = 100))
        assertEquals("待巩固", progress.statusLabel(today = 100))
    }

    @Test
    fun scheduledLearningProgressStillCountsTowardUpcomingReviewWindow() {
        val progress = EntryProgress(
            repetitions = 0,
            intervalDays = 1,
            nextReviewEpochDay = 101,
        )
        assertTrue(!progress.needsReviewToday(today = 100))
        assertTrue(progress.needsReviewBy(day = 101))
        assertEquals("学习中", progress.statusLabel(today = 100))
    }

    @Test
    fun firstCorrectAnswerGraduatesEntryToReviewQueue() {
        val next = Sm2Scheduler.next(
            current = EntryProgress(
                repetitions = 0,
                intervalDays = 1,
                nextReviewEpochDay = 100,
            ),
            quality = 5,
            today = 100,
        )
        assertTrue(next.isInReviewQueue())
        assertEquals("已排程", next.statusLabel(today = 100))
    }

    @Test
    fun judgingRewardsFastCorrectAnswers() {
        assertEquals(
            5,
            JudgingEngine.score(
                isCorrect = true,
                responseMillis = 1500,
                questionType = StudyQuestionType.FillJyutping,
            ),
        )
        assertEquals(
            4,
            JudgingEngine.score(
                isCorrect = true,
                responseMillis = 6000,
                questionType = StudyQuestionType.FillJyutping,
            ),
        )
        assertEquals(
            1,
            JudgingEngine.score(
                isCorrect = false,
                responseMillis = 800,
                questionType = StudyQuestionType.MultipleChoice,
            ),
        )
        assertTrue(Sm2Scheduler.next(null, 5).easeFactor >= 2.5)
    }
}
