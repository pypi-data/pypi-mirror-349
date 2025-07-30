from xspider.http.request import Request
from xspider.type.types import Generator
from xspider.type.validators import is_str, is_list_of


class Spider(object):
    start_url: str | None = None
    start_urls: list[str] | None = None

    def __init__(self) -> None:
        pass

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
