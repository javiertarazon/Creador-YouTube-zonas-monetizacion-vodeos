import json
import shutil
import subprocess
from pathlib import Path


class VideoComposer:
    def __init__(self, remotion_dir: str = "remotion"):
        self.remotion_dir = Path(remotion_dir)

    def render(self, props: dict, output: str) -> dict:
        """Render the actual Remotion composition when Node dependencies exist."""
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if not shutil.which("npm"):
            raise RuntimeError("npm no está instalado.")

        props_file = output_path.parent / "render-props.json"
        props_file.write_text(json.dumps(props, ensure_ascii=False), encoding="utf-8")

        command = [
            "npx", "remotion", "render", "src/index.ts", "Video",
            str(output_path), "--props", str(props_file),
        ]
        completed = subprocess.run(
            command,
            cwd=self.remotion_dir,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                f"Remotion falló ({completed.returncode}): "
                f"{completed.stderr[-4000:]}"
            )
        return {
            "video": str(output_path),
            "renderer": "remotion",
            "command": command,
        }
