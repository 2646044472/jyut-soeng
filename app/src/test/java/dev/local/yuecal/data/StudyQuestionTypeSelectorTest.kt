package dev.local.yuecal.data

import dev.local.yuecal.domain.SessionMode
import dev.local.yuecal.domain.StudyQuestionType
import org.junit.Assert.assertEquals
import org.junit.Test

class StudyQuestionTypeSelectorTest {

    @Test
    fun learnModeUsesFillJyutping() {
        assertEquals(
            StudyQuestionType.FillJyutping,
            studyQuestionTypeFor(SessionMode.Learn),
        )
    }

    @Test
    fun reviewModeUsesFillJyutping() {
        assertEquals(
            StudyQuestionType.FillJyutping,
            studyQuestionTypeFor(SessionMode.Review),
        )
    }

    @Test
    fun focusedWordSessionUsesAPronunciationTitle() {
        assertEquals(
            "正音词学习",
            sessionTitle(SessionMode.Learn, "word"),
        )
    }

    @Test
    fun focusedExpressionReviewUsesAnExpressionTitle() {
        assertEquals(
            "表达复习",
            sessionTitle(SessionMode.Review, "expression"),
        )
    }

    @Test
    fun mixedSessionKeepsItsExistingTitle() {
        assertEquals(
            "今日学习",
            sessionTitle(SessionMode.Learn, null),
        )
    }
}
