import logging
from abc import ABC, abstractmethod
from typing import TypeAlias, Union

import redis

from event_core.adapters.services.exceptions import KeyNotExists
from event_core.config import get_redis_mapping_connection_params
from event_core.domain.types import ObjectType

logger = logging.getLogger(__name__)

ValueT: TypeAlias = Union[str, int, float]


def _namespace_from_obj_types(from_type: ObjectType, to_type: ObjectType) -> str:
    return f'{from_type}__{to_type}'


class AbstractMapper(ABC):
    @abstractmethod
    def set(self, from_type: ObjectType, to_type: ObjectType, str, val: ValueT) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, from_type: ObjectType, to_type: ObjectType, key: str) -> ValueT:
        raise NotImplementedError

    @abstractmethod
    def delete(self, from_type: ObjectType, to_type: ObjectType, key: str) -> None:
        raise NotImplementedError


class RedisMapper(AbstractMapper):
    def __init__(self):
        self._r = redis.Redis(**get_redis_mapping_connection_params())

    def set(self, from_type: ObjectType, to_type: ObjectType, key: str, val: ValueT) -> None:
        namespace = _namespace_from_obj_types(from_type, to_type)
        self._r.hset(name=namespace, key=key, value=val)

    def get(self, from_type: ObjectType, to_type: ObjectType, key: str) -> ValueT:
        namespace = _namespace_from_obj_types(from_type, to_type)
        if (v := self._r.hget(name=namespace, key=key)) is None:
            raise KeyNotExists(f"Key {key} does not exist")
        return v

    def delete(self, from_type: ObjectType, to_type: ObjectType, key: str) -> None:
        namespace = _namespace_from_obj_types(from_type, to_type)
        self._r.hdel(name=namespace, key=key)
