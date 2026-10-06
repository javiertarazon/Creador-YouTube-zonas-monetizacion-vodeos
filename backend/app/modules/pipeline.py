from app.modules.trend_scout import TrendScout
from app.modules.idea_analyzer import IdeaAnalyzer
from app.modules.creative_transformer import CreativeTransformer
from app.modules.script_writer import ScriptWriter
from app.modules.quality_gate import QualityGate

class FactoryPipeline:
    def __init__(self):
        self.scout = TrendScout()
        self.idea = IdeaAnalyzer()
        self.transform = CreativeTransformer()
        self.script = ScriptWriter()
        self.quality = QualityGate()

    async def run(self, topic: str, language: str, market: str, duration_seconds: int, publish: bool = False) -> dict:
        scout = await self.scout.run(topic, market)
        idea = await self.idea.run(scout, language)
        concept = await self.transform.run(idea)
        script = await self.script.run(concept, language, duration_seconds)
        quality = await self.quality.run(script)
        return {
            "status": "ready_for_human_review" if quality["passed"] else "quality_failed",
            "human_review_required": True,
            "auto_publish_enabled": False,
            "publish_requested": publish,
            "stages": {
                "trend_scout": scout,
                "idea_analyzer": idea,
                "creative_transformer": concept,
                "script_writer": script,
                "quality_gate": quality,
            },
        }
