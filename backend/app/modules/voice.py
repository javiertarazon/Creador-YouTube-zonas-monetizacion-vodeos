import shutil
import subprocess
from pathlib import Path

from app.config import settings


class PiperVoice:
    def available(self) -> bool:
        return shutil.which(settings.piper_command) is not None

    def synthesize(self, text: str, model: str | None = None, output: str = "output/voice.wav") -> str:
        selected_model = model or settings.piper_model
        if not self.available():
            raise RuntimeError("Piper no está instalado en el entorno.")
        if not selected_model:
            raise RuntimeError("PIPER_MODEL no está configurado.")

        out = Path(output)
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [settings.piper_command, "--model", selected_model, "--output_file", str(out)],
            input=text.encode("utf-8"),
            check=True,
            capture_output=True,
        )
        return str(out)
