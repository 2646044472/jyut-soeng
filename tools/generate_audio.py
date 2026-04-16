#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import struct
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUNDLE_PATH = ROOT / "app" / "src" / "main" / "assets" / "builtin" / "content.json"
ASSET_ROOT = ROOT / "app" / "src" / "main" / "assets"

SAMPLE_RATE = 16_000
DURATION_SECONDS = 0.72
AMPLITUDE = 0.32

TONE_CONTOURS = {
    1: (880.0, 880.0),
    2: (720.0, 900.0),
    3: (660.0, 660.0),
    4: (620.0, 430.0),
    5: (430.0, 650.0),
    6: (430.0, 430.0),
}


def envelope(position: float) -> float:
    fade = 0.08
    if position < fade:
        return position / fade
    if position > 1 - fade:
        return (1 - position) / fade
    return 1.0


def write_wave(path: Path, tone: int) -> None:
    start_freq, end_freq = TONE_CONTOURS[tone]
    frames = int(SAMPLE_RATE * DURATION_SECONDS)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        phase = 0.0
        for index in range(frames):
            progress = index / max(1, frames - 1)
            freq = start_freq + (end_freq - start_freq) * progress
            phase += (2.0 * math.pi * freq) / SAMPLE_RATE
            value = math.sin(phase) * AMPLITUDE * envelope(progress)
            wav_file.writeframes(struct.pack("<h", int(max(-1.0, min(1.0, value)) * 32767)))


def main() -> None:
    bundle = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))
    for entry in bundle["entries"]:
        relative_path = entry["audioAsset"]
        output_path = ASSET_ROOT / relative_path
        write_wave(output_path, int(entry["tone"]))
    print(f"Generated {len(bundle['entries'])} wav files in {ASSET_ROOT / 'audio' / 'generated'}")


if __name__ == "__main__":
    main()
