package dev.local.yuecal

import android.app.Application
import android.util.Log
import androidx.work.Configuration
import androidx.hilt.work.HiltWorkerFactory
import dagger.hilt.android.HiltAndroidApp
import dev.local.yuecal.work.AppWorkScheduler
import javax.inject.Inject
import timber.log.Timber

@HiltAndroidApp
class CantoCalibratorApp : Application(), Configuration.Provider {

    @Inject
    lateinit var workerFactory: HiltWorkerFactory

    @Inject
    lateinit var workScheduler: AppWorkScheduler

    override val workManagerConfiguration: Configuration
        get() = Configuration.Builder()
            .setWorkerFactory(workerFactory)
            .setMinimumLoggingLevel(Log.INFO)
            .build()

    override fun onCreate() {
        super.onCreate()
        Timber.plant(Timber.DebugTree())
        workScheduler.scheduleBootstrap()
    }
}
