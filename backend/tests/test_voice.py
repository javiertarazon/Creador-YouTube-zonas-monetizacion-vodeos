import pytest

from app.modules.voice import PiperVoice


def test_piper_reports_missing_model(monkeypatch):
    voice = PiperVoice()
    monkeypatch.setattr(voice, "available", lambda: True)
    with pytest.raises(RuntimeError, match="PIPER_MODEL"):
        voice.synthesize("hola", model="", output="/tmp/test.wav")
