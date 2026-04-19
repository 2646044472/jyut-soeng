package dev.local.yuecal.di

import android.content.Context
import androidx.room.Room
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import dev.local.yuecal.data.AppDatabase
import dev.local.yuecal.data.EntryDao
import dev.local.yuecal.data.MIGRATION_3_4
import dev.local.yuecal.data.ProgressDao
import dev.local.yuecal.data.SessionDao
import javax.inject.Qualifier
import javax.inject.Singleton
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.Dispatchers
import kotlinx.serialization.json.Json

@Qualifier
annotation class IoDispatcher

@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides
    @Singleton
    fun provideJson(): Json = Json {
        ignoreUnknownKeys = true
        prettyPrint = true
        isLenient = true
    }

    @Provides
    @Singleton
    @IoDispatcher
    fun provideIoDispatcher(): CoroutineDispatcher = Dispatchers.IO

    @Provides
    @Singleton
    fun provideDatabase(
        @ApplicationContext context: Context,
    ): AppDatabase = Room.databaseBuilder(
        context,
        AppDatabase::class.java,
        "canto_calibrator.db",
    ).addMigrations(MIGRATION_3_4).build()

    @Provides
    fun provideEntryDao(database: AppDatabase): EntryDao = database.entryDao()

    @Provides
    fun provideProgressDao(database: AppDatabase): ProgressDao = database.progressDao()

    @Provides
    fun provideSessionDao(database: AppDatabase): SessionDao = database.sessionDao()
}
