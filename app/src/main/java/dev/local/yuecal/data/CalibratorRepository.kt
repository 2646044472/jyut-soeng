package dev.local.yuecal.data

import android.content.Context
import android.net.Uri
import androidx.room.withTransaction
import dagger.hilt.android.qualifiers.ApplicationContext
import dev.local.yuecal.di.IoDispatcher
import dev.local.yuecal.domain.AppSettings
import dev.local.yuecal.domain.CalibrationEntry
import dev.local.yuecal.domain.DashboardSummary
import dev.local.yuecal.domain.EntryProgress
import dev.local.yuecal.domain.ImportResult
import dev.local.yuecal.domain.JudgingEngine
import dev.local.yuecal.domain.SessionMode
import dev.local.yuecal.domain.Sm2Scheduler
import dev.local.yuecal.domain.StudyQuestion
import dev.local.yuecal.domain.StudyQuestionType
import dev.local.yuecal.domain.StudySession
import dev.local.yuecal.domain.SubmissionOutcome
import dev.local.yuecal.domain.statusLabel
import dev.local.yuecal.domain.todayEpochDay
import dev.local.yuecal.media.AppAudioPlayer
import java.io.File
import java.io.IOException
import java.net.HttpURLConnection
import java.net.URL
import java.time.Instant
import java.util.UUID
import java.util.zip.ZipInputStream
import javax.inject.Inject
import javax.inject.Singleton
import kotlin.math.roundToInt
import kotlin.random.Random
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.withContext
import kotlinx.serialization.SerializationException
import kotlinx.serialization.builtins.ListSerializer
import kotlinx.serialization.json.Json

