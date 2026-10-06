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


class FakeQuality:
    async def run(self, script):
        return {
            "score": 10.0,
            "passed": True,
            "checks": {"script_nonempty": True, "minimum_score": True},
        }


@pytest.mark.asyncio
async def test_pipeline_orchestrates_stages_and_requires_human_review():
    pipeline = FactoryPipeline()
    pipeline.scout = FakeScout()
    pipeline.idea = FakeIdea()
    pipeline.transform = FakeTransform()
    pipeline.script = FakeScript()
    pipeline.quality = FakeQuality()

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
