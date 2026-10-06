import pytest

from app.modules.pipeline import FactoryPipeline


class FakeScout:
    async def run(self, topic, market):
        return {"topic": topic, "market": market, "trends": [], "sources": []}


class FakeIdea:
    async def run(self, scout, language):
        return {"analysis": f"analysis:{scout['topic']}:{language}"}


class FakeTransform:
    async def run(self, idea):
        return {"concept": f"concept:{idea['analysis']}"}


class FakeScript:
    async def run(self, concept, language, duration_seconds):
        return {"script": f"script:{concept['concept']}:{language}:{duration_seconds}"}


class FakeAssets:
    def build(self, **kwargs):
        return {"assets": [], "manifest": "manifest.json"}


class FakeVoice:
    def available(self):
        return False


class FakeComposer:
    def render(self, props, output):
        return {"video": output, "renderer": "fake"}


class FakeQuality:
    async def run(self, script, video_path=None, audio_path=None):
        return {"score": 10.0, "passed": True, "checks": {"minimum_score": True}}


class FakePublisher:
    async def prepare(self, video_path, title, description=""):
        return {"auto_publish": False, "requires_human_confirmation": True}


class FakeAnalytics:
    def record(self, run_id, metrics, output_dir):
        return {"run_id": run_id, "metrics": metrics}


@pytest.mark.asyncio
async def test_pipeline_orchestrates_all_stages_and_requires_human_review():
    pipeline = FactoryPipeline()
    pipeline.scout = FakeScout()
    pipeline.idea = FakeIdea()
    pipeline.transform = FakeTransform()
    pipeline.script = FakeScript()
    pipeline.assets = FakeAssets()
    pipeline.voice = FakeVoice()
    pipeline.composer = FakeComposer()
    pipeline.quality = FakeQuality()
    pipeline.publisher = FakePublisher()
    pipeline.analytics = FakeAnalytics()

    result = await pipeline.run(
        topic="Historia",
        language="es",
        market="US",
        duration_seconds=90,
        publish=True,
    )

    assert result["status"] == "ready_for_human_review"
    assert result["human_review_required"] is True
    assert result["auto_publish_enabled"] is False
    assert result["publish_requested"] is True
    assert result["stages"]["script_writer"]["script"].startswith("script:")
    assert "assets" in result["stages"]
    assert "video_composer" in result["stages"]
    assert "publisher" in result["stages"]
