import httpx
from app.config import settings


class OpenAIModelProvider:
    """Provider for OpenAI Responses API.

    The ChatGPT session itself cannot be embedded into a deployed app. The
    production equivalent is the OpenAI API, configured with OPENAI_API_KEY.
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or settings.openai_api_key
        self.base_url = settings.openai_base_url.rstrip("/")
        self.model = settings.openai_model

    async def generate(self, prompt: str, system: str = "") -> str:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY no está configurada.")

        payload = {
            "model": self.model,
            "instructions": system,
            "input": prompt,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=settings.model_timeout_seconds) as client:
            response = await client.post(
                f"{self.base_url}/responses",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()

        output_text = data.get("output_text")
        if output_text:
            return output_text.strip()

        chunks: list[str] = []
        for item in data.get("output", []):
            for content in item.get("content", []):
                if content.get("type") in {"output_text", "text"}:
                    text = content.get("text", "")
                    if text:
                        chunks.append(text)
        return "\n".join(chunks).strip()
