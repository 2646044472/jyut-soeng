package dev.local.yuecal.data

import kotlin.random.Random

internal fun orderSessionEntries(
    entries: List<CalibrationEntryEntity>,
    random: Random = Random.Default,
): List<CalibrationEntryEntity> {
    return entries.shuffled(random)
}
