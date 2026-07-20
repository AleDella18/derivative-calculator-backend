import matplotlib.pyplot as plt
import pytest

from app.services import graphic_generator as graph_module


@pytest.mark.asyncio
async def test_graph_is_generated_in_memory_and_figure_is_closed(monkeypatch, tmp_path):
    captured = {}

    async def fake_upload(data, filename):
        captured.update(data=data, filename=filename)
        return "https://store.public.blob.vercel-storage.com/graphs/id.png"

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(graph_module, "upload_png", fake_upload)
    figures_before = set(plt.get_fignums())

    result = await graph_module.graphic_generator("2*x", "x")

    assert result.startswith("https://")
    assert captured["data"].startswith(b"\x89PNG\r\n\x1a\n")
    assert captured["filename"].startswith("graphs/")
    assert captured["filename"].endswith(".png")
    assert not (tmp_path / "imgs").exists()
    assert set(plt.get_fignums()) == figures_before


@pytest.mark.asyncio
async def test_figure_is_closed_when_upload_fails(monkeypatch):
    async def failed_upload(data, filename):
        raise RuntimeError("upload failed")

    monkeypatch.setattr(graph_module, "upload_png", failed_upload)
    figures_before = set(plt.get_fignums())

    with pytest.raises(RuntimeError, match="upload failed"):
        await graph_module.graphic_generator("2*x", "x")

    assert set(plt.get_fignums()) == figures_before
