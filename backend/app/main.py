from fastapi import FastAPI
from app.schemas import PipelineRequest, PipelineResponse
from app.modules.pipeline import FactoryPipeline

app = FastAPI(title="Creador YouTube", version="0.1.0")
pipeline = FactoryPipeline()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/pipeline/run", response_model=PipelineResponse)
async def run_pipeline(request: PipelineRequest):
    return await pipeline.run(
        topic=request.topic,
        language=request.language,
        market=request.market,
        duration_seconds=request.duration_seconds,
        publish=request.publish,
    )
