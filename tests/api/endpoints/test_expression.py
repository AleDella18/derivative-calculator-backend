from types import SimpleNamespace

import pytest

from app.api.endpoints import expression
from app.schemas.expression import ExpressionRequest


class FakeRequest:
    def __init__(self):
        self.headers = {"cookie": "auth_token=test-token"}
        self.app = SimpleNamespace(state=SimpleNamespace(db=object()))


@pytest.mark.asyncio
async def test_new_derivative_stores_and_returns_complete_blob_url(monkeypatch):
    blob_url = "https://store.public.blob.vercel-storage.com/graphs/new.png"
    saved = []
    monkeypatch.setattr(expression, "jwt_decoder", lambda token: "user@example.com")
    monkeypatch.setattr(expression, "get_existing_derivative", lambda expr, db: None)
    monkeypatch.setattr(
        expression, "compute_derivative", lambda expr, var: (True, "2")
    )

    async def fake_graphic_generator(expr, var):
        return blob_url

    monkeypatch.setattr(expression, "graphic_generator", fake_graphic_generator)
    monkeypatch.setattr(
        expression,
        "save_derivative",
        lambda *args: saved.append(args),
    )

    request = FakeRequest()
    result = await expression.compute_expression(
        ExpressionRequest(expr="2*x", diff_var="x"), request
    )

    assert result == {"derivative": "2", "img_path": blob_url}
    assert saved[0][1:5] == ("2*x", "2", request.app.state.db, blob_url)


@pytest.mark.asyncio
async def test_cached_derivative_does_not_upload(monkeypatch):
    blob_url = "https://store.public.blob.vercel-storage.com/graphs/cached.png"
    monkeypatch.setattr(expression, "jwt_decoder", lambda token: "user@example.com")
    monkeypatch.setattr(expression, "get_existing_derivative", lambda expr, db: "2")
    monkeypatch.setattr(expression, "get_function_id", lambda expr, db: 1)
    monkeypatch.setattr(expression, "get_image_path", lambda function_id, db: blob_url)

    async def unexpected_upload(*args):
        pytest.fail("cached results must not generate or upload another graph")

    monkeypatch.setattr(expression, "graphic_generator", unexpected_upload)

    result = await expression.compute_expression(
        ExpressionRequest(expr="2*x", diff_var="x"), FakeRequest()
    )

    assert result == {"derivative": "2", "img_path": blob_url}


@pytest.mark.asyncio
async def test_upload_failure_does_not_insert_database_row(monkeypatch):
    saved = []
    monkeypatch.setattr(expression, "jwt_decoder", lambda token: "user@example.com")
    monkeypatch.setattr(expression, "get_existing_derivative", lambda expr, db: None)
    monkeypatch.setattr(
        expression, "compute_derivative", lambda expr, var: (True, "2")
    )

    async def failed_upload(*args):
        raise RuntimeError("upload unavailable")

    monkeypatch.setattr(expression, "graphic_generator", failed_upload)
    monkeypatch.setattr(expression, "save_derivative", lambda *args: saved.append(args))

    with pytest.raises(Exception) as exc_info:
        await expression.compute_expression(
            ExpressionRequest(expr="2*x", diff_var="x"), FakeRequest()
        )

    assert getattr(exc_info.value, "status_code", None) == 500
    assert saved == []
