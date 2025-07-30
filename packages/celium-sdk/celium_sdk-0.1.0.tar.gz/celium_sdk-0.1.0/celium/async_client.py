"""Async Client façade."""
from __future__ import annotations

from .config import Config
from .transport.httpx_async import HttpxAsyncTransport
from .auth.api_key import ApiKeyAuth
from .transport.base import Transport


class AsyncClient:
    """Async variant (uses httpx.AsyncClient under the hood)."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        transport: Transport | None = None,
    ):
        self._config = Config()
        if base_url:
            object.__setattr__(self._config, "base_url", base_url)
        if timeout:
            object.__setattr__(self._config, "timeout", timeout)
        if max_retries is not None:
            object.__setattr__(self._config, "max_retries", max_retries)

        self._transport = transport or HttpxAsyncTransport(
            base_url=self._config.base_url,
            default_headers={"User-Agent": self._config.user_agent},
            timeout=self._config.timeout,
            max_retries=self._config.max_retries,
        )
        self._auth = ApiKeyAuth(api_key or "")

        secured = self._transport_with_auth

    # ------------------------------------------------- #
    @property
    def _transport_with_auth(self) -> Transport:
        return self._auth.decorate(self._transport)

    # ---------------- context mgr ------------------- #
    async def __aenter__(self):  # async context
        return self

    async def __aexit__(self, *exc):
        await self._transport.aclose()
