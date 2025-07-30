from __future__ import annotations

from xspider.utils.spider_priority_queue import SpiderPriorityQueue
from xspider.http.request import Request
from xspider.core.component import Component

from xspider.type.types import Any, Self, TYPE_CHECKING

if TYPE_CHECKING:
    from xspider.core.crawler import Crawler


class Scheduler(Component):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self._schedules: SpiderPriorityQueue | None = None

    def __len__(self) -> int:
        return self._schedules.qsize()

    def open(self) -> None:
        self._schedules = SpiderPriorityQueue()

    def close(self) -> None:
        self._schedules = None

    @classmethod
    def create_instance(cls, crawler: Crawler) -> Self:
        return cls()

    async def enqueue_request(self, request: Request) -> None:
        await self._schedules.put(request)

    async def dequeue_request(self) -> Request:
        return await self._schedules.get()
