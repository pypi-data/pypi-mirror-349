from asyncio import create_task, gather

from xspider.spider import Spider
from xspider.core.configer import Configer
from xspider.core.crawler import Crawler
from xspider.type.types import Type, Final, Task
from xspider.exceptions import SpiderClsTypeError


class CrawlerProcess(object):
    def __init__(self, configer: Configer | None = None) -> None:
        self.configer = configer
        self._crawlers: Final[set] = set()
        self._tasks: Final[set] = set()

    def crawl(self, spider_cls: Type[Spider]) -> None:
        crawler = self._create_crawler(spider_cls)
        self._crawlers.add(crawler)
        task = self._crawl(crawler)
        self._tasks.add(task)

    def _create_crawler(self, spider_cls: Type[Spider]) -> Crawler:
        if isinstance(spider_cls, str):
            raise SpiderClsTypeError(f"{self.__class__.__name__}.crawl 参数 spider_cls 不支持字符串类型！")
        crawler = Crawler(spider_cls, self.configer.copy())
        return crawler

    @staticmethod
    def _crawl(crawler: Crawler) -> Task:
        return create_task(crawler.crawl())

    async def start(self) -> None:
        await gather(*self._tasks)
