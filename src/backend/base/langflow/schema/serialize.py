from collections.abc import AsyncIterator, Generator, Iterator
from datetime import datetime

from loguru import logger
from pydantic import BaseModel
from pydantic.v1 import BaseModel as BaseModelV1


def recursive_serialize_or_str(obj):
    try:
        if isinstance(obj, str):
            return obj
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, dict):
            return {k: recursive_serialize_or_str(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [recursive_serialize_or_str(v) for v in obj]
        if isinstance(obj, BaseModel | BaseModelV1):
            if hasattr(obj, "model_dump"):
                obj_dict = obj.model_dump()
            elif hasattr(obj, "dict"):
                obj_dict = obj.dict()
            return {k: recursive_serialize_or_str(v) for k, v in obj_dict.items()}

        if isinstance(obj, AsyncIterator | Generator | Iterator):
            # contain memory addresses
            # without consuming the iterator
            # return list(obj) consumes the iterator
            # return f"{obj}" this generates '<generator object BaseChatModel.stream at 0x33e9ec770>'
            # it is not useful
            return "Unconsumed Stream"
        if hasattr(obj, "dict"):
            return {k: recursive_serialize_or_str(v) for k, v in obj.dict().items()}
        if hasattr(obj, "model_dump"):
            return {k: recursive_serialize_or_str(v) for k, v in obj.model_dump().items()}
        if isinstance(obj, type) and issubclass(obj, BaseModel):
            # This a type BaseModel and not an instance of it
            return repr(obj)
        return str(obj)
    except Exception:  # noqa: BLE001
        logger.debug(f"Cannot serialize object {obj}")
        return str(obj)
