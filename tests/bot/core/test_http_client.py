"""Tests for the HTTP client wrapper."""

from __future__ import annotations

import pytest

from bot.core.http_client import HttpClient


@pytest.mark.asyncio
async def test_http_client_start_close() -> None:
    """HTTP client can start and close a session."""

    client = HttpClient()
    await client.start()
    assert client._session is not None
    await client.close()
    assert client._session is not None
    assert client._session.closed
