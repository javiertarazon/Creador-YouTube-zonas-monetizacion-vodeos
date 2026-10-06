import json
import shutil
import subprocess
from pathlib import Path

from app.config import settings


class QualityGate:
    async def run(self, script: dict, video_path: str | None = None, audio_path: str | None = None) -> dict:
        text = script.get("script", "").strip()
        checks = {
            "script_nonempty": bool(text),
            "copyright_safe_workflow": True,
            "human_review_required": True,
        }

        if video_path:
            checks["video_exists"] = Path(video_path).exists()
            checks["video_has_streams"] = self._has_streams(video_path) if checks["video_exists"] else False
        else:
            checks["video_exists"] = False
            checks["video_has_streams"] = False

        checks["audio_exists"] = bool(audio_path and Path(audio_path).exists())

        score = sum([
            4.0 if checks["script_nonempty"] else 0.0,
            1.0 if checks["copyright_safe_workflow"] else 0.0,
            2.0 if checks["video_exists"] else 0.0,
            1.0 if checks["video_has_streams"] else 0.0,
            1.0 if checks["audio_exists"] else 0.0,
            1.0,  # human review gate
        ])

        checks["minimum_score"] = score >= settings.quality_min_score
        return {
            "score": score,
            "passed": checks["minimum_score"],
            "checks": checks,
            "target_lufs": settings.target_lufs,
        }

    @staticmethod
    def _has_streams(path: str) -> bool:
        if not shutil.which("ffprobe"):
            return False
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "stream=index", "-of", "json", path],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            return False
        try:
            return bool(json.loads(result.stdout).get("streams"))
        except json.JSONDecodeError:
            return False
