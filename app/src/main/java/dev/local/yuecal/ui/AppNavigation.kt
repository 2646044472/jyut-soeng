package dev.local.yuecal.ui

import android.content.Intent
import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Book
import androidx.compose.material.icons.outlined.Home
import androidx.compose.material.icons.outlined.Person
import androidx.compose.material.icons.outlined.PlayArrow
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.DialogProperties
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import dev.local.yuecal.domain.CalibrationEntry
import dev.local.yuecal.domain.DashboardSummary
import dev.local.yuecal.domain.StudyQuestion
import dev.local.yuecal.domain.StudyQuestionType
import dev.local.yuecal.ui.theme.CantoCalibratorTheme

private enum class TopLevelDestination(
    val route: String,
    val label: String,
    val icon: androidx.compose.ui.graphics.vector.ImageVector,
) {
    Today("today", "今日", Icons.Outlined.Home),
    Library("library", "词库", Icons.Outlined.Book),
    Search("search", "搜索", Icons.Outlined.Search),
    Profile("profile", "我的", Icons.Outlined.Person),
}

@Composable
fun CantoCalibratorApp() {
    CantoCalibratorTheme {
        val navController = rememberNavController()
        val backStackEntry by navController.currentBackStackEntryAsState()
        val currentDestination = backStackEntry?.destination

        Scaffold(
            bottomBar = {
                NavigationBar {
                    TopLevelDestination.entries.forEach { destination ->
                        NavigationBarItem(
                            selected = currentDestination?.hierarchy?.any { it.route == destination.route } == true,
                            onClick = {
                                navController.navigate(destination.route) {
                                    popUpTo(navController.graph.findStartDestination().id) {
                                        saveState = true
                                    }
                                    launchSingleTop = true
                                    restoreState = true
                                }
                            },
                            icon = { Icon(destination.icon, contentDescription = destination.label) },
                            label = { Text(destination.label) },
                        )
                    }
                }
            },
        ) { innerPadding ->
            NavHost(
                navController = navController,
                startDestination = TopLevelDestination.Today.route,
                modifier = Modifier.padding(innerPadding),
            ) {
                composable(TopLevelDestination.Today.route) {
                    val viewModel: TodayViewModel = hiltViewModel()
                    val state by viewModel.uiState.collectAsStateWithLifecycle()
                    TodayScreen(
                        state = state,
                        onStartLearn = { navController.navigate("session/learn") },
                        onStartReview = { navController.navigate("session/review") },
                    )
                }
                composable(TopLevelDestination.Library.route) {
                    val viewModel: LibraryViewModel = hiltViewModel()
                    val state by viewModel.uiState.collectAsStateWithLifecycle()
                    val launcher = rememberLauncherForActivityResult(
                        contract = ActivityResultContracts.OpenDocument(),
                    ) { uri: Uri? ->
                        uri?.let(viewModel::importFromUri)
                    }
                    LibraryScreen(
                        state = state,
                        onImport = { launcher.launch(arrayOf("application/json", "text/json")) },
                        onPlayAudio = viewModel::playAudio,
                        onDismissMessage = viewModel::clearMessage,
                    )
                }
                composable(TopLevelDestination.Search.route) {
                    val viewModel: SearchViewModel = hiltViewModel()
                    val state by viewModel.uiState.collectAsStateWithLifecycle()
                    SearchScreen(
                        state = state,
                        onQueryChanged = viewModel::updateQuery,
                        onPlayAudio = viewModel::playAudio,
                    )
                }
                composable(TopLevelDestination.Profile.route) {
                    val viewModel: ProfileViewModel = hiltViewModel()
                    val state by viewModel.uiState.collectAsStateWithLifecycle()
                    ProfileScreen(
                        state = state,
                        onAutoplayChanged = viewModel::setAutoplay,
                        onReminderChanged = viewModel::setReminders,
                        onDailyLearnGoalChange = viewModel::updateDailyLearnGoal,
                        onRefreshBuiltin = viewModel::refreshBuiltinContent,
                        onImportFromGitHub = viewModel::importFromGitHub,
                        onDismissMessage = viewModel::clearMessage,
                    )
                }
                composable("session/{mode}") {
                    val viewModel: SessionViewModel = hiltViewModel()
                    val state by viewModel.uiState.collectAsStateWithLifecycle()
                    SessionScreen(
                        state = state,
                        onAnswerChanged = viewModel::updateAnswerInput,
                        onSubmit = viewModel::submitAnswer,
                        onNext = viewModel::advance,
                        onRestart = viewModel::loadSession,
                    )
                }
            }
        }
    }
}

