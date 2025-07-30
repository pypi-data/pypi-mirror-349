from xspider.type.types import Literal, Any, Self, Callable


class Request(object):
    def __init__(
            self,
            url: str,
            /,
            *,
            callback: Callable[..., Any] | None = None,
            method: Literal["GET", "POST", "PUT", "DELETE"] = "GET",
            headers: dict[str, str] | None = None,
            body: bytes | str | None = None,
            cookies: dict[str, str] | None = None,
            priority: int = 0,
            proxy: dict[str, str] | None = None
    ):
        self.url = url
        self.callback = callback
        self.method = method
        self.headers = headers
        self.body = body
        self.cookies = cookies
        self.priority = priority
        self.proxy = proxy

    def __lt__(self, other: Self) -> bool:
        return self.priority < other.priority

    def __repr__(self) -> str:
        return f"<Request {self.method} {self.url}>"


__all__ = [
    "Request"
]
