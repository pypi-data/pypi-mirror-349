from __future__ import annotations
from abc import ABC, abstractmethod

from xspider.type.types import Any, Self, TYPE_CHECKING

if TYPE_CHECKING:
    from xspider.core.crawler import Crawler


class Component(ABC):
    @abstractmethod
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(Component, self).__init__(*args, **kwargs)

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def open(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @classmethod
    @abstractmethod
    def create_instance(cls, crawler: Crawler) -> Self:
        return cls()

    def idle(self) -> bool:
        return len(self) == 0
