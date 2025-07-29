from xspider.utils.spider_priority_queue import SpiderPriorityQueue
from xspider.http.request import Request


class Scheduler(object):
    def __init__(self) -> None:
        self._schedules: SpiderPriorityQueue | None = None

    def __len__(self) -> int:
        return self._schedules.qsize()

    def idle(self) -> bool:
        return len(self) == 0

    def open(self) -> None:
        self._schedules = SpiderPriorityQueue()

    async def enqueue_request(self, request: Request) -> None:
        await self._schedules.put(request)

    async def dequeue_request(self) -> Request:
        return await self._schedules.get()
