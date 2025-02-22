import logging
from abc import ABC, abstractmethod
from typing import TypeAlias, Union

import redis

from event_core.adapters.services.exceptions import KeyNotExists
from event_core.config import get_redis_mapping_connection_params

logger = logging.getLogger(__name__)

Value: TypeAlias = Union[str, int, float]


class AbstractMapper(ABC):
    @abstractmethod
    def set(self, key: str, val: Value) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, key: str) -> Value:
        raise NotImplementedError


class RedisMapper(AbstractMapper):
    def __init__(self):
        self._r = redis.Redis(**get_redis_mapping_connection_params())

    def set(self, key: str, val: Value) -> None:
        self._r.set(name=key, value=val)

    def get(self, key: str) -> Value:
        if (v := self._r.get(name=key)) is None:
            raise KeyNotExists(f"Key {key} does not exist")
        return v
