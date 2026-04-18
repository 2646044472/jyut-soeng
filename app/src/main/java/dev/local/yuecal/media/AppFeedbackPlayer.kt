package dev.local.yuecal.media

import android.media.AudioManager
import android.media.ToneGenerator
import android.os.Handler
import android.os.Looper

object AppFeedbackPlayer {

    private data class ToneStep(
        val tone: Int,
        val durationMs: Int,
        val delayMs: Long = 0,
    )

    private val toneGenerator = ToneGenerator(AudioManager.STREAM_NOTIFICATION, 35)
    private val handler = Handler(Looper.getMainLooper())
    private var sequenceToken: Long = 0L

    fun playCorrect() {
        playSequence(
            ToneStep(
                tone = ToneGenerator.TONE_PROP_BEEP2,
                durationMs = 70,
            ),
            ToneStep(
                tone = ToneGenerator.TONE_PROP_ACK,
                durationMs = 95,
                delayMs = 90,
            ),
        )
    }

    fun playWrong() {
        playSequence(
            ToneStep(
                tone = ToneGenerator.TONE_PROP_NACK,
                durationMs = 130,
            ),
        )
    }

    @Synchronized
    private fun playSequence(vararg steps: ToneStep) {
        sequenceToken += 1
        val currentToken = sequenceToken
        steps.forEach { step ->
            handler.postDelayed(
                {
                    if (sequenceToken == currentToken) {
                        toneGenerator.startTone(step.tone, step.durationMs)
                    }
                },
                step.delayMs,
            )
        }
    }
}