@Composable
private fun TodayScreen(
    state: TodayUiState,
    onStartLearn: () -> Unit,
    onStartReview: () -> Unit,
) {
    val summary = state.dashboard
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        item {
            TodayHeroCard(summary)
        }
        item {
            SessionLaneCard(
                eyebrow = "今日学习",
                title = "今日学完，明日接着复习",
                description = "新内容以输入题为主，今天学进去的条目，会在明日自动转进复习。",
                stats = "新词 ${summary.newWordEntries} · 新表达 ${summary.newExpressionEntries} · 明日回看 ${summary.incomingReviewEntries}",
                cta = "开始今日学习",
                onClick = onStartLearn,
            )
        }
        item {
            SessionLaneCard(
                eyebrow = "今日复习",
                title = "先刷到期，再决定要不要多练",
                description = "今日目标只算已学过且到期的词和表达；刷完以后想多练，再继续补刷已学内容。",
                stats = "待回看词 ${summary.dueWordEntries} · 表达 ${summary.dueExpressionEntries} · 自动目标 ${summary.dailyReviewGoal}",
                cta = "开始今日复习",
                onClick = onStartReview,
            )
        }
        item {
            OverviewCard(summary)
        }
    }
}

@Composable
private fun LibraryScreen(
    state: LibraryUiState,
    onImport: () -> Unit,
    onPlayAudio: (String?) -> Unit,
    onDismissMessage: () -> Unit,
) {
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        item {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text("词库", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
                OutlinedButton(onClick = onImport) {
                    Text("导入 JSON")
                }
            }
        }
        item {
            Text(
                "这里是正音词条和表达卡，不展示英译，重点只放在读法、用法和例句。",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
        state.lastMessage?.let { message ->
            item { MessageCard(message = message, onDismiss = onDismissMessage) }
        }
        items(state.entries, key = { it.id }) { entry ->
            EntryCard(entry = entry, onPlayAudio = onPlayAudio)
        }
    }
}

@Composable
private fun SearchScreen(
    state: SearchUiState,
    onQueryChanged: (String) -> Unit,
    onPlayAudio: (String?) -> Unit,
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        Text("搜索", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
        OutlinedTextField(
            modifier = Modifier.fillMaxWidth(),
            value = state.query,
            onValueChange = onQueryChanged,
            label = { Text("输入词语、Jyutping、用法或例句") },
        )
        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            items(state.results, key = { it.id }) { entry ->
                EntryCard(entry = entry, onPlayAudio = onPlayAudio)
            }
        }
    }
}

