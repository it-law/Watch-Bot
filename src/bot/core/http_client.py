"""Async HTTP client wrapper."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

import aiohttp


@dataclass
class HttpClient:
    """Wrapper for aiohttp ClientSession.

    Attributes:
        timeout_seconds: Total request timeout in seconds.
    """

    timeout_seconds: float = 30.0
    _session: Optional[aiohttp.ClientSession] = None

    async def start(self) -> None:
        """Initialize the underlying aiohttp session."""

        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout_seconds)
            self._session = aiohttp.ClientSession(timeout=timeout)

    async def close(self) -> None:
        """Close the underlying aiohttp session."""

        if self._session is not None:
            await self._session.close()

    async def get(self, url: str, **kwargs: Any) -> aiohttp.ClientResponse:
        """Perform an HTTP GET request.

        Args:
            url: Target URL.
            **kwargs: Additional aiohttp request parameters.

        Returns:
            aiohttp ClientResponse.
        """

        await self.start()
        assert self._session is not None
        return await self._session.get(url, **kwargs)
