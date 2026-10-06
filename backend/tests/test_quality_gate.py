import pytest
from app.modules.quality_gate import QualityGate

@pytest.mark.asyncio
async def test_quality_gate_passes_nonempty_script():
    result = await QualityGate().run({"script": "Guion de prueba"})
    assert result["passed"] is True
    assert result["score"] >= 8

