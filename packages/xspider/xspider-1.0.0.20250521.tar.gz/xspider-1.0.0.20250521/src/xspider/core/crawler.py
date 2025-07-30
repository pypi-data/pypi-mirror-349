from xspider.spider import Spider
from xspider.type.types import Type
from xspider.core.configer import Configer
from xspider.core.engine import Engine


class Crawler(object):
    def __init__(self, spider_cls: Type[Spider], configer: Configer) -> None:
        self.spider_cls = spider_cls
        self.configer = configer

        self.spider: Spider | None = None
        self.engine: Engine | None = None

    async def crawl(self):
        self.spider = self._create_spider()
        self.engine = self._create_engine()
        await self.engine.start_spider(self.spider)

    def _create_spider(self) -> Spider:
        spider = self.spider_cls.create_instance(self)
        self._set_spider(spider)
        return spider

    def _create_engine(self) -> Engine:
        engine = Engine(self)
        return engine

    def _set_spider(self, spider):
        self.configer.update_config_by_spider(spider)
