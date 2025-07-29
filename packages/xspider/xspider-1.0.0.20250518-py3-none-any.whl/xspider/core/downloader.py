import time
import random
import asyncio
import requests

from xspider.http.request import Request


class Downloader(object):
    def __init__(self) -> None:
        self._downloads: set[Request] | None = None

    def __len__(self) -> int:
        return len(self._downloads)

    def idle(self) -> bool:
        return len(self) == 0

    def open(self):
        self._downloads = set()

    async def download(self, request: Request):
        self._downloads.add(request)
        response = await self._download(request)
        self._downloads.remove(request)
        return response

    async def _download(self, request: Request):
        await asyncio.sleep(random.uniform(0, 1))
        return "<Response [200]>"
