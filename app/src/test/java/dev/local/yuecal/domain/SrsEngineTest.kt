package dev.local.yuecal.domain

import java.time.Instant
import java.time.LocalDate
import java.time.ZoneId
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
    fun earlyReviewIntervalsStayLightweight() {
        val first = Sm2Scheduler.next(current = null, quality = 5, today = 100)
        val second = Sm2Scheduler.next(current = first, quality = 5, today = 101)
        val third = Sm2Scheduler.next(current = second, quality = 5, today = 103)

        assertEquals(1, first.intervalDays)
        assertEquals(2, second.intervalDays)
        assertEquals(3, third.intervalDays)
        assertEquals(103, second.nextReviewEpochDay)
        assertEquals(106, third.nextReviewEpochDay)
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

    @Test
    fun newLearningWindowCoversExactlyOneLocalDay() {
        val zone = ZoneId.of("Asia/Shanghai")
        val day = LocalDate.of(2026, 9, 11)
        val start = startOfDayEpochMillis(day, zone)
        val end = startOfDayEpochMillis(day.plusDays(1), zone)

        assertEquals(day, Instant.ofEpochMilli(start).atZone(zone).toLocalDate())
        assertEquals(day.plusDays(1), Instant.ofEpochMilli(end).atZone(zone).toLocalDate())
        assertEquals(24 * 60 * 60 * 1000L, end - start)
    }
}
