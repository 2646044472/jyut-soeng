package dev.local.yuecal.data

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.PreferenceDataStoreFactory
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStoreFile
import dagger.hilt.android.qualifiers.ApplicationContext
import dev.local.yuecal.domain.SessionMode
import dev.local.yuecal.domain.StudyQuestion
import dev.local.yuecal.domain.StudySession
import javax.inject.Inject
import javax.inject.Singleton
import kotlinx.coroutines.flow.first
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json

@Serializable
data class PersistedSessionState(
    val session: StudySession,
    val currentIndex: Int,
    val round: Int,
    val retryQuestionCount: Int,
    val totalQuestionCount: Int,
    val correctCount: Int,
    val feedback: PersistedSessionFeedback? = null,
    val currentRoundMistakes: List<StudyQuestion> = emptyList(),
)

@Serializable
data class PersistedSessionFeedback(
    val isCorrect: Boolean,
    val correctAnswer: String,
    val userAnswer: String,
)

@Singleton
class SessionStateStore @Inject constructor(
    @ApplicationContext context: Context,
    private val json: Json,
) {

    private val dataStore: DataStore<Preferences> = PreferenceDataStoreFactory.create(
        produceFile = { context.preferencesDataStoreFile("canto_calibrator_session.preferences_pb") },
    )

    suspend fun read(mode: SessionMode, entryType: String? = null): PersistedSessionState? {
        val raw = dataStore.data.first()[keyFor(mode, entryType)] ?: return null
        return runCatching {
            json.decodeFromString<PersistedSessionState>(raw)
        }.getOrNull()
    }

    suspend fun save(mode: SessionMode, entryType: String? = null, state: PersistedSessionState) {
        dataStore.edit { prefs ->
            prefs[keyFor(mode, entryType)] = json.encodeToString(PersistedSessionState.serializer(), state)
        }
    }

    suspend fun clear(mode: SessionMode, entryType: String? = null) {
        dataStore.edit { prefs ->
            prefs.remove(keyFor(mode, entryType))
        }
    }

    private fun keyFor(mode: SessionMode, entryType: String?) = when (mode) {
        SessionMode.Learn -> when (entryType) {
            "word" -> Keys.LEARN_WORD_SESSION_STATE
            "expression" -> Keys.LEARN_EXPRESSION_SESSION_STATE
            else -> Keys.LEARN_SESSION_STATE
        }
        SessionMode.Review -> when (entryType) {
            "word" -> Keys.REVIEW_WORD_SESSION_STATE
            "expression" -> Keys.REVIEW_EXPRESSION_SESSION_STATE
            else -> Keys.REVIEW_SESSION_STATE
        }
    }

    private object Keys {
        val LEARN_SESSION_STATE = stringPreferencesKey("learn_session_state")
        val LEARN_WORD_SESSION_STATE = stringPreferencesKey("learn_word_session_state")
        val LEARN_EXPRESSION_SESSION_STATE = stringPreferencesKey("learn_expression_session_state")
        val REVIEW_SESSION_STATE = stringPreferencesKey("review_session_state")
        val REVIEW_WORD_SESSION_STATE = stringPreferencesKey("review_word_session_state")
        val REVIEW_EXPRESSION_SESSION_STATE = stringPreferencesKey("review_expression_session_state")
    }
}
