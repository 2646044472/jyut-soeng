package dev.local.yuecal.domain

data class AppReleaseInfo(
    val version: String,
    val tagName: String,
    val releaseUrl: String,
    val apkDownloadUrl: String,
)
