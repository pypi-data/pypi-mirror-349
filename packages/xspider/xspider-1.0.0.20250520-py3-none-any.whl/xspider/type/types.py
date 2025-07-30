from types import ModuleType
from asyncio import Task, Future
from typing import (
    Literal,
    Final,
    Any,
    Self,
    TypeVar,
    TypeGuard,
    TYPE_CHECKING,
    Type,
    TypeAlias, Never, NoReturn
)
from collections.abc import (
    Iterator, Callable, Generator, AsyncGenerator, AsyncIterable, AsyncIterator, Coroutine, MutableMapping,
    ItemsView, KeysView, ValuesView
)

from xspider.utils.string import camel_to_snake


class ConfigerItemsView(ItemsView):
    def __repr__(self) -> str:
        return f"{camel_to_snake(self.__class__.__name__)}({list(self)})"


class ConfigerKeysView(KeysView):
    def __repr__(self) -> str:
        return f"{camel_to_snake(self.__class__.__name__)}({list(self)})"


class ConfigerValuesView(ValuesView):
    def __repr__(self) -> str:
        return f"{camel_to_snake(self.__class__.__name__)}({list(self)})"


__all__ = [
    "ModuleType",

    "Task", "Future",

    "Literal", "Final", "Any", "Self", "TypeVar", "TypeGuard", "TYPE_CHECKING", "Type",

    "Iterator", "Callable", "Generator", "AsyncGenerator", "Coroutine", "MutableMapping", "ConfigerItemsView",
    "ConfigerKeysView", "ConfigerValuesView"
]
