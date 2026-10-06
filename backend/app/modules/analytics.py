from pathlib import Path
import json
from datetime import datetime, timezone


class AnalyticsFeedback:
    def record(self, run_id: str, metrics: dict, output_dir: str) -> dict:
        root = Path(output_dir)
        root.mkdir(parents=True, exist_ok=True)
        payload = {
            "run_id": run_id,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "metrics": metrics,
        }
        path = root / f"{run_id}.analytics.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return payload | {"path": str(path)}
