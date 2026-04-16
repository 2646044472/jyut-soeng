package dev.local.yuecal.data

import kotlinx.serialization.Serializable

@Serializable
data class ContentBundle(
    val version: String,
    val generatedAt: String,
    val entries: List<ContentEntryAsset>,
)

@Serializable
data class ContentEntryAsset(
    val id: String,
    val displayText: String,
    val promptText: String,
    val answerJyutping: String,
    val gloss: String = "",
    val notes: String = "",
    val usageTip: String = "",
    val exampleSentence: String = "",
    val exampleTranslation: String = "",
    val entryType: String = "word",
    val category: String = "",
    val groupId: String = "",
    val tone: Int = 0,
    val audioAsset: String? = null,
    val sourceLabel: String = "import",
)
