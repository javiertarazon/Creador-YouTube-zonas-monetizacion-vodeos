# Creador YouTube — Open Source Factory

Pipeline modular para producción de videos de YouTube, basado en componentes open-source y con revisión humana antes de publicar.

## Stack
- Python 3.11 + FastAPI
- Ollama para LLM local
- faster-whisper para STT
- Piper como adaptador TTS
- FFmpeg para procesamiento multimedia
- Remotion + React para composición
- PostgreSQL, Redis y MinIO para infraestructura

## Pipeline
Trend Scout → Idea Analyzer → Creative Transformer → Script Writer → Voice/Assets → Video Composer → Quality Gate → Human Review → Publisher → Analytics.

## Reglas del flujo
- No copiar literalmente guiones, frases o estructura de videos de referencia.
- No reutilizar assets de terceros sin licencia compatible.
- La publicación automática está desactivada por defecto.
- Quality Gate: puntuación mínima configurable, 8/10 por defecto.
- Objetivo de audio: -14 LUFS.

## Arranque local
1. Copia .env.example a .env.
2. Ejecuta docker compose up --build.
3. Descarga un modelo: docker compose exec ollama ollama pull llama3.2:3b.
4. API: GET /health.
5. Pipeline: POST /pipeline/run.

## Estado
Base funcional inicial implementada. Trend Scout y Publisher requieren integrar proveedores concretos antes de producción; la publicación automática permanece bloqueada.
