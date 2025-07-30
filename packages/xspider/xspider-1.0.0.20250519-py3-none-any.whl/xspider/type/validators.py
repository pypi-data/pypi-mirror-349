from inspect import isgenerator, isasyncgen, iscoroutine

from xspider.type.types import Any, TypeVar, TypeGuard


def is_int(obj: Any) -> TypeGuard[int]:
    return isinstance(obj, int) and not isinstance(obj, bool)


def is_str(val: Any) -> TypeGuard[str]:
    return isinstance(val, str)


def is_list(val: Any) -> TypeGuard[list[Any]]:
    return isinstance(val, list)


T = TypeVar("T")


def is_list_of(val: list[Any], type_: type[T]) -> TypeGuard[list[T]]:
    return isinstance(val, list) and all(isinstance(i, type_) for i in val)


is_generator = isgenerator
is_async_generator = isasyncgen
is_coroutine = iscoroutine

__all__ = [
    "is_str",
    "is_list_of",
    "is_generator", "is_async_generator", "is_coroutine"
]
