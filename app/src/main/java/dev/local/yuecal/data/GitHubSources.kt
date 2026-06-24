package dev.local.yuecal.data

object GitHubSources {
    const val REPO_OWNER = "2646044472"
    const val REPO_NAME = "jyut-soeng"
    const val REPO_WEB_URL = "https://github.com/2646044472/jyut-soeng"
    const val RELEASES_URL = "$REPO_WEB_URL/releases"
    const val LATEST_RELEASE_API_URL = "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/releases/latest"
    const val LATEST_APK_URL = "$RELEASES_URL/latest/download/yuet-soeng-latest.apk"
    const val CONTENT_PACK_URL = "$RELEASES_URL/latest/download/yuet-soeng-content.zip"
}
