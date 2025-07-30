from __future__ import annotations
from asyncio import Queue

from xspider.core.component import Component
from xspider.item import Item
from xspider.http.request import Request
from xspider.type.types import Any, Self, TYPE_CHECKING

if TYPE_CHECKING:
    from xspider.core.crawler import Crawler


class Processor(Component):
    def __init__(self, crawler: Crawler, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.crawler = crawler

        self.queue: Queue | None = None

    def __len__(self) -> int:
        return self.queue.qsize()

    def open(self) -> None:
        self.queue = Queue()

    def close(self) -> None:
        self.queue = None

    @classmethod
    def create_instance(cls, crawler: Crawler) -> Self:
        return cls(crawler=crawler)

    async def process(self, output):
        await self.queue.put(output)
        await self._process()

    async def _process(self):
        while not self.idle():
            result = await self.queue.get()
            if isinstance(result, Request):
                await self._process_request(result)
            else:
                assert isinstance(result, Item)
                await self._process_item(result)

    async def _process_request(self, request: Request) -> None:
        await self.crawler.engine.enqueue_request(request)

    async def _process_item(self, item: Item) -> None:
        print(item)
