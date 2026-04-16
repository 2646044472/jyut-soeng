package dev.local.yuecal.ui

import android.content.Intent
import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
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
import androidx.compose.runtime.getValue
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
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
                        onStartCorrection = { navController.navigate("session/correction") },
                        onStartExpression = { navController.navigate("session/expression") },
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
                        onDailyGoalChange = viewModel::updateDailyGoal,
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
    onStartCorrection: () -> Unit,
    onStartExpression: () -> Unit,
) {
    val summary = state.dashboard
    val wordGoal = ((summary.dailyGoal * 0.75f).toInt()).coerceAtLeast(6)
    val expressionGoal = (summary.dailyGoal - wordGoal).coerceAtLeast(2)
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        item {
            HeroCard(summary = summary, wordGoal = wordGoal, expressionGoal = expressionGoal)
        }
        item {
            Text(
                text = "今日任务",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
            )
        }
        item {
            StudyModeCard(
                eyebrow = "词语正音",
                title = "看词填粤拼，用粤拼校正读音",
                description = "先按自己的习惯读一遍，再写出 Jyutping，马上对照常错点和发音提醒。",
                stats = "${summary.dueWordEntries} 条待练 · 今日建议 ${wordGoal} 条",
                cta = "开始词语正音",
                onClick = onStartCorrection,
            )
        }
        item {
            StudyModeCard(
                eyebrow = "俚语与用法",
                title = "边学口语表达，边记住正确读法",
                description = "每张卡都会给你用法、场景和例句，再让你补出 Jyutping，把说法和读法一起吃透。",
                stats = "${summary.dueExpressionEntries} 条待练 · 今日建议 ${expressionGoal} 条",
                cta = "开始表达卡片",
                onClick = onStartExpression,
            )
        }
        item {
            ProgressSummaryCard(summary = summary)
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
                "这里不是背拼音表，而是看你会不会用 Jyutping 把音校准回来。",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
        state.lastMessage?.let { message ->
            item {
                MessageCard(message = message, onDismiss = onDismissMessage)
            }
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
    onDailyGoalChange: (Int) -> Unit,
    onRefreshBuiltin: () -> Unit,
    onImportFromGitHub: () -> Unit,
    onDismissMessage: () -> Unit,
) {
    val context = LocalContext.current
    val settings = state.settings
    val presets = listOf(10, 14, 18, 24, 32)
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        item {
            Text("我的", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
        }
        state.lastMessage?.let { message ->
            item {
                MessageCard(message = message, onDismiss = onDismissMessage)
            }
        }
        item {
            SettingsRow(
                title = "自动播音",
                subtitle = "只用于有真人示范读音的词条；不再默认强调音高轮廓。",
                checked = settings.autoplayAudio,
                onCheckedChange = onAutoplayChanged,
            )
        }
        item {
            SettingsRow(
                title = "每日提醒",
                subtitle = "在你通常会开口练的时间提醒你。",
                checked = settings.remindersEnabled,
                onCheckedChange = onReminderChanged,
            )
        }
        item {
            GoalCard(
                dailyGoal = settings.dailyGoal,
                presets = presets,
                onSelect = onDailyGoalChange,
            )
        }
        item {
            StatCard(
                title = "GitHub 更新源",
                value = "粤常",
                subtitle = "粤语正音词卡与表达卡片 · ${state.githubRepoUrl.removePrefix("https://github.com/")}",
            )
        }
        item {
            OutlinedButton(
                modifier = Modifier.fillMaxWidth(),
                onClick = onImportFromGitHub,
            ) {
                Text("从 GitHub 拉取题库")
            }
        }
        item {
            OutlinedButton(
                modifier = Modifier.fillMaxWidth(),
                onClick = {
                    context.startActivity(
                        Intent(Intent.ACTION_VIEW, Uri.parse(state.githubReleasesUrl)),
                    )
                },
            ) {
                Text("打开 GitHub Releases")
            }
        }
        item {
            StatCard(
                title = "当前内置题库版本",
                value = settings.builtInSeedVersion.ifBlank { "未导入" },
                subtitle = "重新导入后会覆盖内置正音词条和表达卡片。",
            )
        }
        item {
            OutlinedButton(
                modifier = Modifier.fillMaxWidth(),
                onClick = onRefreshBuiltin,
            ) {
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
            Text("当前没有可用 session。")
        }
        return
    }

    if (question == null) {
        CompletionScreen(
            title = session.title,
            correctCount = state.correctCount,
            totalCount = session.questions.size,
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
                current = state.currentIndex + 1,
                total = session.questions.size,
            )
        }
        item {
            PracticeCard(question = question)
        }
        if (question.type == StudyQuestionType.ExpressionCard) {
            item {
                ExpressionContextCard(question = question)
            }
        }
        item {
            if (question.type == StudyQuestionType.MultipleChoice) {
                MultipleChoiceCard(
                    options = question.options,
                    enabled = state.feedback == null,
                    onPick = { option ->
                        onAnswerChanged(option)
                        onSubmit()
                    },
                )
            } else {
                AnswerInputCard(
                    value = state.answerInput,
                    onValueChange = onAnswerChanged,
                    enabled = state.feedback == null,
                    onSubmit = onSubmit,
                )
            }
        }
        state.feedback?.let { feedback ->
            item {
                FeedbackCard(question = question, feedback = feedback)
            }
            item {
                Button(
                    modifier = Modifier.fillMaxWidth(),
                    onClick = onNext,
                ) {
                    Text(if (state.currentIndex + 1 >= session.questions.size) "完成这一轮" else "下一题")
                }
            }
        }
    }
}

@Composable
private fun HeroCard(
    summary: DashboardSummary,
    wordGoal: Int,
    expressionGoal: Int,
) {
    Card(
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.primaryContainer,
        ),
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Text(
                "今日正音",
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold,
            )
            Text(
                "粤拼是你校正口型、声母、韵母和语流的标尺，不是背完就结束的目标。",
                style = MaterialTheme.typography.bodyLarge,
            )
            Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                MiniStat(label = "待练总数", value = "${summary.dueEntries}")
                MiniStat(label = "词语", value = "${summary.dueWordEntries}")
                MiniStat(label = "表达", value = "${summary.dueExpressionEntries}")
            }
            Surface(
                color = MaterialTheme.colorScheme.surface.copy(alpha = 0.72f),
                shape = MaterialTheme.shapes.large,
            ) {
                Text(
                    modifier = Modifier.padding(horizontal = 14.dp, vertical = 12.dp),
                    text = "今天建议：${wordGoal} 条词语正音 + ${expressionGoal} 张表达卡。英语释义会保留，帮助你像背词一样快速抓意思，但核心是把音读准。",
                    style = MaterialTheme.typography.bodyMedium,
                )
            }
        }
    }
}

