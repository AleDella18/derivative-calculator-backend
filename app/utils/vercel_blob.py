"""Asynchronous storage operations for Vercel Blob."""

import os
from typing import Final
from urllib.parse import quote, urlparse

import httpx


BLOB_API_URL: Final = "https://blob.vercel-storage.com"
BLOB_TIMEOUT: Final = httpx.Timeout(30.0, connect=10.0)


class VercelBlobError(RuntimeError):
    """Raised when a graph cannot be uploaded to Vercel Blob."""


def get_blob_token() -> str:
    """Return the configured Blob token, or raise a safe configuration error."""
    token = os.getenv("VERCEL_BLOB_READ_WRITE_TOKEN", "").strip()
    if not token:
        raise VercelBlobError("VERCEL_BLOB_READ_WRITE_TOKEN is required")
    return token


async def upload_png(data: bytes, filename: str) -> str:
    """Upload PNG bytes to a public Vercel Blob pathname.

    Args:
        data: Complete PNG file content.
        filename: Destination pathname within the Blob store.

    Returns:
        The complete public URL returned by Vercel Blob.

    Raises:
        VercelBlobError: If configuration is missing, the request fails, Vercel
            returns a non-success response, or its response has no valid URL.

    This function performs network I/O and never writes to the local filesystem.
    """
    if not data:
        raise VercelBlobError("Cannot upload an empty PNG")
    if not filename or filename.startswith("/") or ".." in filename.split("/"):
        raise VercelBlobError("A valid Blob pathname is required")

    token = get_blob_token()
    upload_url = f"{BLOB_API_URL}/{quote(filename, safe='/')}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "image/png",
        "x-content-type": "image/png",
        "x-api-version": "7",
        "x-add-random-suffix": "0",
    }

    try:
        async with httpx.AsyncClient(timeout=BLOB_TIMEOUT) as client:
            response = await client.put(upload_url, content=data, headers=headers)
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise VercelBlobError(
            f"Vercel Blob upload failed with status {exc.response.status_code}"
        ) from exc
    except httpx.HTTPError as exc:
        raise VercelBlobError("Vercel Blob upload request failed") from exc

    try:
        blob_url = response.json().get("url")
    except (ValueError, AttributeError) as exc:
        raise VercelBlobError("Vercel Blob returned a malformed response") from exc

    parsed_url = urlparse(blob_url) if isinstance(blob_url, str) else None
    if (
        not parsed_url
        or parsed_url.scheme != "https"
        or not parsed_url.hostname
        or not parsed_url.hostname.endswith(".public.blob.vercel-storage.com")
    ):
        raise VercelBlobError("Vercel Blob response did not contain a valid public URL")

    return blob_url
