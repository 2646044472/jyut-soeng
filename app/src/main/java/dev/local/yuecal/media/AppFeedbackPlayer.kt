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

    private val toneGenerator = ToneGenerator(AudioManager.STREAM_MUSIC, 22)
    private val handler = Handler(Looper.getMainLooper())
    private var sequenceToken: Long = 0L

    fun playCorrect() {
        playSequence(
            ToneStep(
                tone = ToneGenerator.TONE_PROP_BEEP,
                durationMs = 35,
            ),
            ToneStep(
                tone = ToneGenerator.TONE_PROP_BEEP2,
                durationMs = 45,
                delayMs = 45,
            ),
            ToneStep(
                tone = ToneGenerator.TONE_PROP_ACK,
                durationMs = 60,
                delayMs = 100,
            ),
        )
    }

    fun playWrong() {
        playSequence(
            ToneStep(
                tone = ToneGenerator.TONE_PROP_BEEP2,
                durationMs = 45,
            ),
            ToneStep(
                tone = ToneGenerator.TONE_PROP_NACK,
                durationMs = 65,
                delayMs = 60,
            ),
        )
    }

    @Synchronized
    private fun playSequence(vararg steps: ToneStep) {
        sequenceToken += 1
        val currentToken = sequenceToken
        handler.removeCallbacksAndMessages(null)
        toneGenerator.stopTone()
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
