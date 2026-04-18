package dev.local.yuecal.media

import android.media.AudioManager
import android.media.ToneGenerator

object AppFeedbackPlayer {

    private val toneGenerator = ToneGenerator(AudioManager.STREAM_NOTIFICATION, 80)

    fun playCorrect() {
        toneGenerator.startTone(ToneGenerator.TONE_PROP_ACK, 140)
    }

    fun playWrong() {
        toneGenerator.startTone(ToneGenerator.TONE_CDMA_SOFT_ERROR_LITE, 180)
    }
}
