import httpx
from app.config import settings

class OllamaProvider:
    def __init__(self):
        self.base_url = settings.ollama_base_url.rstrip("/")

    async def generate(self, prompt: str, system: str = "") -> str:
        payload = {"model": settings.ollama_model, "prompt": prompt, "system": system, "stream": False}
        async with httpx.AsyncClient(timeout=180) as client:
            response = await client.post(f"{self.base_url}/api/generate", json=payload)
            response.raise_for_status()
            return response.json().get("response", "").strip()
