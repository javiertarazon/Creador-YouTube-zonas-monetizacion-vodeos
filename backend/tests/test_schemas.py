import pytest
from pydantic import ValidationError

from app.schemas import PipelineRequest


def test_pipeline_request_defaults():
    request = PipelineRequest(topic="Tecnología")

    assert request.language == "es"
    assert request.market == "US"
    assert request.duration_seconds == 60
    assert request.publish is False


@pytest.mark.parametrize(
    "duration",
    [14, 1801],
)
def test_pipeline_request_rejects_invalid_duration(duration):
    with pytest.raises(ValidationError):
        PipelineRequest(topic="Tecnología", duration_seconds=duration)


def test_pipeline_request_rejects_empty_topic():
    with pytest.raises(ValidationError):
        PipelineRequest(topic="")
