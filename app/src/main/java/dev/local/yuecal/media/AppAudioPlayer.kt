package dev.local.yuecal.media

import android.content.Context
import android.net.Uri
import androidx.media3.common.MediaItem
import androidx.media3.exoplayer.ExoPlayer
import dagger.hilt.android.qualifiers.ApplicationContext
import java.io.File
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AppAudioPlayer @Inject constructor(
    @ApplicationContext context: Context,
) {

    private val player = ExoPlayer.Builder(context).build()

    fun playAsset(assetPath: String?) {
        if (assetPath.isNullOrBlank()) return
        val uri = when {
            assetPath.startsWith("http://") || assetPath.startsWith("https://") || assetPath.startsWith("file:") -> {
                Uri.parse(assetPath)
            }

            assetPath.startsWith("/") -> Uri.fromFile(File(assetPath))
            else -> Uri.parse("asset:///$assetPath")
        }
        player.setMediaItem(MediaItem.fromUri(uri))
        player.prepare()
        player.playWhenReady = true
    }

    fun stop() {
        player.stop()
    }
}
