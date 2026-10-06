from datetime import datetime, timezone

import httpx

from app.config import settings


class TrendScout:
    async def run(self, topic: str, market: str) -> dict:
        if not settings.youtube_api_key:
            return {
                "status": "provider_not_configured",
                "topic": topic,
                "market": market,
                "trends": [{"query": topic, "source": "user_topic"}],
                "sources": [],
                "live_data": False,
            }

        params = {
            "part": "snippet",
            "q": topic,
            "type": "video",
            "order": "viewCount",
            "maxResults": settings.youtube_trend_results,
            "regionCode": market.upper(),
            "key": settings.youtube_api_key,
        }
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get("https://www.googleapis.com/youtube/v3/search", params=params)
            response.raise_for_status()
            data = response.json()

        trends = []
        for item in data.get("items", []):
            snippet = item.get("snippet", {})
            video_id = item.get("id", {}).get("videoId")
            trends.append({
                "title": snippet.get("title", ""),
                "channel": snippet.get("channelTitle", ""),
                "published_at": snippet.get("publishedAt"),
                "video_id": video_id,
                "url": f"https://www.youtube.com/watch?v={video_id}" if video_id else None,
            })

        return {
            "status": "ready",
            "topic": topic,
            "market": market,
            "trends": trends,
            "sources": ["youtube_data_api"],
            "live_data": True,
            "captured_at": datetime.now(timezone.utc).isoformat(),
        }
