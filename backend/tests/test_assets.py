import json

from app.modules.assets import AssetManager


def test_assets_are_generated_and_manifest_is_auditable(tmp_path):
    result = AssetManager().build("Título", "Tema", str(tmp_path), count=2)

    assert len(result["assets"]) == 2
    for asset in result["assets"]:
        assert asset["license"] == "original"
        assert asset["source"] == "generated_by_pipeline"

    manifest = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    assert len(manifest) == 2
