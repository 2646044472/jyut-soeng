package dev.local.yuecal.data

import dev.local.yuecal.domain.SessionMode
import kotlin.random.Random

internal fun orderSessionEntries(
    entries: List<CalibrationEntryEntity>,
    mode: SessionMode,
    entryType: String?,
    random: Random = Random.Default,
): List<CalibrationEntryEntity> {
    return if (mode == SessionMode.Learn && entryType == "sentence") {
        entries.sortedWith(
            compareByDescending<CalibrationEntryEntity> { it.storyReviewed }
                .thenBy { it.sortOrder }
                .thenBy { it.id },
        )
    } else {
        entries.shuffled(random)
    }
}