@Singleton
class CalibratorRepository @Inject constructor(
    private val database: AppDatabase,
    private val entryDao: EntryDao,
    private val progressDao: ProgressDao,
    private val sessionDao: SessionDao,
    private val settingsStore: AppSettingsStore,
    private val audioPlayer: AppAudioPlayer,
    @ApplicationContext private val context: Context,
    private val json: Json,
    @IoDispatcher private val ioDispatcher: CoroutineDispatcher,
) {

    val settings: Flow<AppSettings> = settingsStore.settings

    private val entryCounts = combine(
        entryDao.observeEntryCount(),
        entryDao.observeEntryCountByType("word"),
        entryDao.observeEntryCountByType("expression"),
    ) { totalEntries, wordEntries, expressionEntries ->
        Triple(totalEntries, wordEntries, expressionEntries)
    }

    private val reviewCounts = combine(
        progressDao.observeDueCount(todayEpochDay()),
        progressDao.observeDueCountByType("word", todayEpochDay()),
        progressDao.observeDueCountByType("expression", todayEpochDay()),
        progressDao.observeIncomingCount(todayEpochDay() + 1),
        progressDao.observeNewCountByType("word"),
        progressDao.observeNewCountByType("expression"),
    ) { counts ->
        counts.toList()
    }

    private val dashboardCounts = combine(
        entryCounts,
        reviewCounts,
        progressDao.observeStartedCount(),
        sessionDao.observeAttemptsCount(),
    ) { entries, review, startedEntries, attempts ->
        DashboardSummary(
            totalEntries = entries.first,
            wordEntries = entries.second,
            expressionEntries = entries.third,
            dueEntries = review[0],
            dueWordEntries = review[1],
            dueExpressionEntries = review[2],
            incomingReviewEntries = review[3],
            newWordEntries = review[4],
            newExpressionEntries = review[5],
            startedEntries = startedEntries,
            totalAttempts = attempts,
        )
    }

    val dashboard: Flow<DashboardSummary> = combine(
        dashboardCounts,
        sessionDao.observeCorrectCount(),
        settingsStore.settings,
    ) { base, correct, settings ->
        base.copy(
            totalCorrect = correct ?: 0,
            dailyLearnGoal = settings.dailyLearnGoal,
            dailyReviewGoal = settings.dailyReviewGoal,
        )
    }

    val libraryEntries: Flow<List<CalibrationEntry>> = entryDao.observeLibraryEntries().map { rows ->
        rows.map { it.toModel() }
    }

    fun searchEntries(query: String): Flow<List<CalibrationEntry>> {
        val trimmed = query.trim()
        return if (trimmed.isBlank()) {
            libraryEntries.map { it.take(80) }
        } else {
            entryDao.observeSearchResults(trimmed, 80).map { rows -> rows.map { it.toModel() } }
        }
    }

    suspend fun dueCountNow(): Int = withContext(ioDispatcher) {
        progressDao.dueCountNow(todayEpochDay())
    }

    suspend fun ensureBuiltinImported(force: Boolean = false): ImportResult = withContext(ioDispatcher) {
        val bundleText = context.assets.open("builtin/content.json").bufferedReader().use { it.readText() }
        val bundle = decodeBundle(bundleText)
        val currentSettings = settingsStore.snapshot()
        if (!force && currentSettings.builtInSeedVersion == bundle.version) {
            ImportResult(sourceLabel = "builtin", version = bundle.version, importedCount = 0)
        } else {
            val result = syncManagedBundle(
                bundle = bundle,
                defaultSource = "builtin",
            )
            settingsStore.setBuiltInSeedVersion(bundle.version)
            result
        }
    }

    suspend fun importFromUri(uri: Uri): ImportResult = withContext(ioDispatcher) {
        val text = context.contentResolver.openInputStream(uri)?.bufferedReader()?.use { it.readText() }
            ?: error("Unable to read import file.")
        val bundle = decodeBundle(text)
        val now = System.currentTimeMillis()
        val sourceLabel = "local-import"
        val entities = bundle.entries.map { asset ->
            asset.toEntity(
                createdAt = now,
                updatedAt = now,
                defaultSource = sourceLabel,
            )
        }
        entryDao.upsertEntries(entities)
        ImportResult(sourceLabel = sourceLabel, version = bundle.version, importedCount = entities.size)
    }

    suspend fun importFromGitHub(): ImportResult = withContext(ioDispatcher) {
        runCatching { importFromGitHubPack() }
            .getOrElse { packError ->
                val wrapped = IOException("GitHub 内容包暂不可用", packError)
                throw wrapped
            }
    }

    private suspend fun importFromGitHubPack(): ImportResult {
        val localRoot = downloadGitHubPack()
        val bundleFile = File(localRoot, "content.json")
        if (!bundleFile.exists()) {
            error("GitHub 内容包缺少 content.json")
        }
        val bundle = decodeBundle(bundleFile.readText())
        return syncManagedBundle(
            bundle = bundle,
            defaultSource = "github",
            audioResolver = { asset ->
                resolveImportedAudio(asset.audioAsset, localRoot)
            },
        )
    }

    suspend fun buildSession(
        mode: SessionMode,
    ): StudySession = withContext(ioDispatcher) {
        val settings = settingsStore.snapshot()
        val targetSize = when (mode) {
            SessionMode.Learn -> settings.dailyLearnGoal.coerceAtLeast(4)
            SessionMode.Review -> settings.dailyReviewGoal.coerceAtLeast(6)
        }
        val expressionLimit = when (mode) {
            SessionMode.Learn -> (targetSize * 0.4f).roundToInt().coerceAtLeast(2)
            SessionMode.Review -> (targetSize * 0.35f).roundToInt().coerceAtLeast(2)
        }
        val wordLimit = (targetSize - expressionLimit).coerceAtLeast(2)
        val today = todayEpochDay()
        val wordEntries = when (mode) {
            SessionMode.Learn -> selectLearningEntriesByType(
                entryType = "word",
                today = today,
                limit = wordLimit,
            )
            SessionMode.Review -> selectReviewEntriesByType(
                entryType = "word",
                today = today,
                limit = wordLimit,
            )
        }
        val expressionEntries = when (mode) {
            SessionMode.Learn -> selectLearningEntriesByType(
                entryType = "expression",
                today = today,
                limit = expressionLimit,
            )
            SessionMode.Review -> selectReviewEntriesByType(
                entryType = "expression",
                today = today,
                limit = expressionLimit,
            )
        }
        val fallbackWords = if (wordEntries.isNotEmpty()) {
            wordEntries
        } else if (mode == SessionMode.Learn) {
            entryDao.getFallbackEntriesByType("word", wordLimit)
        } else {
            emptyList()
        }
        val fallbackExpressions = if (expressionEntries.isNotEmpty()) {
            expressionEntries
        } else if (mode == SessionMode.Learn) {
            entryDao.getFallbackEntriesByType("expression", expressionLimit)
        } else {
            emptyList()
        }
        val chosenEntries = when (mode) {
            SessionMode.Learn -> interleaveEntries(
                first = fallbackWords,
                second = fallbackExpressions,
            )
            SessionMode.Review -> (fallbackWords + fallbackExpressions)
                .distinctBy { it.id }
                .shuffled(Random(System.nanoTime()))
        }
        val randomizedEntries = chosenEntries.shuffled(Random(System.nanoTime()))
        val candidatePool = entryDao.getAllEntries()
        val questions = randomizedEntries.map { entry ->
            val currentProgress = progressDao.getProgress(entry.id)?.toDomain()
            val options = if ((currentProgress?.repetitions ?: 0) >= 2) {
                buildMultipleChoiceOptions(
                    correctAnswer = entry.answerJyutping,
                    pool = candidatePool.filter { it.entryType == entry.entryType },
                )
            } else {
                emptyList()
            }
            StudyQuestion(
                entryId = entry.id,
                type = when {
                    entry.entryType == "expression" -> StudyQuestionType.ExpressionCard
                    options.isNotEmpty() -> StudyQuestionType.MultipleChoice
                    else -> StudyQuestionType.FillJyutping
                },
                displayText = entry.displayText,
                promptText = entry.promptText,
                answerJyutping = entry.answerJyutping,
                gloss = entry.gloss,
                options = options,
                audioAsset = entry.audioAsset,
                category = entry.category,
                notes = entry.notes,
                usageTip = entry.usageTip,
                exampleSentence = entry.exampleSentence,
                exampleTranslation = entry.exampleTranslation,
                sourceLabel = entry.sourceLabel,
            )
        }
        StudySession(
            sessionId = UUID.randomUUID().toString(),
            mode = mode,
            title = if (mode == SessionMode.Learn) "今日学习" else "今日复习",
            questions = questions,
        )
    }

    private suspend fun selectLearningEntriesByType(
        entryType: String,
        today: Long,
        limit: Int,
    ): List<CalibrationEntryEntity> {
        if (limit <= 0) return emptyList()
        val learningEntries = entryDao.getLearningEntriesByType(entryType, today, limit)
        if (learningEntries.size >= limit) return learningEntries

        val collected = learningEntries.toMutableList()
        val seenIds = collected.mapTo(mutableSetOf()) { it.id }

        entryDao.getNewEntriesByType(entryType, limit).forEach { entry ->
            if (seenIds.add(entry.id) && collected.size < limit) {
                collected += entry
            }
        }
        return collected
    }

    private suspend fun selectReviewEntriesByType(
        entryType: String,
        today: Long,
        limit: Int,
    ): List<CalibrationEntryEntity> {
        if (limit <= 0) return emptyList()
        val dueEntries = entryDao.getDueEntriesByType(entryType, today, limit)
        if (dueEntries.size >= limit) return dueEntries

        val collected = dueEntries.toMutableList()
        val seenIds = collected.mapTo(mutableSetOf()) { it.id }

        entryDao.getScheduledEntriesByType(
            entryType = entryType,
            today = today,
            lookaheadDay = today + 1,
            limit = limit * 2,
        ).forEach { entry ->
            if (seenIds.add(entry.id) && collected.size < limit) {
                collected += entry
            }
        }
        if (collected.size >= limit) return collected

        entryDao.getStartedReviewEntriesByType(entryType, limit * 3).forEach { entry ->
            if (seenIds.add(entry.id) && collected.size < limit) {
                collected += entry
            }
        }
        return collected
    }

    suspend fun submitAnswer(
        sessionId: String,
        question: StudyQuestion,
        selectedAnswer: String,
        responseMillis: Long,
    ): SubmissionOutcome = withContext(ioDispatcher) {
        val isCorrect = normalizeJyutpingAnswer(selectedAnswer) == normalizeJyutpingAnswer(question.answerJyutping)
        val quality = JudgingEngine.score(isCorrect, responseMillis, question.type)
        val currentProgress = progressDao.getProgress(question.entryId)?.toDomain()
        val nextProgress = Sm2Scheduler.next(currentProgress, quality)
        progressDao.upsertProgress(
            ReviewProgressEntity(
                entryId = question.entryId,
                repetitions = nextProgress.repetitions,
                intervalDays = nextProgress.intervalDays,
                easeFactor = nextProgress.easeFactor,
                nextReviewEpochDay = nextProgress.nextReviewEpochDay,
                lastReviewedAt = nextProgress.lastReviewedAt,
                totalCorrect = nextProgress.totalCorrect,
                totalAttempts = nextProgress.totalAttempts,
                streak = nextProgress.streak,
            ),
        )
        sessionDao.insertAttempt(
            StudyAttemptEntity(
                sessionId = sessionId,
                entryId = question.entryId,
                selectedAnswer = selectedAnswer,
                correctAnswer = question.answerJyutping,
                isCorrect = isCorrect,
                quality = quality,
                answeredAt = System.currentTimeMillis(),
                responseMillis = responseMillis,
            ),
        )
        SubmissionOutcome(
            isCorrect = isCorrect,
            correctAnswer = question.answerJyutping,
            updatedProgress = nextProgress,
            quality = quality,
        )
    }

    suspend fun playAudio(assetPath: String?) {
        withContext(Dispatchers.Main) {
            audioPlayer.playAsset(assetPath)
        }
    }

    suspend fun stopAudio() {
        withContext(Dispatchers.Main) {
            audioPlayer.stop()
        }
    }

    private suspend fun syncManagedBundle(
        bundle: ContentBundle,
        defaultSource: String,
        audioResolver: (ContentEntryAsset) -> String? = { null },
    ): ImportResult {
        val now = System.currentTimeMillis()
        val entities = bundle.entries.map { asset ->
            asset.toEntity(
                createdAt = now,
                updatedAt = now,
                defaultSource = defaultSource,
                audioOverride = audioResolver(asset),
            )
        }
        database.withTransaction {
            syncManagedEntries(
                incomingAssets = bundle.entries,
                incomingEntities = entities,
                updatedAt = now,
            )
        }
        return ImportResult(
            sourceLabel = defaultSource,
            version = bundle.version,
            importedCount = entities.size,
        )
    }

    private suspend fun syncManagedEntries(
        incomingAssets: List<ContentEntryAsset>,
        incomingEntities: List<CalibrationEntryEntity>,
        updatedAt: Long,
    ) {
        val existingEntries = entryDao.getAllEntriesIncludingArchived()
        val plan = ManagedEntrySyncPlanner.plan(
            existingEntries = existingEntries,
            incomingEntries = incomingAssets,
        )
        entryDao.upsertEntries(incomingEntities)

        val progressIds = (plan.aliasTargetByEntryId.keys + plan.aliasTargetByEntryId.values).distinct()
        val progressById = if (progressIds.isEmpty()) {
            emptyMap()
        } else {
            progressDao.getProgressByEntryIds(progressIds).associateBy { it.entryId }
        }

        plan.aliasTargetByEntryId.entries
            .groupBy(keySelector = { it.value }, valueTransform = { it.key })
            .forEach { (targetEntryId, sourceEntryIds) ->
                val uniqueSourceIds = sourceEntryIds.distinct()
                val mergedProgress = buildList {
                    progressById[targetEntryId]?.let(::add)
                    uniqueSourceIds.forEach { sourceEntryId ->
                        progressById[sourceEntryId]?.let(::add)
                    }
                }
                ReviewProgressMerger.merge(
                    targetId = targetEntryId,
                    records = mergedProgress,
                )?.let(progressDao::upsertProgress)
                if (uniqueSourceIds.isNotEmpty()) {
                    progressDao.deleteProgressByEntryIds(uniqueSourceIds)
                    uniqueSourceIds.forEach { sourceEntryId ->
                        sessionDao.reassignAttempts(
                            sourceEntryId = sourceEntryId,
                            targetEntryId = targetEntryId,
                        )
                    }
                }
            }

        if (plan.archiveEntryIds.isNotEmpty()) {
            entryDao.archiveEntries(plan.archiveEntryIds.toList(), updatedAt = updatedAt)
        }
    }

    private fun downloadGitHubPack(): File {
        val localRoot = File(context.filesDir, "github-content")
        val tempRoot = File(context.cacheDir, "github-content-download")
        resetDirectory(tempRoot)
        val zipFile = File(tempRoot, "content.zip")
        downloadToFile(
            url = GitHubSources.CONTENT_PACK_URL,
            target = zipFile,
            accept = "application/octet-stream",
        )
        unzip(zipFile = zipFile, targetDir = tempRoot)
        val extractedRoot = tempRoot.walkTopDown()
            .firstOrNull { it.isFile && it.name == "content.json" }
            ?.parentFile
            ?: error("GitHub 内容包缺少 content.json")
        resetDirectory(localRoot)
        extractedRoot.copyRecursively(localRoot, overwrite = true)
        tempRoot.deleteRecursively()
        return localRoot
    }

    private fun decodeBundle(text: String): ContentBundle {
        return try {
            json.decodeFromString(ContentBundle.serializer(), text)
        } catch (_: SerializationException) {
            val entries = json.decodeFromString(ListSerializer(ContentEntryAsset.serializer()), text)
            ContentBundle(
                version = "import-${System.currentTimeMillis()}",
                generatedAt = Instant.now().toString(),
                entries = entries,
            )
        }
    }

    private fun ContentEntryAsset.toEntity(
        createdAt: Long,
        updatedAt: Long,
        defaultSource: String,
        audioOverride: String? = null,
    ): CalibrationEntryEntity = CalibrationEntryEntity(
        id = id,
        displayText = displayText,
        promptText = promptText,
        answerJyutping = answerJyutping,
        gloss = gloss,
        notes = notes,
        usageTip = usageTip,
        exampleSentence = exampleSentence,
        exampleTranslation = exampleTranslation,
        entryType = entryType.ifBlank { "word" },
        category = category,
        groupId = groupId.ifBlank { answerJyutping.dropLast(1) },
        tone = if (tone == 0) answerJyutping.lastOrNull()?.digitToIntOrNull() ?: 0 else tone,
        audioAsset = audioOverride ?: audioAsset,
        sourceLabel = sourceLabel.ifBlank { defaultSource },
        sortOrder = sortOrder.coerceAtLeast(1),
        createdAt = createdAt,
        updatedAt = updatedAt,
        isActive = true,
    )

    private fun EntryWithProgress.toModel(): CalibrationEntry {
        val today = todayEpochDay()
        val progressModel = progress?.toDomain()
        return CalibrationEntry(
            id = entry.id,
            displayText = entry.displayText,
            promptText = entry.promptText,
            answerJyutping = entry.answerJyutping,
            gloss = entry.gloss,
            notes = entry.notes,
            usageTip = entry.usageTip,
            exampleSentence = entry.exampleSentence,
            exampleTranslation = entry.exampleTranslation,
            entryType = entry.entryType,
            category = entry.category,
            groupId = entry.groupId,
            tone = entry.tone,
            audioAsset = entry.audioAsset,
            sourceLabel = entry.sourceLabel,
            statusLabel = progressModel.statusLabel(today),
        )
    }

    private fun ReviewProgressEntity.toDomain(): EntryProgress = EntryProgress(
        repetitions = repetitions,
        intervalDays = intervalDays,
        easeFactor = easeFactor,
        nextReviewEpochDay = nextReviewEpochDay,
        lastReviewedAt = lastReviewedAt,
        totalCorrect = totalCorrect,
        totalAttempts = totalAttempts,
        streak = streak,
    )

    private fun httpGetText(url: String): String {
        val connection = (URL(url).openConnection() as HttpURLConnection).apply {
            connectTimeout = 15_000
            readTimeout = 30_000
            requestMethod = "GET"
            setRequestProperty("Accept", "application/json")
            setRequestProperty("User-Agent", "CantoCalibrator/0.1.0")
        }
        return connection.inputStream.bufferedReader().use { it.readText() }
    }

    private fun downloadToFile(
        url: String,
        target: File,
        accept: String,
    ) {
        target.parentFile?.mkdirs()
        val connection = (URL(url).openConnection() as HttpURLConnection).apply {
            connectTimeout = 15_000
            readTimeout = 60_000
            requestMethod = "GET"
            setRequestProperty("Accept", accept)
            setRequestProperty("User-Agent", "CantoCalibrator/0.1.0")
        }
        if (connection.responseCode !in 200..299) {
            throw IOException("HTTP ${connection.responseCode} while fetching $url")
        }
        connection.inputStream.use { input ->
            target.outputStream().use(input::copyTo)
        }
    }

    private fun unzip(
        zipFile: File,
        targetDir: File,
    ) {
        ZipInputStream(zipFile.inputStream().buffered()).use { zipInput ->
            var entry = zipInput.nextEntry
            val targetRootPath = targetDir.canonicalFile.toPath()
            while (entry != null) {
                val outputFile = File(targetDir, entry.name)
                val outputPath = outputFile.canonicalFile.toPath()
                require(outputPath.startsWith(targetRootPath)) { "GitHub 内容包路径非法" }
                if (entry.isDirectory) {
                    outputFile.mkdirs()
                } else {
                    outputFile.parentFile?.mkdirs()
                    outputFile.outputStream().use(zipInput::copyTo)
                }
                zipInput.closeEntry()
                entry = zipInput.nextEntry
            }
        }
    }

    private fun resetDirectory(directory: File) {
        if (directory.exists()) {
            directory.deleteRecursively()
        }
        directory.mkdirs()
    }

    private fun resolveImportedAudio(relativePath: String?, localRoot: File): String? {
        relativePath ?: return null
        if (packagedAssetExists(relativePath)) {
            return relativePath
        }
        val downloadedFile = File(localRoot, relativePath)
        return downloadedFile.takeIf(File::exists)?.absolutePath
    }

    private fun packagedAssetExists(path: String): Boolean = runCatching {
        context.assets.open(path).use { }
        true
    }.getOrDefault(false)

    private fun interleaveEntries(
        first: List<CalibrationEntryEntity>,
        second: List<CalibrationEntryEntity>,
    ): List<CalibrationEntryEntity> {
        val result = mutableListOf<CalibrationEntryEntity>()
        val seenIds = mutableSetOf<String>()
        val maxSize = maxOf(first.size, second.size)
        for (index in 0 until maxSize) {
            listOfNotNull(first.getOrNull(index), second.getOrNull(index)).forEach { entry ->
                if (seenIds.add(entry.id)) {
                    result += entry
                }
            }
        }
        return result
    }

    private fun normalizeJyutpingAnswer(value: String): String = value
        .trim()
        .lowercase()
        .replace("·", " ")
        .replace("-", " ")
        .replace(Regex("[1-6]"), "")
        .replace(Regex("\\s+"), "")

    private fun buildMultipleChoiceOptions(
        correctAnswer: String,
        pool: List<CalibrationEntryEntity>,
    ): List<String> {
        val distractors = pool
            .asSequence()
            .map { it.answerJyutping }
            .filter { normalizeJyutpingAnswer(it) != normalizeJyutpingAnswer(correctAnswer) }
            .distinct()
            .shuffled()
            .take(3)
            .toList()
        return (distractors + correctAnswer).distinct().shuffled()
    }
}
