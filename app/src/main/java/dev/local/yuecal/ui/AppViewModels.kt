package dev.local.yuecal.ui

import android.net.Uri
import dev.local.yuecal.BuildConfig
import androidx.lifecycle.ViewModel
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import dev.local.yuecal.data.AppSettingsStore
import dev.local.yuecal.data.CalibratorRepository
import dev.local.yuecal.data.GitHubSources
import dev.local.yuecal.data.PersistedSessionFeedback
import dev.local.yuecal.data.PersistedSessionState
import dev.local.yuecal.data.SessionStateStore
import dev.local.yuecal.domain.AppSettings
import dev.local.yuecal.domain.AppReleaseInfo
import dev.local.yuecal.domain.CalibrationEntry
import dev.local.yuecal.domain.DashboardSummary
import dev.local.yuecal.domain.SessionMode
import dev.local.yuecal.domain.StudyQuestion
import dev.local.yuecal.domain.StudySession
import dev.local.yuecal.media.AppFeedbackPlayer
import dev.local.yuecal.work.AppWorkScheduler
import java.util.UUID
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
    val currentAppVersion: String = BuildConfig.VERSION_NAME,
    val githubRepoUrl: String = GitHubSources.REPO_WEB_URL,
    val githubReleasesUrl: String = GitHubSources.RELEASES_URL,
    val latestAppVersion: String? = null,
    val latestAppReleaseUrl: String = GitHubSources.RELEASES_URL,
    val isCheckingAppUpdate: Boolean = false,
    val isDownloadingAppUpdate: Boolean = false,
    val hasAppUpdate: Boolean = false,
    val pendingApkInstallPath: String? = null,
    val lastMessage: String? = null,
)

data class SessionUiState(
    val isLoading: Boolean = true,
    val session: StudySession? = null,
    val currentIndex: Int = 0,
    val currentQuestion: StudyQuestion? = null,
    val round: Int = 1,
    val retryQuestionCount: Int = 0,
    val totalQuestionCount: Int = 0,
    val correctCount: Int = 0,
    val answerInput: String = "",
    val feedback: SessionFeedback? = null,
    val autoplayAudio: Boolean = true,
)

