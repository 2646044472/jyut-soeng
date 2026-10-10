package dev.local.yuecal.ui

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.assertDoesNotExist
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import dev.local.yuecal.domain.CalibrationEntry
import dev.local.yuecal.domain.SessionMode
import dev.local.yuecal.domain.StudyQuestion
import dev.local.yuecal.domain.StudyQuestionType
import dev.local.yuecal.domain.StudySession
import dev.local.yuecal.ui.theme.CantoCalibratorTheme
import org.junit.Assert.assertEquals
import org.junit.Rule
import org.junit.Test

class SentenceReaderScreenTest {

    @get:Rule val composeRule = createComposeRule()

    @Test
    fun jyutpingIsVisibleAndMeaningIsRevealedOnlyOnRequest() {
        var spokenText: String? = null
        val sentence = CalibrationEntry(
            id = "test-sentence",
            displayText = "測試原句",
            promptText = "",
            answerJyutping = "cak1 si3 jyun4 geoi3",
            gloss = "测试中文意思",
            notes = "",
            usageTip = "测试使用场景",
            exampleSentence = "",
            exampleTranslation = "",
            entryType = "sentence",
            category = "测试",
            groupId = "test-sentence",
            tone = 0,
            audioAsset = null,
            sourceLabel = "test",
            statusLabel = "",
        )

        composeRule.setContent {
            CantoCalibratorTheme {
                SentenceReaderScreen(
                    SentenceReaderUiState(listOf(sentence), totalSentenceCount = 1),
                    onSpeak = { spokenText = it },
                    onStartLearning = {},
                )
            }
        }

        composeRule.onNodeWithText("cak1").assertIsDisplayed()
        composeRule.onNodeWithText("si3").assertIsDisplayed()
        composeRule.onNodeWithText("jyun4").assertIsDisplayed()
        composeRule.onNodeWithText("geoi3").assertIsDisplayed()
        composeRule.onNodeWithText("測").assertIsDisplayed()
        composeRule.onNodeWithText("試").assertIsDisplayed()
        composeRule.onNodeWithText("原").assertIsDisplayed()
        composeRule.onNodeWithText("句").assertIsDisplayed()
        composeRule.onNodeWithText("测试中文意思").assertDoesNotExist()
        composeRule.onNodeWithText("测试使用场景").assertDoesNotExist()

        composeRule.onNodeWithContentDescription("播放粤语读音").performClick()
        composeRule.runOnIdle { assertEquals("測試原句", spokenText) }

        composeRule.onNodeWithText("查看中文意思").performClick()
        composeRule.onNodeWithText("测试中文意思").assertIsDisplayed()
        composeRule.onNodeWithText("测试使用场景").assertIsDisplayed()

        composeRule.onNodeWithText("收起中文意思").performClick()
        composeRule.onNodeWithText("测试中文意思").assertDoesNotExist()
    }

    @Test
    fun sentenceReaderKeepsMeaningToggleWhenGlossIsMissing() {
        val sentence = CalibrationEntry(
            id = "test-sentence-without-gloss",
            displayText = "測試原句",
            promptText = "",
            answerJyutping = "cak1 si3 jyun4 geoi3",
            gloss = "",
            notes = "",
            usageTip = "",
            exampleSentence = "",
            exampleTranslation = "",
            entryType = "sentence",
            category = "测试",
            groupId = "test-sentence-without-gloss",
            tone = 0,
            audioAsset = null,
            sourceLabel = "test",
            statusLabel = "",
        )

        composeRule.setContent {
            CantoCalibratorTheme {
                SentenceReaderScreen(
                    SentenceReaderUiState(listOf(sentence), totalSentenceCount = 1),
                    onSpeak = {},
                    onStartLearning = {},
                )
            }
        }

        composeRule.onNodeWithText("查看中文意思").assertIsDisplayed().performClick()
        composeRule.onNodeWithText("这条句子的中文意思暂未录入。").assertIsDisplayed()
    }

    @Test
    fun sentenceStudyShowsMeaningAndPreviousNextEvenWithoutGloss() {
        val question = StudyQuestion(
            entryId = "study-sentence",
            type = StudyQuestionType.ExpressionCard,
            displayText = "測試句子",
            promptText = "",
            answerJyutping = "cak1 si3 geoi3 zi2",
            gloss = "",
            options = emptyList(),
            audioAsset = null,
            category = "测试",
            notes = "",
            usageTip = "",
            exampleSentence = "",
            exampleTranslation = "",
            sourceLabel = "test",
        )
        val session = StudySession(
            sessionId = "test-session",
            mode = SessionMode.Learn,
            title = "句子学习",
            questions = listOf(
                question.copy(displayText = "第一句"),
                question.copy(entryId = "study-sentence-2", displayText = "第二句"),
                question.copy(entryId = "study-sentence-3", displayText = "第三句"),
            ),
        )
        var currentIndex by mutableIntStateOf(1)

        composeRule.setContent {
            CantoCalibratorTheme {
                SentenceStudyScreen(
                    state = SentenceStudyUiState(
                        isLoading = false,
                        session = session,
                        currentIndex = currentIndex,
                    ),
                    onPrevious = { currentIndex = (currentIndex - 1).coerceAtLeast(0) },
                    onNext = { currentIndex = (currentIndex + 1).coerceAtMost(session.questions.size) },
                    onDone = {},
                )
            }
        }

        composeRule.onNodeWithText("第二句").assertIsDisplayed()
        composeRule.onNodeWithText("上一句").assertIsDisplayed().performClick()
        composeRule.onNodeWithText("第一句").assertIsDisplayed()
        composeRule.onNodeWithText("下一句").assertIsDisplayed().performClick()
        composeRule.onNodeWithText("第二句").assertIsDisplayed()
        composeRule.onNodeWithText("展开查看句子意思").performClick()
        composeRule.onNodeWithText("这条句子的中文意思暂未录入。").assertIsDisplayed()
    }
}
