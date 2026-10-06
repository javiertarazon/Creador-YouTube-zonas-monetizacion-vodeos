from pathlib import Path
from uuid import uuid4

from app.config import settings
from app.modules.analytics import AnalyticsFeedback
from app.modules.assets import AssetManager
from app.modules.composer import VideoComposer
from app.modules.publisher import Publisher
from app.modules.quality_gate import QualityGate
from app.modules.script_writer import ScriptWriter
from app.modules.trend_scout import TrendScout
from app.modules.idea_analyzer import IdeaAnalyzer
from app.modules.creative_transformer import CreativeTransformer
from app.modules.voice import PiperVoice


class FactoryPipeline:
    def __init__(self):
        self.scout = TrendScout()
        self.idea = IdeaAnalyzer()
        self.transform = CreativeTransformer()
        self.script = ScriptWriter()
        self.assets = AssetManager()
        self.voice = PiperVoice()
        self.composer = VideoComposer()
        self.quality = QualityGate()
        self.publisher = Publisher()
        self.analytics = AnalyticsFeedback()

    async def run(
        self,
        topic: str,
        language: str,
        market: str,
        duration_seconds: int,
        publish: bool = False,
        render_video: bool = True,
    ) -> dict:
        run_id = uuid4().hex[:12]
        root = Path(settings.output_dir) / run_id
        root.mkdir(parents=True, exist_ok=True)

        scout = await self.scout.run(topic, market)
        idea = await self.idea.run(scout, language)
        concept = await self.transform.run(idea)
        script = await self.script.run(concept, language, duration_seconds)

        assets = self.assets.build(
            title=topic,
            topic=topic,
            output_dir=str(root / "assets"),
        )

        voice = {"status": "not_configured", "audio": None}
        if settings.piper_model and self.voice.available():
            audio = self.voice.synthesize(
                script["script"],
                output=str(root / "voice.wav"),
            )
            voice = {"status": "ready", "audio": audio}
        elif settings.piper_model:
            voice = {"status": "piper_unavailable", "audio": None}

        video = {"status": "not_requested", "video": None}
        if render_video:
            video_path = root / "video.mp4"
            video = self.composer.render(
                {
                    "title": topic,
                    "topic": topic,
                    "script": script["script"],
                    "duration_seconds": duration_seconds,
                    "assets": assets["assets"],
                    "voice_audio": voice["audio"],
                },
                str(video_path),
            )

        quality = await self.quality.run(
            script,
            video_path=video.get("video"),
            audio_path=voice.get("audio"),
        )

        publication = await self.publisher.prepare(
            video["video"], topic
        ) if publish and video.get("video") else {
            "auto_publish": False,
            "requires_human_confirmation": True,
            "status": "manual_review_required",
        }

        analytics = self.analytics.record(
            run_id,
            {"quality_score": quality["score"], "video_rendered": bool(video.get("video"))},
            str(root),
        )

        return {
            "status": "ready_for_human_review" if quality["passed"] else "quality_failed",
            "human_review_required": True,
            "auto_publish_enabled": False,
            "publish_requested": publish,
            "run_id": run_id,
            "stages": {
                "trend_scout": scout,
                "idea_analyzer": idea,
                "creative_transformer": concept,
                "script_writer": script,
                "assets": assets,
                "voice": voice,
                "video_composer": video,
                "quality_gate": quality,
                "publisher": publication,
                "analytics": analytics,
            },
        }
