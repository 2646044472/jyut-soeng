package dev.local.yuecal.ui

import android.content.Intent
import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
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
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
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
                        onStartSession = { navController.navigate("session") },
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
                composable("session") {
                    val viewModel: SessionViewModel = hiltViewModel()
                    val state by viewModel.uiState.collectAsStateWithLifecycle()
                    LaunchedEffect(state.currentQuestion?.entryId, state.autoplayAudio) {
                        if (state.autoplayAudio && state.currentQuestion != null) {
                            viewModel.playCurrentAudio()
                        }
                    }
                    SessionScreen(
                        state = state,
                        onPlayAudio = viewModel::playCurrentAudio,
                        onAnswer = viewModel::submitAnswer,
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
    onStartSession: () -> Unit,
) {
    val summary = state.dashboard
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        item {
            Text(
                text = "今日校准",
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold,
            )
        }
        item {
            Card {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    Text("jyut-soeng 即“粤常”的粤语拼音。", style = MaterialTheme.typography.titleMedium)
                    Text(
                        "这个 MVP 面向你自己的日常侧载使用，重点是把粤语读音校准练习做成每天都能打开、每天都能推进的工具。",
                        style = MaterialTheme.typography.bodyMedium,
                    )
                    Text("希望粤语变成日常。", style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Bold)
                }
            }
        }
        item {
            StatCard(
                title = "待处理",
                value = "${summary.dueEntries}",
                subtitle = "总词条 ${summary.totalEntries} · 今日目标 ${summary.dailyGoal}",
            )
        }
        item {
            StatCard(
                title = "正确率",
                value = "${summary.accuracyPercent}%",
                subtitle = "累计 ${summary.totalCorrect}/${summary.totalAttempts} 次答题",
            )
        }
        item {
            StatCard(
                title = "已启动 SRS",
                value = "${summary.startedEntries}",
                subtitle = "首次答对后会自动进入复习排程",
            )
        }
        item {
            Button(
                modifier = Modifier.fillMaxWidth(),
                onClick = onStartSession,
            ) {
                Text("开始学习 Session")
            }
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
            label = { Text("输入题面、Jyutping 或注释") },
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
                checked = settings.autoplayAudio,
                onCheckedChange = onAutoplayChanged,
            )
        }
        item {
            SettingsRow(
                title = "每日提醒",
                checked = settings.remindersEnabled,
                onCheckedChange = onReminderChanged,
            )
        }
        item {
            Card {
                Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("每日目标：${settings.dailyGoal}")
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        OutlinedButton(onClick = { onDailyGoalChange(settings.dailyGoal - 4) }) {
                            Text("-4")
                        }
                        OutlinedButton(onClick = { onDailyGoalChange(settings.dailyGoal + 4) }) {
                            Text("+4")
                        }
                    }
                }
            }
        }
        item {
            StatCard(
                title = "GitHub 更新源",
                value = "jyut-soeng",
                subtitle = "粤常的粤语拼音 · ${state.githubRepoUrl.removePrefix("https://github.com/")}",
            )
        }
        item {
            OutlinedButton(
                modifier = Modifier.fillMaxWidth(),
                onClick = onImportFromGitHub,
            ) {
                Text("从 GitHub 拉取内容")
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
                title = "内置数据版本",
                value = settings.builtInSeedVersion.ifBlank { "未导入" },
                subtitle = "可强制重导内置音高练习集",
            )
        }
        item {
            OutlinedButton(
                modifier = Modifier.fillMaxWidth(),
                onClick = onRefreshBuiltin,
            ) {
                Text("重导内置内容")
            }
        }
        item {
            StatCard(
                title = "累计答题",
                value = "${state.dashboard.totalAttempts}",
                subtitle = "正确 ${state.dashboard.totalCorrect} · 正确率 ${state.dashboard.accuracyPercent}%",
            )
        }
    }
}

@Composable
private fun SessionScreen(
    state: SessionUiState,
    onPlayAudio: () -> Unit,
    onAnswer: (String) -> Unit,
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
    if (session == null || question == null) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Text("当前没有可用题目。")
            OutlinedButton(onClick = onRestart) {
                Text("重新生成 Session")
            }
        }
        return
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        Text(
            text = "Session ${state.currentIndex + 1}/${session.questions.size}",
            style = MaterialTheme.typography.titleMedium,
        )
        Card {
            Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text(question.promptText, style = MaterialTheme.typography.titleLarge)
                Text(question.category, style = MaterialTheme.typography.bodyMedium)
                if (question.notes.isNotBlank()) {
                    Text(question.notes, style = MaterialTheme.typography.bodySmall)
                }
                OutlinedButton(onClick = onPlayAudio) {
                    Text("播放参考音高")
                }
            }
        }
        question.options.forEach { option ->
            Button(
                modifier = Modifier.fillMaxWidth(),
                onClick = { onAnswer(option) },
            ) {
                Text(option)
            }
        }
        state.lastFeedback?.let { feedback ->
            Text(feedback, style = MaterialTheme.typography.bodyMedium)
        }
        Spacer(modifier = Modifier.height(8.dp))
        Text("当前正确数：${state.correctCount}")
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
            verticalArrangement = Arrangement.spacedBy(6.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text(entry.displayText, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                IconButton(onClick = { onPlayAudio(entry.audioAsset) }) {
                    Icon(Icons.Outlined.PlayArrow, contentDescription = "播放")
                }
            }
            Text("答案：${entry.answerJyutping}")
            Text(entry.gloss.ifBlank { entry.promptText }, style = MaterialTheme.typography.bodyMedium)
            Text("分类：${entry.category} · 来源：${entry.sourceLabel}", style = MaterialTheme.typography.bodySmall)
            Text(if (entry.dueNow) "状态：待复习" else "状态：已排程", style = MaterialTheme.typography.bodySmall)
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
            OutlinedButton(onClick = onDismiss) {
                Text("关闭")
            }
        }
    }
}

@Composable
private fun SettingsRow(
    title: String,
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
            Text(title)
            Switch(checked = checked, onCheckedChange = onCheckedChange)
        }
    }
}
