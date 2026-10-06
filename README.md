# Creador YouTube — Open Source Factory

Pipeline modular para producir videos de YouTube con generación de contenido, voz, assets, composición Remotion, controles de calidad y revisión humana antes de publicar.

## Stack
- Python 3.11 + FastAPI
- OpenAI Responses API como proveedor de modelo (configurable por OPENAI_MODEL)
- YouTube Data API opcional para Trend Scout en vivo
- Piper TTS para voz local
- FFmpeg/ffprobe para procesamiento y validación multimedia
- Remotion + React para composición/render real
- PostgreSQL, Redis y MinIO preparados como infraestructura

> La aplicación no puede incrustar directamente el modelo de esta conversación. Para producción se conecta al modelo mediante la API de OpenAI usando OPENAI_API_KEY. La integración usa Responses API. citeturn0search0

## Pipeline
Trend Scout → Idea Analyzer → Creative Transformer → Script Writer → Assets → Piper Voice → Remotion → FFmpeg/Quality Gate → Human Review → Publisher Manifest → Analytics.

## Funcionalidades implementadas
- **Trend Scout:** búsqueda real en YouTube Data API cuando YOUTUBE_API_KEY está configurada; sin clave, declara explícitamente que está usando solo el tema suministrado. La API search.list permite buscar videos por consulta, región y orden. citeturn1search0
- **Idea Analyzer / Creative Transformer / Script Writer:** usan el proveedor OpenAI Responses.
- **Assets:** genera SVG originales y un manifest.json auditable; no descarga assets de terceros silenciosamente.
- **Piper:** sintetiza el guion a WAV cuando PIPER_MODEL y el binario Piper están disponibles.
- **Remotion:** composición dinámica por props, duración configurable y audio opcional.
- **FFmpeg:** mux de audio y normalización LUFS.
- **Quality Gate:** comprueba guion, existencia de video, streams multimedia, audio y revisión humana; mínimo 8/10 por defecto.
- **Publisher:** genera un manifiesto listo para carga; la publicación automática permanece bloqueada.
- **Analytics:** guarda métricas de cada ejecución en JSON.

## Configuración
Copia .env.example a .env y configura como mínimo:
- OPENAI_API_KEY
- OPENAI_MODEL
- PIPER_MODEL si quieres voz
- YOUTUBE_API_KEY si quieres tendencias reales de YouTube

La API de YouTube devuelve resultados de video, canal o playlist y permite limitar la búsqueda a type=video. citeturn1search0turn1search1

## Arranque con Docker
1. Copia .env.example a .env.
2. Ejecuta docker compose up --build.
3. Comprueba GET /health.
4. Ejecuta POST /pipeline/run.

La imagen de API instala FFmpeg, Node/npm, Python y las dependencias de Remotion. La publicación automática sigue deshabilitada.

## Pruebas
GitHub Actions ejecuta tres verificaciones:
1. **Python + FFmpeg:** tests unitarios y generación/lectura de un MP4 real con FFmpeg.
2. **Remotion smoke:** instala Remotion, renderiza un MP4 real de 1 segundo y lo valida con ffprobe.
3. **OpenAI model smoke:** si existe el secret OPENAI_API_KEY, realiza una llamada real al modelo configurado.

## Estado
La implementación funcional está preparada para ejecución end-to-end. Las únicas capacidades que requieren credenciales/recursos externos son la llamada al modelo OpenAI, el Trend Scout en vivo y la voz Piper con un modelo de voz instalado. La publicación automática está deliberadamente bloqueada para conservar la revisión humana.