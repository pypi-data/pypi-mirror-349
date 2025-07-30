from abc import ABCMeta
from pprint import pformat
from copy import deepcopy

from xspider.exceptions import ItemInitException, ItemGetattributeException
from xspider.type.types import Any, Final, MutableMapping, Self, Iterator, create_view_classes


class Field(object):
    pass


class ItemMeta(ABCMeta):
    def __new__(mcs, name: str, bases: tuple, attrs: dict[str, Any]) -> type:
        fields = {}
        new_attrs = {}

        for key, value in attrs.items():
            if isinstance(value, Field):
                fields[key] = value
            else:
                new_attrs[key] = value

        cls = super().__new__(mcs, name, bases, new_attrs)
        cls._FIELDS = fields
        return cls


ItemValidName = ["_FIELDS", "_item", "unassigned_keys"]

view_classes = create_view_classes("Item")


class Item(MutableMapping, metaclass=ItemMeta):
    _FIELDS: dict[str, Field]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._item: Final[dict[str, Any]] = dict()

        if args:
            raise ItemInitException(
                f"{self.__class__.__name__} 对象实例化。"
                f"不支持位置参数，请使用关键字参数传参！"
            )
        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __setitem__(self, key: str, value: Any) -> None:
        if key in self._FIELDS:
            self._item[key] = value
        else:
            raise KeyError(
                f"{self.__class__.__name__} 字段值赋值。"
                f"不支持该字段值 {key!r} 赋值，请先添加该字段到类定义中！"
            )

    def __getitem__(self, key: str) -> Any:
        return self._item[key]

    def __delitem__(self, key: str) -> None:
        del self._item[key]

    def __setattr__(self, name: str, value: Any) -> None:
        if name not in ItemValidName:
            raise AttributeError(
                f"{self.__class__.__name__} 属性值设置。"
                f"不支持该属性值 {name!r} 设置。如果是字段值赋值，请使用 item[{name!r}] = {value!r}！"
            )
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        fields = super().__getattribute__("_FIELDS")
        if name in fields:
            raise ItemGetattributeException(
                f"{self.__class__.__name__} 属性值获取。"
                f"不支持该属性值 {name} 获取。如果是字段值获取，请使用 item[{name!r}]！"
            )
        return super().__getattribute__(name)

    def __getattr__(self, name: str) -> None:
        if name not in ItemValidName:
            raise AttributeError(
                f"{self.__class__.__name__} 属性值获取。"
                f"不支持该属性值 {name} 获取。如果是字段值获取，请先添加该字段到类定义中，然后使用 item[{name!r}]！"
            )

    def __iter__(self) -> Iterator[str]:
        return iter(self._item)

    def __len__(self) -> int:
        return len(self._item)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} _item={pformat(self._item)}>"

    __str__ = __repr__

    def to_dict(self) -> dict[str, Any]:
        return dict(self)

    def copy(self) -> Self:
        return deepcopy(self)

    def items(self) -> view_classes.ItemsView:
        return view_classes.ItemsView(self)

    def keys(self) -> view_classes.KeysView:
        return view_classes.KeysView(self)

    def values(self) -> view_classes.ValuesView:
        return view_classes.ValuesView(self)

    @property
    def unassigned_keys(self) -> list[str]:
        return [k for k in self._FIELDS.keys() if k not in self._item.keys()]


__all__ = [
    "Field", "Item"
]
