from ujson import loads
from pprint import pformat
from copy import deepcopy
from importlib import import_module

from xspider.type.types import Final, Any, ModuleType, Iterator, MutableMapping, Self, create_view_classes
from xspider.type.validators import is_str
from xspider.core.configer import default_config
from xspider.exceptions import ConfigerGetBoolException
from xspider.spider import Spider

view_classes = create_view_classes("Configer")


class Configer(MutableMapping):

    def __init__(self, config: dict[str:Any] | None = None) -> None:
        self._config: Final[dict[str, Any]] = dict()

        self.set_config(default_config)
        self.update_config(config)

    def __contains__(self, key: str) -> bool:
        return key in self._config

    def __setitem__(self, key: str, value: Any) -> None:
        self._config[key] = value

    def __getitem__(self, key: str) -> Any | None:
        if key in self:
            return self._config[key]

    def __delitem__(self, key: str) -> None:
        del self._config[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._config)

    def __len__(self) -> int:
        return len(self._config)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} _config={pformat(self._config)}>"

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

    def set(self, key: str, value: Any) -> None:
        self[key] = value

    def get(self, key: str, default: Any | None = None) -> Any | None:
        return self[key] if key in self else default

    def get_str(self, key: str, default: str = "") -> str:
        return str(self.get(key, default))

    def get_int(self, key: str, default: int = 0) -> int:
        return int(self.get(key, default))

    def get_float(self, key: str, default: float = 0.0) -> float:
        return float(self.get(key, default))

    def get_bool(self, key: str, default: bool = False) -> bool:
        value = self.get(key, default)
        try:
            return bool(int(value))
        except ValueError:
            if value in ("True", "true", "TRUE"):
                return True
            if value in ("False", "false", "FALSE"):
                return False
            raise ConfigerGetBoolException(
                f"布尔类型配置的合法取值应为：0 或 1，True 或 False，'0' 或 '1'，'True' 或 'False'，'true' 或 'false'，"
                f"'TRUE' 或 'FALSE'！"
            )

    def get_list(self, key: str, default: list[Any] | None = None) -> list[Any]:
        value = self.get(key, default if default is not None else [])
        if isinstance(value, str):
            value = value.split(",")
        return list(value)

    def get_dict(self, key: str, default: dict[Any, Any] = None) -> dict[Any, Any]:
        value = self.get(key, default if default is not None else {})
        if isinstance(value, str):
            value = loads(value)
        return dict(value)

    def delete(self, key: str) -> None:
        del self[key]

    def set_config(self, module: str | ModuleType) -> None:
        if isinstance(module, str):
            module = import_module(module)
        for key in dir(module):
            if is_str(key) and key.isupper():
                value = getattr(module, key)
                self.set(key, value)

    def update_config(self, config: dict[str, Any] | None = None) -> None:
        if config is not None:
            for key, value in config.items():
                self.set(key, value)

    def update_config_by_spider(self, spider: Spider) -> None:
        if hasattr(spider, "config"):
            config = getattr(spider, "config")
            self.update_config(config)


__all__ = [
    "Configer",
    "default_config"
]