@Composable
private fun ProfileScreen(
    state: ProfileUiState,
    onAutoplayChanged: (Boolean) -> Unit,
    onReminderChanged: (Boolean) -> Unit,
    onDailyLearnGoalChange: (Int) -> Unit,
    onRefreshBuiltin: () -> Unit,
    onImportFromGitHub: () -> Unit,
    onDismissMessage: () -> Unit,
) {
    val context = LocalContext.current
    val settings = state.settings
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        item {
            Text("我的", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
        }
        state.lastMessage?.let { message ->
            item { MessageCard(message = message, onDismiss = onDismissMessage) }
        }
        item {
            SettingsRow(
                title = "自动播读",
                subtitle = "只在词条有真人或稳定读音资源时自动播放，不再依赖抽象音高轮廓。",
                checked = settings.autoplayAudio,
                onCheckedChange = onAutoplayChanged,
            )
        }
        item {
            SettingsRow(
                title = "每日提醒",
                subtitle = "在你通常会练习的时间提醒你完成今日学习和复习。",
                checked = settings.remindersEnabled,
                onCheckedChange = onReminderChanged,
            )
        }
        item {
            GoalCard(
                title = "每日学习目标",
                subtitle = "新词和新表达的目标量，手动调整。",
                value = settings.dailyLearnGoal,
                min = 4,
                onChange = onDailyLearnGoalChange,
            )
        }
        item {
            StatCard(
                title = "今日复习量",
                value = "${state.dashboard.dailyReviewGoal}",
                subtitle = "只把已学过且到期的内容算进今日目标；想多练时再继续刷已学词。",
            )
        }
        item {
            StatCard(
                title = "GitHub 更新源",
                value = "粤常",
                subtitle = state.githubRepoUrl.removePrefix("https://github.com/"),
            )
        }
        item {
            OutlinedButton(modifier = Modifier.fillMaxWidth(), onClick = onImportFromGitHub) {
                Text("从 GitHub 拉取题库")
            }
        }
        item {
            OutlinedButton(
                modifier = Modifier.fillMaxWidth(),
                onClick = {
                    context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(state.githubReleasesUrl)))
                },
            ) {
                Text("打开 GitHub Releases")
            }
        }
        item {
            StatCard(
                title = "内置题库版本",
                value = state.settings.builtInSeedVersion.ifBlank { "未导入" },
                subtitle = "重导后会覆盖内置正音词条与表达卡。",
            )
        }
        item {
            OutlinedButton(modifier = Modifier.fillMaxWidth(), onClick = onRefreshBuiltin) {
                Text("重导内置题库")
            }
        }
        item {
            StatCard(
                title = "累计练习",
                value = "${state.dashboard.totalAttempts}",
                subtitle = "正确 ${state.dashboard.totalCorrect} · 正确率 ${state.dashboard.accuracyPercent}%",
            )
        }
    }
}

@Composable
private fun SessionScreen(
    state: SessionUiState,
    onAnswerChanged: (String) -> Unit,
    onSubmit: () -> Unit,
    onNext: () -> Unit,
    onRestart: () -> Unit,
) {
    if (state.isLoading) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            CircularProgressIndicator()
        }
        return
    }

    val session = state.session
    val question = state.currentQuestion
    if (session == null) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            Text("当前没有可用练习。")
        }
        return
    }

    if (question == null) {
        CompletionScreen(
            title = session.title,
            correctCount = state.correctCount,
            totalCount = state.totalQuestionCount,
            onRestart = onRestart,
        )
        return
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        item {
            SessionHeader(
                title = session.title,
                round = state.round,
                current = state.currentIndex + 1,
                total = session.questions.size,
            )
        }
        item { PracticeCard(question = question) }
        if (question.type == StudyQuestionType.ExpressionCard) {
            item { ExpressionContextCard(question = question) }
        }
        item {
            when (question.type) {
                StudyQuestionType.MultipleChoice -> MultipleChoiceCard(
                    options = question.options,
                    enabled = state.feedback == null,
                    onPick = { option ->
                        onAnswerChanged(option)
                        onSubmit()
                    },
                )
                StudyQuestionType.FillJyutping,
                StudyQuestionType.ExpressionCard -> AnswerInputCard(
                    focusKey = question.entryId,
                    value = state.answerInput,
                    onValueChange = onAnswerChanged,
                    enabled = state.feedback == null,
                    onSubmit = onSubmit,
                )
            }
        }
    }

    state.feedback?.let { feedback ->
        FeedbackDialog(
            question = question,
            feedback = feedback,
            nextLabel = when {
                state.currentIndex + 1 < session.questions.size -> "下一个"
                state.round == 1 && state.retryQuestionCount > 0 -> "进入错词第二阶段"
                else -> "完成这一轮"
            },
            onNext = onNext,
        )
    }
}