@Composable
private fun ProgressSummaryCard(summary: DashboardSummary) {
    Card {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Text("练习概览", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            Text(
                "已进入排程 ${summary.startedEntries} 条 · 总题库 ${summary.totalEntries} 条 · 词语 ${summary.wordEntries} 条 · 表达 ${summary.expressionEntries} 条",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                MiniStat(label = "累计答题", value = "${summary.totalAttempts}")
                MiniStat(label = "正确率", value = "${summary.accuracyPercent}%")
            }
        }
    }
}

@Composable
private fun StudyModeCard(
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
            Button(
                modifier = Modifier.fillMaxWidth(),
                onClick = onClick,
            ) {
                Text(cta)
            }
        }
    }
}

@Composable
private fun GoalCard(
    dailyGoal: Int,
    presets: List<Int>,
    onSelect: (Int) -> Unit,
) {
    Card {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Text("每日目标", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            Text(
                "别再用 +4 / -4 猜。直接选一个今天能完成的任务包。",
                style = MaterialTheme.typography.bodyMedium,
            )
            Text(
                "当前：${dailyGoal} 条（约 ${(dailyGoal * 0.75f).toInt().coerceAtLeast(6)} 条词语正音 + ${(dailyGoal - (dailyGoal * 0.75f).toInt()).coerceAtLeast(2)} 张表达卡）",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                presets.chunked(2).forEach { row ->
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                    ) {
                        row.forEach { goal ->
                            val selected = goal == dailyGoal
                            OutlinedButton(
                                modifier = Modifier.weight(1f),
                                onClick = { onSelect(goal) },
                            ) {
                                Text(if (selected) "已选 $goal" else "$goal 条")
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun SessionHeader(
    title: String,
    current: Int,
    total: Int,
) {
    Card(
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.secondaryContainer),
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(title, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                Text("第 $current / $total 题", style = MaterialTheme.typography.bodyMedium)
            }
            Text(
                text = "${((current - 1) * 100 / total).coerceAtLeast(0)}%",
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
                    StudyQuestionType.ExpressionCard -> "先读这张表达卡，再写出它的 Jyutping"
                    StudyQuestionType.MultipleChoice -> "先心里读一遍，再从选项里挑出最对的 Jyutping"
                    StudyQuestionType.FillJyutping -> "看到词语先自己读，再写出 Jyutping 校正"
                },
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.primary,
            )
            Text(question.displayText, style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
            if (question.gloss.isNotBlank()) {
                Text(question.gloss, style = MaterialTheme.typography.bodyLarge)
            }
            Text(
                question.promptText,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Text(
                "分类：${question.category}",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
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
            if (question.usageTip.isNotBlank()) {
                Text(question.usageTip, style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Medium)
            }
            if (question.exampleSentence.isNotBlank()) {
                Text("例句：${question.exampleSentence}", style = MaterialTheme.typography.bodyMedium)
            }
            if (question.exampleTranslation.isNotBlank()) {
                Text(
                    question.exampleTranslation,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
    }
}

@Composable
private fun AnswerInputCard(
    value: String,
    onValueChange: (String) -> Unit,
    enabled: Boolean,
    onSubmit: () -> Unit,
) {
    Card {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            OutlinedTextField(
                modifier = Modifier.fillMaxWidth(),
                value = value,
                onValueChange = onValueChange,
                enabled = enabled,
                singleLine = true,
                label = { Text("写出 Jyutping") },
                placeholder = { Text("例如：gam1 jat6") },
            )
            Button(
                modifier = Modifier.fillMaxWidth(),
                enabled = enabled && value.trim().isNotEmpty(),
                onClick = onSubmit,
            ) {
                Text("提交并校对")
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
            Text(
                "这题是快节奏复习题，选出最准确的 Jyutping。",
                style = MaterialTheme.typography.bodyMedium,
            )
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
private fun FeedbackCard(
    question: StudyQuestion,
    feedback: SessionFeedback,
) {
    val correct = feedback.outcome.isCorrect
    Card(
        colors = CardDefaults.cardColors(
            containerColor = if (correct) {
                MaterialTheme.colorScheme.primaryContainer
            } else {
                MaterialTheme.colorScheme.errorContainer
            },
        ),
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            Text(
                if (correct) "这题读音对了" else "这题需要再校一下",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
            )
            Text("你的输入：${feedback.userAnswer}", style = MaterialTheme.typography.bodyMedium)
            Text("标准写法：${feedback.outcome.correctAnswer}", style = MaterialTheme.typography.bodyMedium)
            if (question.notes.isNotBlank()) {
                Text(question.notes, style = MaterialTheme.typography.bodyMedium)
            }
            if (question.exampleSentence.isNotBlank()) {
                Text("例句：${question.exampleSentence}", style = MaterialTheme.typography.bodyMedium)
            }
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
                Text(
                    "$correctCount / $totalCount",
                    style = MaterialTheme.typography.displaySmall,
                    fontWeight = FontWeight.Bold,
                )
                Text(
                    "先把词读出来，再用 Jyutping 对照；这才是你要的正音节奏。",
                    style = MaterialTheme.typography.bodyMedium,
                    textAlign = TextAlign.Center,
                )
                Button(onClick = onRestart) {
                    Text("重新开始一轮")
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
                Column(modifier = Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    Text(entry.displayText, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                    if (entry.gloss.isNotBlank()) {
                        Text(entry.gloss, style = MaterialTheme.typography.bodyMedium)
                    }
                }
                if (entry.audioAsset != null) {
                    IconButton(onClick = { onPlayAudio(entry.audioAsset) }) {
                        Icon(Icons.Outlined.PlayArrow, contentDescription = "播放")
                    }
                }
            }
            Text("Jyutping：${entry.answerJyutping}", style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium)
            if (entry.usageTip.isNotBlank()) {
                Text(entry.usageTip, style = MaterialTheme.typography.bodyMedium)
            } else if (entry.notes.isNotBlank()) {
                Text(entry.notes, style = MaterialTheme.typography.bodyMedium)
            }
            if (entry.exampleSentence.isNotBlank()) {
                Text("例句：${entry.exampleSentence}", style = MaterialTheme.typography.bodyMedium)
            }
            if (entry.exampleTranslation.isNotBlank()) {
                Text(
                    entry.exampleTranslation,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            Text(
                "${if (entry.entryType == "expression") "表达卡" else "正音词条"} · ${entry.category} · ${if (entry.dueNow) "待复习" else "已排程"}",
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
            OutlinedButton(onClick = onDismiss) {
                Text("关闭")
            }
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
