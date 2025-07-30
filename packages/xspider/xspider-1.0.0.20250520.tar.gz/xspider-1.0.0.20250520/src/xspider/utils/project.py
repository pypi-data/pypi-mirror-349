from __future__ import annotations
import sys
import hashlib
from pathlib import Path

from xspider.exceptions import TransformTypeError
from xspider.type.types import Literal, Any, ModuleType, Generator, AsyncGenerator, TYPE_CHECKING
from xspider.type.validators import is_generator, is_async_generator

if TYPE_CHECKING:
    from xspider.core.configer import Configer


async def transform(result: Generator | AsyncGenerator):
    if is_generator(result):
        for i in result:
            yield i

    elif is_async_generator(result):
        async for i in result:
            yield i

    else:
        raise TransformTypeError("callback 返回值类型必须是 'generator' 或 'async_generator'！")


def _init_env() -> None:
    project_dir = str(Path(".").parent.resolve())
    if project_dir not in sys.path:
        sys.path.insert(0, project_dir)


def get_configer(config: str | ModuleType = "config") -> Configer:
    from xspider.core.configer import Configer

    configer = Configer()
    _init_env()
    configer.set_config(config)
    return configer


ALGO_TYPE = Literal[
    "md5", "sha1", "sha224", "sha256", "sha384", "sha512", "blake2b", "blake2s", "sha3_224", "sha3_256", "sha3_384",
    "sha3_512", "shake_128", "shake_256"
]


def gen_data_id(
        *args: Any,
        keys: list | None = None, item: dict | None = None,
        algo_type: ALGO_TYPE = "sha256"
) -> str:
    """
    >>> gen_data_id('123456')
    '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'

    :param args:
    :param keys:
    :param item:
    :param algo_type:
    :return:
    """
    m = hashlib.new(algo_type)
    if args:
        values = args
    elif keys is not None and item is not None:
        if isinstance(keys, list) and isinstance(item, dict):
            values = [item[k] for k in keys if k in item]
        else:
            raise ValueError(f"keys 必须是列表，item 必须是字典！")
    elif item is not None:
        values = [item[k] for k in sorted(item.keys())]
    else:
        raise ValueError(f"args 或 keys 和 item 或 item 必须提供之一！")

    data = list(map(lambda x: str(x), values))

    for i in data:
        m.update(i.encode())

    data_id = m.hexdigest()
    return data_id
