package dev.local.yuecal.work

import android.Manifest
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.core.content.ContextCompat
import androidx.hilt.work.HiltWorker
import androidx.work.CoroutineWorker
import androidx.work.ExistingPeriodicWorkPolicy
import androidx.work.ExistingWorkPolicy
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.WorkerParameters
import dagger.assisted.Assisted
import dagger.assisted.AssistedInject
import dev.local.yuecal.MainActivity
import dev.local.yuecal.R
import dev.local.yuecal.data.AppSettingsStore
import dev.local.yuecal.data.CalibratorRepository
import java.util.concurrent.TimeUnit
import javax.inject.Inject
import javax.inject.Singleton
import timber.log.Timber

private const val REVIEW_CHANNEL_ID = "daily_review"
private const val SEED_WORK_NAME = "seed-content"
private const val REVIEW_WORK_NAME = "daily-review-reminder"

@HiltWorker
class SeedContentWorker @AssistedInject constructor(
    @Assisted appContext: Context,
    @Assisted params: WorkerParameters,
    private val repository: CalibratorRepository,
) : CoroutineWorker(appContext, params) {

    override suspend fun doWork(): Result {
        return runCatching {
            repository.ensureBuiltinImported(force = false)
            Result.success()
        }.getOrElse { throwable ->
            Timber.e(throwable, "Seed content worker failed")
            if (runAttemptCount < 3) Result.retry() else Result.failure()
        }
    }
}

@HiltWorker
class ReviewReminderWorker @AssistedInject constructor(
    @Assisted appContext: Context,
    @Assisted params: WorkerParameters,
    private val repository: CalibratorRepository,
    private val settingsStore: AppSettingsStore,
) : CoroutineWorker(appContext, params) {

    override suspend fun doWork(): Result {
        val settings = settingsStore.snapshot()
        if (!settings.remindersEnabled) return Result.success()
        val dueCount = repository.dueCountNow()
        if (dueCount <= 0) return Result.success()
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU &&
            ContextCompat.checkSelfPermission(
                applicationContext,
                Manifest.permission.POST_NOTIFICATIONS,
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            return Result.success()
        }

        val launchIntent = Intent(applicationContext, MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(
            applicationContext,
            0,
            launchIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE,
        )

        val notification = NotificationCompat.Builder(applicationContext, REVIEW_CHANNEL_ID)
            .setSmallIcon(android.R.drawable.ic_media_play)
            .setContentTitle(applicationContext.getString(R.string.app_name))
            .setContentText("今日有 $dueCount 条待校准项目，打开开始 session。")
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .build()

        val manager = ContextCompat.getSystemService(
            applicationContext,
            NotificationManager::class.java,
        ) ?: return Result.success()
        manager.notify(3001, notification)
        return Result.success()
    }
}

@Singleton
class AppWorkScheduler @Inject constructor(
    private val settingsStore: AppSettingsStore,
    private val repository: CalibratorRepository,
    @dagger.hilt.android.qualifiers.ApplicationContext private val context: Context,
) {

    fun scheduleBootstrap() {
        ensureNotificationChannel()
        val workManager = WorkManager.getInstance(context)
        workManager.enqueueUniqueWork(
            SEED_WORK_NAME,
            ExistingWorkPolicy.KEEP,
            OneTimeWorkRequestBuilder<SeedContentWorker>().build(),
        )
        workManager.enqueueUniquePeriodicWork(
            REVIEW_WORK_NAME,
            ExistingPeriodicWorkPolicy.UPDATE,
            PeriodicWorkRequestBuilder<ReviewReminderWorker>(24, TimeUnit.HOURS).build(),
        )
    }

    suspend fun refreshBuiltInContent() {
        repository.ensureBuiltinImported(force = true)
    }

    suspend fun setRemindersEnabled(enabled: Boolean) {
        settingsStore.setRemindersEnabled(enabled)
    }

    private fun ensureNotificationChannel() {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) return
        val manager = ContextCompat.getSystemService(context, NotificationManager::class.java) ?: return
        val channel = NotificationChannel(
            REVIEW_CHANNEL_ID,
            "Canto review reminders",
            NotificationManager.IMPORTANCE_DEFAULT,
        )
        manager.createNotificationChannel(channel)
    }
}
