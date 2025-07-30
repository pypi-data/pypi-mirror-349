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
    NamedTuple,
    TypeAlias, Never, NoReturn
)
from collections.abc import (
    Iterator, Callable, Generator, AsyncGenerator, AsyncIterable, AsyncIterator, Coroutine, MutableMapping,
    ItemsView, KeysView, ValuesView
)

from xspider.utils.string import camel_to_snake


class ViewClasses(NamedTuple):
    ItemsView: type
    KeysView: type
    ValuesView: type


def create_view_classes(class_name: str) -> ViewClasses:
    def make_view_class(base_class) -> type:
        name = f"{class_name}{base_class.__name__}"

        def __repr__(self) -> str:
            return f"{camel_to_snake(name)}({list(self)})"

        return type(name, (base_class,), {"__repr__": __repr__})

    return ViewClasses(
        ItemsView=make_view_class(ItemsView),
        KeysView=make_view_class(KeysView),
        ValuesView=make_view_class(ValuesView),
    )


__all__ = [
    "ModuleType",

    "Task", "Future",

    "Literal", "Final", "Any", "Self", "TypeVar", "TypeGuard", "TYPE_CHECKING", "Type",

    "Iterator", "Callable", "Generator", "AsyncGenerator", "Coroutine", "MutableMapping", "create_view_classes",
]
