from pathlib import Path
import json


class Publisher:
    """Manual publication handoff.

    YouTube API credentials and automatic publication are intentionally not
    enabled. The module produces a ready-to-upload manifest instead.
    """

    async def prepare(self, video_path: str, title: str, description: str = "") -> dict:
        path = Path(video_path)
        if not path.exists():
            raise FileNotFoundError(video_path)

        manifest_path = path.with_suffix(".publish.json")
        payload = {
            "video": str(path),
            "title": title,
            "description": description,
            "auto_publish": False,
            "requires_human_confirmation": True,
        }
        manifest_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return payload | {"manifest": str(manifest_path)}
