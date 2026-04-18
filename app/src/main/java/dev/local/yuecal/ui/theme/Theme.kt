package dev.local.yuecal.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val LightColors = lightColorScheme(
    primary = Color(0xFF256F63),
    onPrimary = Color(0xFFFFFFFF),
    primaryContainer = Color(0xFFD9F2EC),
    onPrimaryContainer = Color(0xFF113A33),
    secondary = Color(0xFFB36A18),
    onSecondary = Color(0xFFFFFFFF),
    secondaryContainer = Color(0xFFF9E6CF),
    onSecondaryContainer = Color(0xFF5D3300),
    background = Color(0xFFF7F5EF),
    onBackground = Color(0xFF1C1B18),
    surface = Color(0xFFFFFFFF),
    onSurface = Color(0xFF1E1D1A),
    surfaceVariant = Color(0xFFEAE6DE),
    onSurfaceVariant = Color(0xFF5E5A53),
    outline = Color(0xFFD3CBBE),
    error = Color(0xFFB3261E),
    errorContainer = Color(0xFFF9DEDC),
)

private val DarkColors = darkColorScheme(
    primary = Color(0xFF90D5C5),
    onPrimary = Color(0xFF123A33),
    primaryContainer = Color(0xFF1C4C43),
    onPrimaryContainer = Color(0xFFD9F2EC),
    secondary = Color(0xFFF1B56A),
    onSecondary = Color(0xFF5D3300),
    secondaryContainer = Color(0xFF7A4712),
    onSecondaryContainer = Color(0xFFF9E6CF),
    background = Color(0xFF141413),
    onBackground = Color(0xFFF2F1EC),
    surface = Color(0xFF1C1C1A),
    onSurface = Color(0xFFF3F1EB),
    surfaceVariant = Color(0xFF31302D),
    onSurfaceVariant = Color(0xFFD1CBC1),
    outline = Color(0xFF807A72),
    error = Color(0xFFF2B8B5),
    errorContainer = Color(0xFF8C1D18),
)

@Composable
fun CantoCalibratorTheme(
    useDarkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit,
) {
    MaterialTheme(
        colorScheme = if (useDarkTheme) DarkColors else LightColors,
        content = content,
    )
}
