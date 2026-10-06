import json
import shutil
import subprocess
from pathlib import Path


class VideoComposer:
    def __init__(self, remotion_dir: str = "remotion"):
        self.remotion_dir = Path(remotion_dir)

    def render(self, props: dict, output: str) -> dict:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if not shutil.which("npm"):
            raise RuntimeError("npm no está instalado.")
        if not (self.remotion_dir / "node_modules").exists():
            raise RuntimeError("Dependencias de Remotion no instaladas. Ejecuta npm install en remotion/.")

        public_dir = self.remotion_dir / "public" / "generated"
        public_dir.mkdir(parents=True, exist_ok=True)

        normalized = dict(props)
        public_assets = []
        for asset in props.get("assets", []):
            source = Path(asset["path"])
            if source.exists():
                destination = public_dir / source.name
                shutil.copy2(source, destination)
                public_assets.append({**asset, "public_name": f"generated/{source.name}"})
        normalized["assets"] = public_assets

        voice = props.get("voice_audio")
        if voice and Path(voice).exists():
            voice_destination = public_dir / "voice.wav"
            shutil.copy2(voice, voice_destination)
            normalized["voice_audio"] = "generated/voice.wav"
        else:
            normalized["voice_audio"] = None

        props_file = output_path.parent / "render-props.json"
        props_file.write_text(json.dumps(normalized, ensure_ascii=False), encoding="utf-8")

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
