import pytest

from app.providers.openai_model import OpenAIModelProvider


class FakeResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {"output_text": "respuesta de prueba"}


class FakeClient:
    def __init__(self, *args, **kwargs):
        self.posted = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def post(self, url, json, headers):
        self.posted = (url, json, headers)
        return FakeResponse()


@pytest.mark.asyncio
async def test_openai_generate_posts_expected_responses_payload(monkeypatch):
    client = FakeClient()

    import app.providers.openai_model as module

    monkeypatch.setattr(module.httpx, "AsyncClient", lambda **kwargs: client)
    provider = OpenAIModelProvider(api_key="test-key")
    result = await provider.generate("Escribe una idea", system="Eres creativo")

    assert result == "respuesta de prueba"
    assert client.posted[0].endswith("/responses")
    assert client.posted[1]["model"] == provider.model
    assert client.posted[1]["input"] == "Escribe una idea"
    assert client.posted[1]["instructions"] == "Eres creativo"
    assert client.posted[2]["Authorization"] == "Bearer test-key"
