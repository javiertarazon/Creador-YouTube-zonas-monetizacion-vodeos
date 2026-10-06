from app.providers.openai_model import OpenAIModelProvider


class CreativeTransformer:
    def __init__(self, llm=None):
        self.llm = llm or OpenAIModelProvider()

    async def run(self, idea: dict) -> dict:
        prompt = f"""Convierte el análisis en un concepto original de video.
Análisis:
{idea['analysis']}
Crea una estructura propia y evita copiar guiones, frases o recursos de videos de referencia."""
        return {"concept": await self.llm.generate(prompt, system="Eres un director creativo de contenido original.")}