@Composable
private fun TodayHeroCard(summary: DashboardSummary) {
    Card(
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer),
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Text("粤常", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
            Text(
                "先开口，再用 Jyutping 校正。你不是在背音标，而是在把读音调到日常可用。",
                style = MaterialTheme.typography.bodyLarge,
            )
            Row(horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                MiniStat("今日待复习", "${summary.dueEntries}")
                MiniStat("今日新学", "${summary.newWordEntries + summary.newExpressionEntries}")
                MiniStat("明日回看", "${summary.incomingReviewEntries}")
            }
        }
    }
}

@Composable
private fun SessionLaneCard(
    eyebrow: String,
    title: String,
    description: String,
    stats: String,
    cta: String,
    onClick: () -> Unit,
) {
    Card {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Text(eyebrow, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
            Text(title, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            Text(description, style = MaterialTheme.typography.bodyMedium)
            Text(stats, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            Button(modifier = Modifier.fillMaxWidth(), onClick = onClick) {
                Text(cta)
            }
        }
    }
}

@Composable
private fun OverviewCard(summary: DashboardSummary) {
    Card {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Text("整体进度", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            Text(
                "总题库 ${summary.totalEntries} · 词语 ${summary.wordEntries} · 表达 ${summary.expressionEntries} · 已进入排程 ${summary.startedEntries} · 明日回看 ${summary.incomingReviewEntries}",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Row(horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                MiniStat("累计答题", "${summary.totalAttempts}")
                MiniStat("正确率", "${summary.accuracyPercent}%")
            }
        }
    }
}

@Composable
private fun GoalCard(
    title: String,
    subtitle: String,
    value: Int,
    min: Int,
    onChange: (Int) -> Unit,
) {
    var draftValue by remember(value) { mutableStateOf(value.toString()) }

    Card {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(18.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Column(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.spacedBy(4.dp),
            ) {
                Text(title, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                Text(subtitle, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            Column(
                modifier = Modifier.width(168.dp),
                horizontalAlignment = Alignment.End,
                verticalArrangement = Arrangement.spacedBy(6.dp),
            ) {
                Text("$value", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                OutlinedTextField(
                    modifier = Modifier.fillMaxWidth(),
                    value = draftValue,
                    onValueChange = { next ->
                        if (next.all(Char::isDigit)) {
                            draftValue = next
                        }
                    },
                    singleLine = true,
                    label = { Text("手动输入") },
                    placeholder = { Text("$min+") },
                    keyboardOptions = KeyboardOptions(
                        keyboardType = KeyboardType.Number,
                        imeAction = ImeAction.Done,
                    ),
                    keyboardActions = KeyboardActions(
                        onDone = {
                            draftValue.toIntOrNull()?.let { onChange(it.coerceAtLeast(min)) }
                        },
                    ),
                )
                OutlinedButton(
                    modifier = Modifier.fillMaxWidth(),
                    onClick = {
                        draftValue.toIntOrNull()?.let { onChange(it.coerceAtLeast(min)) }
                    },
                ) {
                    Text("保存")
                }
            }
        }
    }
}

@Composable
private fun SessionHeader(
    title: String,
    round: Int,
    current: Int,
    total: Int,
) {
    Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.secondaryContainer)) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(title, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                if (round > 1) {
                    Text("第二阶段：错词再练", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
                }
                Text("第 $current / $total 题", style = MaterialTheme.typography.bodyMedium)
            }
            Text(
                "${((current - 1) * 100 / total).coerceAtLeast(0)}%",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
            )
        }
    }
}

@Composable
private fun PracticeCard(question: StudyQuestion) {
    Card {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Text(
                when (question.type) {
                    StudyQuestionType.FillJyutping -> "先按自己的习惯读，再写出拼音。"
                    StudyQuestionType.MultipleChoice -> "这是熟词快刷题，选出最顺手、最准确的 Jyutping。"
                    StudyQuestionType.ExpressionCard ->
                        if (question.sourceLabel == "generated") "先理解表达，再按提示先练语气，不必硬套进句子。"
                        else "先理解表达和例句，再写出拼音。"
                },
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.primary,
            )
            Text(question.displayText, style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
            Text(question.promptText, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
            Text("分类：${question.category}", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun ExpressionContextCard(question: StudyQuestion) {
    Card {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            if (question.gloss.isNotBlank()) {
                InfoBlock("意思", question.gloss)
            }
            if (question.usageTip.isNotBlank()) {
                InfoBlock(usageLabel(question.sourceLabel), question.usageTip)
            }
            ExampleBlock(question.exampleSentence, question.sourceLabel)
        }
    }
}

@Composable
private fun AnswerInputCard(
    focusKey: String,
    value: String,
    onValueChange: (String) -> Unit,
    enabled: Boolean,
    onSubmit: () -> Unit,
) {
    val focusRequester = FocusRequester()
    val keyboardController = LocalSoftwareKeyboardController.current

    LaunchedEffect(focusKey, enabled) {
        if (enabled) {
            focusRequester.requestFocus()
            keyboardController?.show()
        }
    }

    Card {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            OutlinedTextField(
                modifier = Modifier
                    .fillMaxWidth()
                    .focusRequester(focusRequester),
                value = value,
                onValueChange = onValueChange,
                enabled = enabled,
                singleLine = true,
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done),
                keyboardActions = KeyboardActions(
                    onDone = {
                        if (enabled && value.trim().isNotEmpty()) {
                            onSubmit()
                        }
                    },
                ),
                label = { Text("写出 Jyutping 拼写") },
                placeholder = { Text("例如：gam jat / m goi（不用写 1-6）") },
            )
            Button(
                modifier = Modifier.fillMaxWidth(),
                enabled = enabled && value.trim().isNotEmpty(),
                onClick = onSubmit,
            ) {
                Text("提交")
            }
        }
    }
}

@Composable
private fun MultipleChoiceCard(
    options: List<String>,
    enabled: Boolean,
    onPick: (String) -> Unit,
) {
    Card {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            options.forEach { option ->
                OutlinedButton(
                    modifier = Modifier.fillMaxWidth(),
                    enabled = enabled,
                    onClick = { onPick(option) },
                ) {
                    Text(option)
                }
            }
        }
    }
}

@Composable
private fun FeedbackDialog(
    question: StudyQuestion,
    feedback: SessionFeedback,
    nextLabel: String,
    onNext: () -> Unit,
) {
    AlertDialog(
        onDismissRequest = {},
        properties = DialogProperties(
            dismissOnBackPress = false,
            dismissOnClickOutside = false,
        ),
        text = {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(max = 480.dp)
                    .verticalScroll(rememberScrollState()),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                FeedbackCardContent(question = question, feedback = feedback)
            }
        },
        confirmButton = {
            Button(
                modifier = Modifier.fillMaxWidth(),
                onClick = onNext,
            ) {
                Text(nextLabel)
            }
        },
        dismissButton = {},
    )
}

@Composable
private fun FeedbackCardContent(
    question: StudyQuestion,
    feedback: SessionFeedback,
) {
    val correct = feedback.outcome.isCorrect
    Column(
        modifier = Modifier
            .fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        Text(
            if (correct) "对了，继续压实这个读法" else "这题再校一下，先看标准答案",
            style = MaterialTheme.typography.titleLarge,
            fontWeight = FontWeight.Bold,
            color = if (correct) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.error,
        )
        Text("你的输入：${feedback.userAnswer}", style = MaterialTheme.typography.bodyMedium)
        Text("标准答案：${feedback.outcome.correctAnswer}", style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium)
        Text(
            "平时输入可以写成：${question.answerJyutping.replace(Regex("[1-6]"), "")}",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        Text(
            "分音提示：${formatJyutpingSyllables(question.answerJyutping)}",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        if (question.gloss.isNotBlank()) {
            InfoBlock("意思", question.gloss)
        }
        if (question.usageTip.isNotBlank()) {
            InfoBlock(usageLabel(question.sourceLabel), question.usageTip)
        }
        if (question.exampleSentence.isNotBlank()) {
            ExampleBlock(question.exampleSentence, question.sourceLabel)
        }
    }
}

@Composable
private fun CompletionScreen(
    title: String,
    correctCount: Int,
    totalCount: Int,
    onRestart: () -> Unit,
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(20.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        Card {
            Column(
                modifier = Modifier.padding(24.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
            ) {
                Text(title, style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
                Text("这一轮完成了", style = MaterialTheme.typography.titleMedium)
                Text("$correctCount / $totalCount", style = MaterialTheme.typography.displaySmall, fontWeight = FontWeight.Bold)
                Text(
                    "下一轮继续把生词学进去，把旧词刷出来，这样每天都会更顺口。",
                    style = MaterialTheme.typography.bodyMedium,
                    textAlign = TextAlign.Center,
                )
                Button(onClick = onRestart) {
                    Text("再来一轮")
                }
            }
        }
    }
}

@Composable
private fun EntryCard(
    entry: CalibrationEntry,
    onPlayAudio: (String?) -> Unit,
) {
    Card {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.Top,
            ) {
                Column(modifier = Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text(entry.displayText, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                    if (entry.gloss.isNotBlank()) {
                        InfoBlock("意思", entry.gloss)
                    }
                    if (entry.usageTip.isNotBlank()) {
                        InfoBlock(usageLabel(entry.sourceLabel), entry.usageTip)
                    }
                }
                if (entry.audioAsset != null) {
                    IconButton(onClick = { onPlayAudio(entry.audioAsset) }) {
                        Icon(Icons.Outlined.PlayArrow, contentDescription = "播放")
                    }
                }
            }
            Text("Jyutping：${entry.answerJyutping}", style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium)
            if (entry.exampleSentence.isNotBlank()) {
                ExampleBlock(entry.exampleSentence, entry.sourceLabel)
            }
            Text(
                "${if (entry.entryType == "expression") "表达卡" else "正音词条"} · ${entry.category} · ${entry.statusLabel}",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}

@Composable
private fun StatCard(
    title: String,
    value: String,
    subtitle: String,
) {
    Card {
        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Text(title, style = MaterialTheme.typography.titleMedium)
            Text(value, style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
            Text(subtitle, style = MaterialTheme.typography.bodyMedium)
        }
    }
}

@Composable
private fun MessageCard(
    message: String,
    onDismiss: () -> Unit,
) {
    Card {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(message, modifier = Modifier.weight(1f))
            Spacer(modifier = Modifier.width(12.dp))
            OutlinedButton(onClick = onDismiss) { Text("关闭") }
        }
    }
}

@Composable
private fun SettingsRow(
    title: String,
    subtitle: String,
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
) {
    Card {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Column(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.spacedBy(4.dp),
            ) {
                Text(title, style = MaterialTheme.typography.titleMedium)
                Text(subtitle, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            Switch(checked = checked, onCheckedChange = onCheckedChange)
        }
    }
}

@Composable
private fun MiniStat(
    label: String,
    value: String,
) {
    Column(verticalArrangement = Arrangement.spacedBy(2.dp)) {
        Text(label, style = MaterialTheme.typography.labelMedium)
        Text(value, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
    }
}

@Composable
private fun ExampleBlock(
    raw: String,
    sourceLabel: String,
) {
    val lines = raw
        .split("\n")
        .map { it.trim() }
        .filter { it.isNotEmpty() }
    if (lines.isEmpty()) return
    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
        Text(
            if (sourceLabel == "generated") "练习提示" else "例句",
            style = MaterialTheme.typography.labelLarge,
            color = MaterialTheme.colorScheme.primary,
        )
        lines.forEach { line ->
            Text("• $line", style = MaterialTheme.typography.bodyMedium)
        }
    }
}

@Composable
private fun InfoBlock(
    label: String,
    value: String,
) {
    if (value.isBlank()) return
    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
        Text(label, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
        Text(value, style = MaterialTheme.typography.bodyMedium)
    }
}

private fun usageLabel(sourceLabel: String): String = if (sourceLabel == "generated") "提醒" else "点用"

private fun formatJyutpingSyllables(raw: String): String {
    val pieces = Regex("[a-z]+[1-6]").findAll(raw.lowercase()).map { it.value }.toList()
    return if (pieces.isEmpty()) raw else pieces.joinToString(" / ")
}
