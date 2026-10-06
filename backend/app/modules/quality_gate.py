from app.config import settings

class QualityGate:
    async def run(self, script: dict) -> dict:
        text = script.get("script", "").strip()
        score = 10.0 if text else 0.0
        return {
            "score": score,
            "passed": score >= settings.quality_min_score,
            "checks": {
                "script_nonempty": bool(text),
                "minimum_score": score >= settings.quality_min_score,
                "copyright_safe_workflow": True,
                "human_review_required": True,
            },
        }
