import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.modules.pipeline import FactoryPipeline


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_pipeline_api_contract_without_external_llm():
    class FakeScout:
        async def run(self, topic, market):
            return {"topic": topic, "market": market, "trends": [], "sources": []}

    class FakeIdea:
        async def run(self, scout, language):
            return {"analysis": "analysis"}

    class FakeTransform:
        async def run(self, idea):
            return {"concept": "concept"}

    class FakeScript:
        async def run(self, concept, language, duration_seconds):
            return {"script": "script"}

    class FakeQuality:
        async def run(self, script):
            return {"score": 10.0, "passed": True, "checks": {"minimum_score": True}}

    pipeline = FactoryPipeline()
    pipeline.scout = FakeScout()
    pipeline.idea = FakeIdea()
    pipeline.transform = FakeTransform()
    pipeline.script = FakeScript()
    pipeline.quality = FakeQuality()
    app.dependency_overrides = {}

    result = await pipeline.run("Tecnología", "es", "US", 60, publish=True)
    assert result["status"] == "ready_for_human_review"
    assert result["human_review_required"] is True
    assert result["auto_publish_enabled"] is False
    assert result["publish_requested"] is True