data class SessionFeedback(
    val isCorrect: Boolean,
    val correctAnswer: String,
    val userAnswer: String,
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
    private val appUpdateState = MutableStateFlow(AppUpdateUiState())
    private var latestRelease: AppReleaseInfo? = null

    val uiState: StateFlow<ProfileUiState> = combine(
        repository.settings,
        repository.dashboard,
        appUpdateState,
        message,
    ) { settings, dashboard, appUpdate, lastMessage ->
        ProfileUiState(
            settings = settings,
            dashboard = dashboard,
            currentAppVersion = BuildConfig.VERSION_NAME,
            githubRepoUrl = GitHubSources.REPO_WEB_URL,
            githubReleasesUrl = GitHubSources.RELEASES_URL,
            latestAppVersion = appUpdate.latestVersion,
            latestAppReleaseUrl = appUpdate.releaseUrl,
            isCheckingAppUpdate = appUpdate.isChecking,
            isDownloadingAppUpdate = appUpdate.isDownloading,
            hasAppUpdate = appUpdate.hasUpdate,
            pendingApkInstallPath = appUpdate.pendingApkInstallPath,
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

    fun updateDailyLearnGoal(goal: Int) {
        viewModelScope.launch {
            settingsStore.setDailyLearnGoal(goal)
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

    fun checkAppUpdate() {
        viewModelScope.launch {
            appUpdateState.update { it.copy(isChecking = true) }
            runCatching { repository.fetchLatestAppRelease() }
                .onSuccess { release ->
                    latestRelease = release
                    val hasUpdate = isVersionNewer(
                        latest = release.version,
                        current = BuildConfig.VERSION_NAME,
                    )
                    appUpdateState.update {
                        it.copy(
                            latestVersion = release.version,
                            releaseUrl = release.releaseUrl,
                            isChecking = false,
                            hasUpdate = hasUpdate,
                        )
                    }
                    message.value = if (hasUpdate) {
                        "发现新版本 ${release.version}，可以直接下载覆盖安装。"
                    } else {
                        "当前已经是最新版本 ${BuildConfig.VERSION_NAME}。"
                    }
                }
                .onFailure { throwable ->
                    appUpdateState.update { it.copy(isChecking = false) }
                    message.value = "检查应用更新失败：${throwable.message ?: "GitHub Release 暂不可用"}"
                }
        }
    }

    fun downloadAppUpdate() {
        viewModelScope.launch {
            val release = latestRelease ?: runCatching { repository.fetchLatestAppRelease() }
                .onSuccess { latestRelease = it }
                .getOrElse { throwable ->
                    message.value = "读取最新版本失败：${throwable.message ?: "GitHub Release 暂不可用"}"
                    return@launch
                }
            appUpdateState.update {
                it.copy(
                    latestVersion = release.version,
                    releaseUrl = release.releaseUrl,
                    hasUpdate = isVersionNewer(release.version, BuildConfig.VERSION_NAME),
                    isDownloading = true,
                )
            }
            runCatching { repository.downloadAppRelease(release) }
                .onSuccess { apkFile ->
                    appUpdateState.update {
                        it.copy(
                            isDownloading = false,
                            pendingApkInstallPath = apkFile.absolutePath,
                        )
                    }
                    message.value = "新版本 APK 已下载完成，准备打开系统安装器。"
                }
                .onFailure { throwable ->
                    appUpdateState.update { it.copy(isDownloading = false) }
                    message.value = "下载更新失败：${throwable.message ?: "网络暂不可用"}"
                }
        }
    }

    fun markApkInstallHandled() {
        appUpdateState.update { it.copy(pendingApkInstallPath = null) }
    }

    fun clearMessage() {
        message.value = null
    }

    private fun isVersionNewer(latest: String, current: String): Boolean {
        val latestParts = latest.split('.').mapNotNull(String::toIntOrNull)
        val currentParts = current.split('.').mapNotNull(String::toIntOrNull)
        val maxLength = maxOf(latestParts.size, currentParts.size)
        for (index in 0 until maxLength) {
            val latestPart = latestParts.getOrElse(index) { 0 }
            val currentPart = currentParts.getOrElse(index) { 0 }
            if (latestPart != currentPart) {
                return latestPart > currentPart
            }
        }
        return false
    }
}

private data class AppUpdateUiState(
    val latestVersion: String? = null,
    val releaseUrl: String = GitHubSources.RELEASES_URL,
    val isChecking: Boolean = false,
    val isDownloading: Boolean = false,
    val hasUpdate: Boolean = false,
    val pendingApkInstallPath: String? = null,
)

@HiltViewModel
class SessionViewModel @Inject constructor(
    private val repository: CalibratorRepository,
    private val sessionStateStore: SessionStateStore,
    savedStateHandle: SavedStateHandle,
) : ViewModel() {

    private val mutableState = MutableStateFlow(SessionUiState())
    val uiState: StateFlow<SessionUiState> = mutableState

    private var questionStartMillis: Long = 0
    private val currentRoundMistakes = linkedMapOf<String, StudyQuestion>()
    private val mode: SessionMode = when (savedStateHandle.get<String>("mode")) {
        "review" -> SessionMode.Review
        else -> SessionMode.Learn
    }

    init {
        viewModelScope.launch {
            repository.settings.collect { settings ->
                mutableState.update { it.copy(autoplayAudio = settings.autoplayAudio) }
            }
        }
        restoreOrLoadSession()
    }

    fun loadSession() {
        viewModelScope.launch {
            sessionStateStore.clear(mode)
            buildFreshSession()
        }
    }

    fun playCurrentAudio() {
        val current = uiState.value.currentQuestion ?: return
        viewModelScope.launch {
            repository.playAudio(current.audioAsset)
        }
    }

    fun updateAnswerInput(answer: String) {
        mutableState.update { it.copy(answerInput = answer) }
    }

    fun submitAnswer() {
        val session = uiState.value.session ?: return
        val currentQuestion = uiState.value.currentQuestion ?: return
        val answer = uiState.value.answerInput.trim()
        if (answer.isBlank() || uiState.value.feedback != null) return
        viewModelScope.launch {
            val responseMillis = System.currentTimeMillis() - questionStartMillis
            val outcome = repository.submitAnswer(
                sessionId = session.sessionId,
                question = currentQuestion,
                selectedAnswer = answer,
                responseMillis = responseMillis,
            )
            mutableState.value = uiState.value.copy(
                correctCount = uiState.value.correctCount + if (outcome.isCorrect) 1 else 0,
                retryQuestionCount = when {
                    outcome.isCorrect -> uiState.value.retryQuestionCount
                    else -> {
                        currentRoundMistakes[currentQuestion.entryId] = currentQuestion
                        currentRoundMistakes.size
                    }
                },
                feedback = SessionFeedback(
                    isCorrect = outcome.isCorrect,
                    correctAnswer = outcome.correctAnswer,
                    userAnswer = answer,
                ),
            )
            persistCurrentSessionState()
            if (outcome.isCorrect) {
                AppFeedbackPlayer.playCorrect()
            } else {
                AppFeedbackPlayer.playWrong()
            }
        }
    }

    fun advance() {
        val session = uiState.value.session ?: return
        if (uiState.value.feedback == null) return
        val nextIndex = uiState.value.currentIndex + 1
        val nextQuestion = session.questions.getOrNull(nextIndex)
        if (nextQuestion == null && currentRoundMistakes.isNotEmpty()) {
            val retryQuestions = currentRoundMistakes.values.toList()
            currentRoundMistakes.clear()
            val retrySession = session.copy(
                sessionId = UUID.randomUUID().toString(),
                questions = retryQuestions,
            )
            questionStartMillis = System.currentTimeMillis()
            mutableState.value = uiState.value.copy(
                session = retrySession,
                currentIndex = 0,
                currentQuestion = retryQuestions.firstOrNull(),
                round = uiState.value.round + 1,
                retryQuestionCount = 0,
                answerInput = "",
                feedback = null,
            )
            viewModelScope.launch {
                persistCurrentSessionState()
            }
            return
        }
        questionStartMillis = System.currentTimeMillis()
        mutableState.value = uiState.value.copy(
            currentIndex = nextIndex,
            currentQuestion = nextQuestion,
            answerInput = "",
            feedback = null,
        )
        viewModelScope.launch {
            persistCurrentSessionState()
        }
    }

    private fun restoreOrLoadSession() {
        viewModelScope.launch {
            val autoplayAudio = mutableState.value.autoplayAudio
            mutableState.value = SessionUiState(isLoading = true, autoplayAudio = autoplayAudio)
            val restoredState = sessionStateStore.read(mode)
            if (restoredState != null) {
                restorePersistedSession(restoredState, autoplayAudio)
            } else {
                buildFreshSession()
            }
        }
    }

    private suspend fun buildFreshSession() {
        val autoplayAudio = mutableState.value.autoplayAudio
        currentRoundMistakes.clear()
        mutableState.value = SessionUiState(isLoading = true, autoplayAudio = autoplayAudio)
        val session = repository.buildSession(mode = mode)
        questionStartMillis = System.currentTimeMillis()
        mutableState.value = SessionUiState(
            isLoading = false,
            session = session,
            currentIndex = 0,
            currentQuestion = session.questions.firstOrNull(),
            round = 1,
            retryQuestionCount = 0,
            totalQuestionCount = session.questions.size,
            correctCount = 0,
            autoplayAudio = autoplayAudio,
        )
        persistCurrentSessionState()
    }

    private fun restorePersistedSession(
        persistedState: PersistedSessionState,
        autoplayAudio: Boolean,
    ) {
        currentRoundMistakes.clear()
        persistedState.currentRoundMistakes.forEach { question ->
            currentRoundMistakes[question.entryId] = question
        }
        questionStartMillis = System.currentTimeMillis()
        mutableState.value = SessionUiState(
            isLoading = false,
            session = persistedState.session,
            currentIndex = persistedState.currentIndex,
            currentQuestion = persistedState.session.questions.getOrNull(persistedState.currentIndex),
            round = persistedState.round,
            retryQuestionCount = persistedState.retryQuestionCount,
            totalQuestionCount = persistedState.totalQuestionCount,
            correctCount = persistedState.correctCount,
            feedback = persistedState.feedback?.toUiModel(),
            autoplayAudio = autoplayAudio,
        )
    }

    private suspend fun persistCurrentSessionState() {
        val state = uiState.value
        val session = state.session
        val currentQuestion = state.currentQuestion
        if (state.isLoading || session == null || currentQuestion == null) {
            sessionStateStore.clear(mode)
            return
        }
        sessionStateStore.save(
            mode = mode,
            state = PersistedSessionState(
                session = session,
                currentIndex = state.currentIndex,
                round = state.round,
                retryQuestionCount = state.retryQuestionCount,
                totalQuestionCount = state.totalQuestionCount,
                correctCount = state.correctCount,
                feedback = state.feedback?.toPersistedModel(),
                currentRoundMistakes = currentRoundMistakes.values.toList(),
            ),
        )
    }

    private fun SessionFeedback.toPersistedModel(): PersistedSessionFeedback = PersistedSessionFeedback(
        isCorrect = isCorrect,
        correctAnswer = correctAnswer,
        userAnswer = userAnswer,
    )

    private fun PersistedSessionFeedback.toUiModel(): SessionFeedback = SessionFeedback(
        isCorrect = isCorrect,
        correctAnswer = correctAnswer,
        userAnswer = userAnswer,
    )
}
