class TrendScout:
    async def run(self, topic: str, market: str) -> dict:
        return {"status": "ready_for_provider", "topic": topic, "market": market, "trends": [], "sources": []}
