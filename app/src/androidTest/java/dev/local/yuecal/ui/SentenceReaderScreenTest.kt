package dev.local.yuecal.ui

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import dev.local.yuecal.domain.CalibrationEntry
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
                )
            }
        }

        composeRule.onNodeWithText("測試原句").assertIsDisplayed()
        composeRule.onNodeWithText("cak1 si3 jyun4 geoi3").assertIsDisplayed()
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
}
