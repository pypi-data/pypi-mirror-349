from __future__ import annotations
from asyncio import create_task

from xspider.item import Item
from xspider.spider import Spider
from xspider.http.request import Request
from xspider.core.scheduler import Scheduler
from xspider.core.downloader import Downloader
from xspider.core.tasker import Tasker
from xspider.utils.project import transform
from xspider.type.types import Iterator, Callable, TYPE_CHECKING
from xspider.type.validators import is_coroutine
from xspider.exceptions import OutputException

if TYPE_CHECKING:
    from xspider.core.crawler import Crawler


class Engine(object):
    def __init__(self, crawler: Crawler):
        self.crawler = crawler
        self.configer = self.crawler.configer
        self.scheduler: Scheduler | None = None
        self.downloader: Downloader | None = None
        self.tasker: Tasker | None = None

        self.spider: Spider | None = None
        self.start_requests: Iterator[str] | None = None
        self.running: bool = False

    async def start_spider(self, spider: Spider):
        self.scheduler = Scheduler()
        if hasattr(self.scheduler, "open"):
            self.scheduler.open()
        self.downloader = Downloader()
        if hasattr(self.downloader, "open"):
            self.downloader.open()
        self.tasker = Tasker(self.configer.get_int("CONCURRENCY"))
        if hasattr(self.tasker, "open"):
            self.tasker.open()

        self.spider = spider
        self.start_requests = iter(spider.start_requests())
        self.running = True

        await self._open_spider()

    async def _open_spider(self):
        crawling = create_task(self.crawl())
        await crawling

    async def crawl(self):
        while self.running:
            if (request := await self._get_dequeue_request()) is not None:
                await self._crawl(request)
            else:
                try:
                    start_request = next(self.start_requests)  # noqa
                except StopIteration:
                    self.start_requests = None
                except Exception as e:
                    if not await self._exit():
                        continue
                    self.running = False
                else:
                    await self.enqueue_request(start_request)

    async def enqueue_request(self, request):
        await self._schedule_request(request)

    async def _schedule_request(self, request):
        # todo: 处理去重
        await self.scheduler.enqueue_request(request)

    async def _get_dequeue_request(self):
        return await self.scheduler.dequeue_request()

    async def _crawl(self, request):
        async def crawl_task():
            outputs = await self._fetch(request)
            if outputs:
                await self._handle_spider_outputs(outputs)

        await self.tasker.create_task(crawl_task())

    async def _fetch(self, request: Request):
        async def success(response):
            callback: Callable = request.callback or self.spider.parse

            # type(callback(response))
            # <class 'generator'>
            # <class 'async_generator'>
            # <class 'NoneType'>

            if outputs := callback(response):
                if is_coroutine(outputs):
                    await outputs
                else:
                    return transform(outputs)

        resp = await self.downloader.download(request)
        outs = await success(resp)
        return outs

    async def _handle_spider_outputs(self, outputs):
        async for output in outputs:
            if isinstance(output, Request):
                await self.enqueue_request(output)
            elif isinstance(output, Item):
                pass
            else:
                raise OutputException(f"{type(self.spider)} 必须返回 'Request' 或 'Item'！")

    async def _exit(self):
        if self.scheduler.idle() and self.downloader.idle() and self.tasker.idle():
            return True
        return False
