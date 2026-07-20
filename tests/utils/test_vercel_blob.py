import httpx
import pytest

from app.utils import vercel_blob


class FakeAsyncClient:
    response = None
    captured = None

    def __init__(self, *, timeout):
        self.timeout = timeout

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return None

    async def put(self, url, *, content, headers):
        type(self).captured = (url, content, headers, self.timeout)
        return type(self).response


@pytest.mark.asyncio
async def test_upload_png_returns_public_url(monkeypatch):
    public_url = "https://store.public.blob.vercel-storage.com/graphs/id.png"
    request = httpx.Request("PUT", "https://blob.vercel-storage.com/graphs/id.png")
    FakeAsyncClient.response = httpx.Response(
        200, json={"url": public_url}, request=request
    )
    monkeypatch.setenv("BLOB_READ_WRITE_TOKEN", "secret-token")
    monkeypatch.setattr(vercel_blob.httpx, "AsyncClient", FakeAsyncClient)

    result = await vercel_blob.upload_png(b"png bytes", "graphs/id.png")

    assert result == public_url
    url, content, headers, timeout = FakeAsyncClient.captured
    assert url.endswith("/graphs/id.png")
    assert content == b"png bytes"
    assert headers["Content-Type"] == "image/png"
    assert headers["Authorization"] == "Bearer secret-token"
    assert timeout == vercel_blob.BLOB_TIMEOUT


def test_missing_blob_token_has_clear_safe_error(monkeypatch):
    monkeypatch.delenv("BLOB_READ_WRITE_TOKEN", raising=False)

    with pytest.raises(
        vercel_blob.VercelBlobError,
        match="BLOB_READ_WRITE_TOKEN is required",
    ):
        vercel_blob.get_blob_token()


@pytest.mark.asyncio
async def test_failed_http_response_raises_domain_error(monkeypatch):
    request = httpx.Request("PUT", "https://blob.vercel-storage.com/graphs/id.png")
    FakeAsyncClient.response = httpx.Response(503, request=request)
    monkeypatch.setenv("BLOB_READ_WRITE_TOKEN", "secret-token")
    monkeypatch.setattr(vercel_blob.httpx, "AsyncClient", FakeAsyncClient)

    with pytest.raises(vercel_blob.VercelBlobError, match="status 503"):
        await vercel_blob.upload_png(b"png bytes", "graphs/id.png")


@pytest.mark.asyncio
@pytest.mark.parametrize("payload", [{}, {"url": "not-a-url"}, []])
async def test_malformed_response_raises_domain_error(monkeypatch, payload):
    request = httpx.Request("PUT", "https://blob.vercel-storage.com/graphs/id.png")
    FakeAsyncClient.response = httpx.Response(200, json=payload, request=request)
    monkeypatch.setenv("BLOB_READ_WRITE_TOKEN", "secret-token")
    monkeypatch.setattr(vercel_blob.httpx, "AsyncClient", FakeAsyncClient)

    with pytest.raises(vercel_blob.VercelBlobError):
        await vercel_blob.upload_png(b"png bytes", "graphs/id.png")
