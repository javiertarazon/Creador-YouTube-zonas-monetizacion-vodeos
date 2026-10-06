from pydantic import BaseModel, Field

class PipelineRequest(BaseModel):
    topic: str = Field(min_length=2)
    language: str = "es"
    market: str = "US"
    duration_seconds: int = Field(default=60, ge=15, le=1800)
    publish: bool = False

class PipelineResponse(BaseModel):
    status: str
    human_review_required: bool
    auto_publish_enabled: bool
    stages: dict
