package dev.local.yuecal.media

import android.content.Context
import android.os.Handler
import android.os.Looper
import android.speech.tts.TextToSpeech

class CantoneseSentenceSpeaker(context: Context) {
    private val mainHandler = Handler(Looper.getMainLooper())
    private var engine: TextToSpeech? = null
    private var ready = false
    private var unavailable = false
    private var closed = false
    private var pending: Pair<String, () -> Unit>? = null

    init {
        try {
            engine = TextToSpeech(context.applicationContext) { status ->
                mainHandler.post {
                    if (!closed) {
                        val tts = engine
                        val voice = if (status == TextToSpeech.SUCCESS) {
                            val voices = runCatching { tts?.voices.orEmpty() }.getOrDefault(emptySet())
                            voices.firstOrNull { it.locale.language == "yue" }
                                ?: voices.firstOrNull { it.locale.language == "zh" && it.locale.country == "HK" }
                        } else null
                        ready = tts != null && voice != null &&
                            runCatching { tts.setVoice(voice) == TextToSpeech.SUCCESS }.getOrDefault(false)
                        unavailable = !ready
                        pending?.let { (text, onUnavailable) ->
                            pending = null
                            speak(text, onUnavailable)
                        }
                    }
                }
            }
        } catch (_: Exception) {
            unavailable = true
        }
    }

    fun speak(text: String, onUnavailable: () -> Unit) {
        if (closed || unavailable) {
            onUnavailable()
            return
        }
        if (!ready) {
            pending = text to onUnavailable
            return
        }
        if (engine?.speak(text, TextToSpeech.QUEUE_FLUSH, null, "sentence") != TextToSpeech.SUCCESS) {
            onUnavailable()
        }
    }

    fun close() {
        closed = true
        pending = null
        engine?.stop()
        engine?.shutdown()
        engine = null
    }
}
