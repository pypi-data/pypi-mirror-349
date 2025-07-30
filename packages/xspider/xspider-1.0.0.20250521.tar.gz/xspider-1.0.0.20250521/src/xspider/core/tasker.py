from __future__ import annotations
from asyncio import create_task, Semaphore

from xspider.core.component import Component
from xspider.type.types import Final, Task, Future, Coroutine, Any, Self, TYPE_CHECKING

if TYPE_CHECKING:
    from xspider.core.crawler import Crawler


class Tasker(Component):

    def __init__(self, concurrency: int = 8, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self._concurrency: Final[int] = concurrency

        self._tasks: set[Task] | None = None
        self._semaphore: Semaphore | None = None

    def __len__(self) -> int:
        return len(self._tasks)

    def open(self) -> None:
        self._tasks = set()
        self._semaphore = Semaphore(self._concurrency)

    def close(self) -> None:
        self._tasks = None
        self._semaphore = None

    @classmethod
    def create_instance(cls, crawler: Crawler) -> Self:
        concurrency = crawler.configer.get_int("CONCURRENCY")
        return cls(concurrency=concurrency)

    async def create_task(self, coro: Coroutine) -> Task:
        task = create_task(coro)
        self._tasks.add(task)
        await self._semaphore.acquire()

        def done_callback(_fut: Future) -> None:
            self._tasks.remove(task)
            self._semaphore.release()

        task.add_done_callback(done_callback)
        return task
