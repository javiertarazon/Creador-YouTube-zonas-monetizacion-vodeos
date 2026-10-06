import json
from pathlib import Path
from html import escape


class AssetManager:
    """Creates license-safe local assets and an auditable manifest.

    The first implementation intentionally generates original SVG title cards
    instead of downloading third-party images. This keeps the pipeline
    deterministic and avoids silently introducing incompatible licenses.
    """

    def build(self, title: str, topic: str, output_dir: str, count: int = 3) -> dict:
        root = Path(output_dir)
        root.mkdir(parents=True, exist_ok=True)
        assets = []

        for index in range(1, count + 1):
            path = root / f"card_{index:02d}.svg"
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">
  <rect width="1920" height="1080" fill="#111827"/>
  <rect x="90" y="90" width="1740" height="900" rx="42" fill="#1f2937"/>
  <text x="160" y="430" fill="#ffffff" font-family="Arial, sans-serif" font-size="88" font-weight="700">{escape(title)}</text>
  <text x="160" y="540" fill="#d1d5db" font-family="Arial, sans-serif" font-size="48">{escape(topic)}</text>
  <text x="160" y="850" fill="#9ca3af" font-family="Arial, sans-serif" font-size="32">Original asset · Creador YouTube</text>
</svg>"""
            path.write_text(svg, encoding="utf-8")
            assets.append({
                "path": str(path),
                "type": "svg",
                "license": "original",
                "source": "generated_by_pipeline",
            })

        manifest = root / "manifest.json"
        manifest.write_text(json.dumps(assets, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"assets": assets, "manifest": str(manifest)}
