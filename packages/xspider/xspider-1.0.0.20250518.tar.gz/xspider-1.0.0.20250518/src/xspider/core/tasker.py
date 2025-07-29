from asyncio import create_task, Semaphore

from xspider.types import Task, Final, Future, Coroutine


class Tasker(object):
    def __init__(self, total_concurrency: int = 16) -> None:
        self._total_concurrency: Final[int] = total_concurrency

        self._tasks: set[Task] | None = None
        self._semaphore: Semaphore | None = None

    def __len__(self) -> int:
        return len(self._tasks)

    def idle(self) -> bool:
        return len(self) == 0

    def open(self):
        self._tasks = set()
        self._semaphore = Semaphore(self._total_concurrency)

    async def create_task(self, coro: Coroutine) -> Task:
        task = create_task(coro)
        self._tasks.add(task)
        await self._semaphore.acquire()

        def done_callback(_fut: Future):
            self._tasks.remove(task)
            self._semaphore.release()

        task.add_done_callback(done_callback)
        return task
