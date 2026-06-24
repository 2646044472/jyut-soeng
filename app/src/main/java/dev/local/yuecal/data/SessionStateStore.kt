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

    suspend fun read(mode: SessionMode): PersistedSessionState? {
        val raw = dataStore.data.first()[keyFor(mode)] ?: return null
        return runCatching {
            json.decodeFromString<PersistedSessionState>(raw)
        }.getOrNull()
    }

    suspend fun save(mode: SessionMode, state: PersistedSessionState) {
        dataStore.edit { prefs ->
            prefs[keyFor(mode)] = json.encodeToString(PersistedSessionState.serializer(), state)
        }
    }

    suspend fun clear(mode: SessionMode) {
        dataStore.edit { prefs ->
            prefs.remove(keyFor(mode))
        }
    }

    private fun keyFor(mode: SessionMode) = when (mode) {
        SessionMode.Learn -> Keys.LEARN_SESSION_STATE
        SessionMode.Review -> Keys.REVIEW_SESSION_STATE
    }

    private object Keys {
        val LEARN_SESSION_STATE = stringPreferencesKey("learn_session_state")
        val REVIEW_SESSION_STATE = stringPreferencesKey("review_session_state")
    }
}
