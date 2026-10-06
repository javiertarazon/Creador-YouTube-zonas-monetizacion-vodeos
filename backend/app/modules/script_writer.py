from app.providers.ollama import OllamaProvider

class ScriptWriter:
    def __init__(self, llm=None):
        self.llm = llm or OllamaProvider()

    async def run(self, concept: dict, language: str, duration_seconds: int) -> dict:
        prompt = f"""Escribe un guion original para YouTube en {language}.
Duración objetivo: {duration_seconds} segundos.
Concepto:
{concept['concept']}
Incluye hook inicial, desarrollo, cierre y CTA. No copies textos de terceros."""
        return {"script": await self.llm.generate(prompt)}
