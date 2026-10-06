import shutil
import subprocess
from pathlib import Path

class PiperVoice:
    def available(self) -> bool:
        return shutil.which("piper") is not None

    def synthesize(self, text: str, model: str, output: str) -> str:
        if not self.available():
            raise RuntimeError("Piper no está instalado en el entorno.")
        out = Path(output)
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["piper", "--model", model, "--output_file", str(out)], input=text.encode(), check=True)
        return str(out)
