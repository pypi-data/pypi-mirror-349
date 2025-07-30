from __future__ import annotations

from xspider.http.request import Request
from xspider.type.types import Generator, Self, TYPE_CHECKING
from xspider.type.validators import is_str, is_list_of

if TYPE_CHECKING:
    from xspider.core.crawler import Crawler


class Spider(object):
    start_url: str | None = None
    start_urls: list[str] | None = None

    def __init__(self) -> None:
        self.crawler: Crawler | None = None

    @classmethod
    def create_instance(cls, crawler: Crawler) -> Self:
        ins = cls()
        ins.crawler = crawler
        return ins

    def start_requests(self) -> Generator[Request, None, None]:
        if is_str(url := self.start_url):
            yield Request(url)
        if is_list_of(urls := self.start_urls, str):
            for url in urls:
                yield Request(url)

    def parse(self, response):
        raise NotImplementedError("必须实现 parse 方法！")


__all__ = [
    "Spider"
]
