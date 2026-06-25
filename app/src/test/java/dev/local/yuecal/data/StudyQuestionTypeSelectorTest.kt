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
}
