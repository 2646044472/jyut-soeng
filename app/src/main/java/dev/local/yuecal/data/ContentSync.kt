package dev.local.yuecal.data

internal data class ManagedEntrySyncPlan(
    val aliasTargetByEntryId: Map<String, String>,
    val archiveEntryIds: Set<String>,
)

internal object ManagedEntrySyncPlanner {
    private val managedSourceLabels = setOf("builtin", "github")

    fun plan(
        existingEntries: List<CalibrationEntryEntity>,
        incomingEntries: List<ContentEntryAsset>,
    ): ManagedEntrySyncPlan {
        val managedEntries = existingEntries.filter { it.sourceLabel in managedSourceLabels }
        val activeManagedEntries = managedEntries.filter { it.isActive }
        val incomingIds = incomingEntries.mapTo(linkedSetOf()) { it.id }
        val incomingKeys = incomingEntries.mapTo(linkedSetOf()) { it.canonicalKey() }
        val existingByKey = managedEntries.groupBy { it.canonicalKey() }
        val aliasTargetByEntryId = buildMap {
            incomingEntries.forEach { incoming ->
                existingByKey[incoming.canonicalKey()].orEmpty()
                    .asSequence()
                    .map { it.id }
                    .filter { it != incoming.id }
                    .forEach { sourceId ->
                        put(sourceId, incoming.id)
                    }
            }
        }
        val archiveEntryIds = activeManagedEntries
            .asSequence()
            .filter { it.id !in incomingIds }
            .filter { entry ->
                entry.id in aliasTargetByEntryId || entry.canonicalKey() !in incomingKeys
            }
            .map { it.id }
            .toSet()
        return ManagedEntrySyncPlan(
            aliasTargetByEntryId = aliasTargetByEntryId,
            archiveEntryIds = archiveEntryIds,
        )
    }
}

internal object ReviewProgressMerger {
    fun merge(targetId: String, records: List<ReviewProgressEntity>): ReviewProgressEntity? {
        if (records.isEmpty()) return null
        val anchor = records.maxWithOrNull(
            compareBy<ReviewProgressEntity>(
                { it.repetitions },
                { it.intervalDays },
                { it.totalAttempts },
                { it.lastReviewedAt ?: 0L },
                { it.nextReviewEpochDay },
            ),
        ) ?: return null
        return anchor.copy(
            entryId = targetId,
            nextReviewEpochDay = records.minOf { it.nextReviewEpochDay },
            lastReviewedAt = records.mapNotNull { it.lastReviewedAt }.maxOrNull(),
            totalCorrect = records.sumOf { it.totalCorrect },
            totalAttempts = records.sumOf { it.totalAttempts },
            streak = records.maxOf { it.streak },
        )
    }
}

internal fun canonicalEntryKey(
    entryType: String,
    displayText: String,
    answerJyutping: String,
): String = listOf(
    entryType.normalizeCanonicalValue(),
    displayText.normalizeCanonicalValue(),
    answerJyutping.normalizeCanonicalValue(),
).joinToString(separator = "|")

private fun ContentEntryAsset.canonicalKey(): String = canonicalEntryKey(
    entryType = entryType,
    displayText = displayText,
    answerJyutping = answerJyutping,
)

private fun CalibrationEntryEntity.canonicalKey(): String = canonicalEntryKey(
    entryType = entryType,
    displayText = displayText,
    answerJyutping = answerJyutping,
)

private fun String.normalizeCanonicalValue(): String = trim()
    .lowercase()
    .replace(Regex("\\s+"), " ")
