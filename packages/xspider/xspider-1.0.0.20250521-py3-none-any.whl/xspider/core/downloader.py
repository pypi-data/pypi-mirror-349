from __future__ import annotations
import time
import random
import asyncio
import requests

from xspider.http.request import Request
from xspider.http.response import Response
from xspider.core.component import Component
from xspider.type.types import Any, Self, TYPE_CHECKING

if TYPE_CHECKING:
    from xspider.core.crawler import Crawler


class Downloader(Component):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self._downloads: set[Request] | None = None

    def __len__(self) -> int:
        return len(self._downloads)

    def open(self) -> None:
        self._downloads = set()

    def close(self) -> None:
        self._downloads = None

    @classmethod
    def create_instance(cls, crawler: Crawler) -> Self:
        return cls()

    async def download(self, request: Request) -> Response:
        self._downloads.add(request)
        response = await self._download(request)
        self._downloads.remove(request)
        return response

    async def _download(self, request: Request) -> Response:
        await asyncio.sleep(random.uniform(0, 1))
        return "<Response [200]>"
