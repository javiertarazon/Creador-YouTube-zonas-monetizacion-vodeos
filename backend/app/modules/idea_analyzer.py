from app.providers.openai_model import OpenAIModelProvider


class IdeaAnalyzer:
    def __init__(self, llm=None):
        self.llm = llm or OpenAIModelProvider()

    async def run(self, scout: dict, language: str) -> dict:
        prompt = f"""Analiza esta idea para YouTube.
Tema: {scout['topic']}
Mercado: {scout['market']}
Idioma: {language}
Devuelve: angle, audience, hook, risks y originality. No copies contenido de terceros."""
        return {"analysis": await self.llm.generate(prompt, system="Eres un estratega editorial de YouTube.")}

