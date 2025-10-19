import asyncio
from collections.abc import Iterable

import httpx


class Broadcast:
    """
    Send the same HTTP request concurrently to multiple peers using httpx.AsyncClient.

    Example
    -------
        async with Broadcast(peers) as client:
            responses = await client.get("/update")
            for peer, resp in responses:
                if isinstance(resp, Exception):
                    # handle error
                else:
                    # resp is httpx.Response
    """

    def __init__(self, peers: Iterable[str | httpx.URL], client_kwargs: dict[str, object] | None = None) -> None:
        self.peers: list[str | httpx.URL] = list(peers)
        self._client_kwargs = client_kwargs or {}
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "Broadcast":
        self._client = httpx.AsyncClient(**self._client_kwargs)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    def _build_url(self, peer: str, path: str) -> str:
        """
        Join peer and path in a sensible way. If path is an absolute URL (starts
        with http:// or https://) it is returned as-is.
        """
        path_str = str(path)
        if path_str.startswith("http://") or path_str.startswith("https://"):
            return path_str

        if peer.endswith("/") and path_str.startswith("/"):
            return peer[:-1] + path_str
        if not peer.endswith("/") and not path_str.startswith("/"):
            return peer + "/" + path_str
        return peer + path_str

    async def request(self, method: str, url: str, **kwargs) -> list[tuple[str, httpx.Response | Exception]]:
        """
        Send the given HTTP method to all peers concurrently.

        Returns a list of (peer, result) in the same order as the peers provided.
        Each result is either an httpx.Response or an Exception (if that request failed).
        """
        if self._client is None:
            raise RuntimeError("Broadcast must be used as an async context manager (async with Broadcast(...))")

        loop = asyncio.get_event_loop()
        tasks = []
        urls = []
        for peer in self.peers:
            full_url = self._build_url(peer, url)
            urls.append(full_url)
            # schedule the request; exceptions will be captured by gather
            tasks.append(loop.create_task(self._client.request(method, full_url, **kwargs)))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        return list(zip(self.peers, results))

    # Convenience methods for common HTTP verbs
    async def get(self, url: str, **kwargs) -> list[tuple[str, httpx.Response | Exception]]:
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs) -> list[tuple[str, httpx.Response | Exception]]:
        return await self.request("POST", url, **kwargs)

    async def put(self, url: str, **kwargs) -> list[tuple[str, httpx.Response | Exception]]:
        return await self.request("PUT", url, **kwargs)

    async def delete(self, url: str, **kwargs) -> list[tuple[str, httpx.Response | Exception]]:
        return await self.request("DELETE", url, **kwargs)

    async def patch(self, url: str, **kwargs) -> list[tuple[str, httpx.Response | Exception]]:
        return await self.request("PATCH", url, **kwargs)

    async def head(self, url: str, **kwargs) -> list[tuple[str, httpx.Response | Exception]]:
        return await self.request("HEAD", url, **kwargs)

    async def options(self, url: str, **kwargs) -> list[tuple[str, httpx.Response | Exception]]:
        return await self.request("OPTIONS", url, **kwargs)

    def __repr__(self) -> str:
        return f"<Broadcast peers={len(self.peers)}>"