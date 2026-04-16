package dev.local.yuecal.ui

import android.net.Uri
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import dev.local.yuecal.data.AppSettingsStore
import dev.local.yuecal.data.CalibratorRepository
import dev.local.yuecal.data.GitHubSources
import dev.local.yuecal.domain.AppSettings
import dev.local.yuecal.domain.CalibrationEntry
import dev.local.yuecal.domain.DashboardSummary
import dev.local.yuecal.domain.StudyQuestion
import dev.local.yuecal.domain.StudySession
import dev.local.yuecal.work.AppWorkScheduler
import javax.inject.Inject
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class TodayUiState(
    val dashboard: DashboardSummary = DashboardSummary(),
)

data class LibraryUiState(
    val entries: List<CalibrationEntry> = emptyList(),
    val lastMessage: String? = null,
)

data class SearchUiState(
    val query: String = "",
    val results: List<CalibrationEntry> = emptyList(),
)

data class ProfileUiState(
    val settings: AppSettings = AppSettings(),
    val dashboard: DashboardSummary = DashboardSummary(),
    val githubRepoUrl: String = GitHubSources.REPO_WEB_URL,
    val githubReleasesUrl: String = GitHubSources.RELEASES_URL,
    val lastMessage: String? = null,
)

data class SessionUiState(
    val isLoading: Boolean = true,
    val session: StudySession? = null,
    val currentIndex: Int = 0,
    val currentQuestion: StudyQuestion? = null,
    val correctCount: Int = 0,
    val lastFeedback: String? = null,
    val autoplayAudio: Boolean = true,
)

@HiltViewModel
class TodayViewModel @Inject constructor(
    repository: CalibratorRepository,
) : ViewModel() {

    val uiState: StateFlow<TodayUiState> = repository.dashboard.map(::TodayUiState).stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5_000),
        initialValue = TodayUiState(),
    )
}

@HiltViewModel
class LibraryViewModel @Inject constructor(
    private val repository: CalibratorRepository,
) : ViewModel() {

    private val message = MutableStateFlow<String?>(null)

    val uiState: StateFlow<LibraryUiState> = combine(
        repository.libraryEntries,
        message,
    ) { entries, lastMessage ->
        LibraryUiState(entries = entries, lastMessage = lastMessage)
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5_000),
        initialValue = LibraryUiState(),
    )

    fun importFromUri(uri: Uri) {
        viewModelScope.launch {
            runCatching { repository.importFromUri(uri) }
                .onSuccess { result ->
                    message.value = "已导入 ${result.importedCount} 条本地内容。"
                }
                .onFailure {
                    message.value = "导入失败：${it.message ?: "未知错误"}"
                }
        }
    }

    fun playAudio(assetPath: String?) {
        viewModelScope.launch {
            repository.playAudio(assetPath)
        }
    }

    fun clearMessage() {
        message.value = null
    }
}

@HiltViewModel
@OptIn(ExperimentalCoroutinesApi::class)
class SearchViewModel @Inject constructor(
    private val repository: CalibratorRepository,
) : ViewModel() {

    private val query = MutableStateFlow("")

    val uiState: StateFlow<SearchUiState> = query.flatMapLatest { currentQuery ->
        repository.searchEntries(currentQuery).map { results ->
            SearchUiState(query = currentQuery, results = results)
        }
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5_000),
        initialValue = SearchUiState(),
    )

    fun updateQuery(value: String) {
        query.value = value
    }

    fun playAudio(assetPath: String?) {
        viewModelScope.launch {
            repository.playAudio(assetPath)
        }
    }
}

