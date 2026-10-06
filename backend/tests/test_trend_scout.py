import pytest

from app.modules.trend_scout import TrendScout


@pytest.mark.asyncio
async def test_trend_scout_returns_requested_topic_and_market():
    result = await TrendScout().run("IA generativa", "US")

    assert result["status"] == "ready_for_provider"
    assert result["topic"] == "IA generativa"
    assert result["market"] == "US"
    assert result["trends"] == []
    assert result["sources"] == []
