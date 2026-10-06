import pytest

from app.providers.ollama import OllamaProvider


class FakeResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {"response": "respuesta de prueba"}


class FakeClient:
    def __init__(self, *args, **kwargs):
        self.posted = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def post(self, url, json):
        self.posted = (url, json)
        return FakeResponse()


@pytest.mark.asyncio
async def test_ollama_generate_posts_expected_payload(monkeypatch):
    client = FakeClient()

    import app.providers.ollama as ollama_module

    monkeypatch.setattr(ollama_module.httpx, "AsyncClient", lambda **kwargs: client)

    provider = OllamaProvider()
    result = await provider.generate("Escribe una idea", system="Eres creativo")

    assert result == "respuesta de prueba"
    assert client.posted[0].endswith("/api/generate")
    assert client.posted[1]["prompt"] == "Escribe una idea"
    assert client.posted[1]["system"] == "Eres creativo"
    assert client.posted[1]["stream"] is False
