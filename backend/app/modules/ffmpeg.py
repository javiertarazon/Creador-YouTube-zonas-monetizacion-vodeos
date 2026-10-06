import shutil
import subprocess
from pathlib import Path


class FFmpegTools:
    def available(self) -> bool:
        return shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None

    def mux_audio(self, video: str, audio: str, output: str) -> str:
        if not self.available():
            raise RuntimeError("ffmpeg/ffprobe no están instalados.")
        out = Path(output)
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([
            "ffmpeg", "-y", "-i", video, "-i", audio,
            "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
            "-c:a", "aac", "-shortest", str(out)
        ], check=True, capture_output=True, text=True)
        return str(out)

    def normalize_lufs(self, input_path: str, output_path: str, target_lufs: int = -14) -> str:
        if not self.available():
            raise RuntimeError("ffmpeg/ffprobe no están instalados.")
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([
            "ffmpeg", "-y", "-i", input_path,
            "-af", f"loudnorm=I={target_lufs}:TP=-1.5:LRA=11",
            "-c:v", "copy", "-c:a", "aac", str(out)
        ], check=True, capture_output=True, text=True)
        return str(out)