@HiltViewModel
class ProfileViewModel @Inject constructor(
    private val repository: CalibratorRepository,
    private val settingsStore: AppSettingsStore,
    private val workScheduler: AppWorkScheduler,
) : ViewModel() {

    private val message = MutableStateFlow<String?>(null)

    val uiState: StateFlow<ProfileUiState> = combine(
        repository.settings,
        repository.dashboard,
        message,
    ) { settings, dashboard, lastMessage ->
        ProfileUiState(
            settings = settings,
            dashboard = dashboard,
            githubRepoUrl = GitHubSources.REPO_WEB_URL,
            githubReleasesUrl = GitHubSources.RELEASES_URL,
            lastMessage = lastMessage,
        )
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5_000),
        initialValue = ProfileUiState(),
    )

    fun setAutoplay(enabled: Boolean) {
        viewModelScope.launch {
            settingsStore.setAutoplayAudio(enabled)
        }
    }

    fun setReminders(enabled: Boolean) {
        viewModelScope.launch {
            workScheduler.setRemindersEnabled(enabled)
        }
    }

    fun updateDailyGoal(goal: Int) {
        viewModelScope.launch {
            settingsStore.setDailyGoal(goal)
        }
    }

    fun refreshBuiltinContent() {
        viewModelScope.launch {
            runCatching { workScheduler.refreshBuiltInContent() }
                .onSuccess { message.value = "已重新导入内置内容。" }
                .onFailure { message.value = "重导失败：${it.message ?: "未知错误"}" }
        }
    }

    fun importFromGitHub() {
        viewModelScope.launch {
            runCatching { repository.importFromGitHub() }
                .onSuccess { result ->
                    message.value = "已从 GitHub 导入 ${result.importedCount} 条内容，版本 ${result.version}。"
                }
                .onFailure { throwable ->
                    message.value = "GitHub 更新失败：${throwable.message ?: "仓库内容暂不可用"}"
                }
        }
    }

    fun clearMessage() {
        message.value = null
    }
}

@HiltViewModel
class SessionViewModel @Inject constructor(
    private val repository: CalibratorRepository,
) : ViewModel() {

    private val mutableState = MutableStateFlow(SessionUiState())
    val uiState: StateFlow<SessionUiState> = mutableState

    private var questionStartMillis: Long = 0

    init {
        viewModelScope.launch {
            repository.settings.collect { settings ->
                mutableState.update { it.copy(autoplayAudio = settings.autoplayAudio) }
            }
        }
        loadSession()
    }

    fun loadSession() {
        viewModelScope.launch {
            mutableState.value = SessionUiState(isLoading = true)
            val session = repository.buildSession()
            questionStartMillis = System.currentTimeMillis()
            mutableState.value = SessionUiState(
                isLoading = false,
                session = session,
                currentIndex = 0,
                currentQuestion = session.questions.firstOrNull(),
                correctCount = 0,
                autoplayAudio = mutableState.value.autoplayAudio,
            )
        }
    }

    fun playCurrentAudio() {
        val current = uiState.value.currentQuestion ?: return
        viewModelScope.launch {
            repository.playAudio(current.audioAsset)
        }
    }

    fun submitAnswer(answer: String) {
        val session = uiState.value.session ?: return
        val currentQuestion = uiState.value.currentQuestion ?: return
        viewModelScope.launch {
            val responseMillis = System.currentTimeMillis() - questionStartMillis
            val outcome = repository.submitAnswer(
                sessionId = session.sessionId,
                question = currentQuestion,
                selectedAnswer = answer,
                responseMillis = responseMillis,
            )
            val nextIndex = uiState.value.currentIndex + 1
            val nextQuestion = session.questions.getOrNull(nextIndex)
            questionStartMillis = System.currentTimeMillis()
            mutableState.value = uiState.value.copy(
                currentIndex = nextIndex,
                currentQuestion = nextQuestion,
                correctCount = uiState.value.correctCount + if (outcome.isCorrect) 1 else 0,
                lastFeedback = if (outcome.isCorrect) {
                    "正确：${outcome.correctAnswer}"
                } else {
                    "答案是 ${outcome.correctAnswer}"
                },
            )
        }
    }
}
