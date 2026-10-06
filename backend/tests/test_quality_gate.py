import subprocess

import pytest

from app.modules.quality_gate import QualityGate


@pytest.mark.asyncio
async def test_quality_gate_passes_nonempty_script():
    result = await QualityGate().run({"script": "Guion de prueba"})
    assert result["passed"] is True
    assert result["score"] >= 8


@pytest.mark.asyncio
async def test_quality_gate_validates_real_ffmpeg_media(tmp_path):
    video = tmp_path / "test.mp4"
    audio = tmp_path / "test.wav"

    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=320x180:d=1",
        "-f", "lavfi", "-i", "sine=frequency=440:duration=1",
        "-c:v", "libx264", "-c:a", "pcm_s16le", str(video),
    ], check=True, capture_output=True)

    subprocess.run([
        "ffmpeg", "-y", "-i", str(video), "-vn", "-c:a", "pcm_s16le", str(audio),
    ], check=True, capture_output=True)

    result = await QualityGate().run(
        {"script": "Guion de prueba"},
        video_path=str(video),
        audio_path=str(audio),
    )
    assert result["checks"]["video_exists"] is True
    assert result["checks"]["video_has_streams"] is True
    assert result["checks"]["audio_exists"] is True
    assert result["passed"] is True
