package dev.local.yuecal.data

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.PreferenceDataStoreFactory
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStoreFile
import dagger.hilt.android.qualifiers.ApplicationContext
import dev.local.yuecal.domain.AppSettings
import javax.inject.Inject
import javax.inject.Singleton
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.map

@Singleton
class AppSettingsStore @Inject constructor(
    @ApplicationContext context: Context,
) {

    private val dataStore: DataStore<Preferences> = PreferenceDataStoreFactory.create(
        produceFile = { context.preferencesDataStoreFile("canto_calibrator_settings.preferences_pb") },
    )

    val settings: Flow<AppSettings> = dataStore.data.map { prefs ->
        AppSettings(
            autoplayAudio = prefs[Keys.AUTOPLAY_AUDIO] ?: true,
            remindersEnabled = prefs[Keys.REMINDERS_ENABLED] ?: true,
            dailyLearnGoal = prefs[Keys.DAILY_LEARN_GOAL] ?: 10,
            builtInSeedVersion = prefs[Keys.BUILTIN_SEED_VERSION] ?: "",
        )
    }

    suspend fun snapshot(): AppSettings = settings.first()

    suspend fun setAutoplayAudio(enabled: Boolean) {
        dataStore.edit { it[Keys.AUTOPLAY_AUDIO] = enabled }
    }

    suspend fun setRemindersEnabled(enabled: Boolean) {
        dataStore.edit { it[Keys.REMINDERS_ENABLED] = enabled }
    }

    suspend fun setDailyLearnGoal(goal: Int) {
        dataStore.edit { it[Keys.DAILY_LEARN_GOAL] = goal.coerceAtLeast(4) }
    }

    suspend fun setBuiltInSeedVersion(version: String) {
        dataStore.edit { it[Keys.BUILTIN_SEED_VERSION] = version }
    }

    private object Keys {
        val AUTOPLAY_AUDIO = booleanPreferencesKey("autoplay_audio")
        val REMINDERS_ENABLED = booleanPreferencesKey("reminders_enabled")
        val DAILY_LEARN_GOAL = intPreferencesKey("daily_learn_goal")
        val BUILTIN_SEED_VERSION = stringPreferencesKey("builtin_seed_version")
    }
}
