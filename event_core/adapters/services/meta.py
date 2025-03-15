import logging
from collections import abc, defaultdict
from enum import StrEnum
from typing import Dict, Iterator, cast

import redis

from ...config import get_redis_mapping_connection_params

logger = logging.getLogger(__name__)


class Meta(StrEnum):
    CHUNK_THUMB = "CHUNK-CHUNK_THUMB"
    DOC_THUMB = "DOC-DOC_THUMB"
    FILENAME = "DOC-FILENAME"
    PARENT = "CHUNK-DOC"
    FRAME_SECONDS = "ELEM-FRAME-SECONDS"
    PAGE = "ELEM-PAGE"
    COORDS = "ELEM-COORDS"


class AbstractNamespace(abc.MutableMapping):
    """
    ABC for namespaces within Meta Mappings.

    A `MetaMapping` is composed of multiple `AbstractNamespaces`.
    Each namespace implements the interface of a mutable mapping.
    """

    def __setitem__(self, key: str, value: str) -> None:
        raise NotImplementedError

    def __getitem__(self, key: str) -> str:
        raise NotImplementedError

    def __delitem__(self, key: str) -> None:
        raise NotImplementedError

    def __iter__(self) -> Iterator[str]:
        raise NotImplementedError


class AbstractMetaMapping(abc.Mapping):
    """
    ABC for interacting with the Meta Service, which essentially
    maintains mappings of objects to their respective meta
    information, categorized by namespaces. Specifically, each
    namespace represents a type of meta data.

    E.g:
        CHUNK-DOC: maps chunk keys to their parent doc key
        DOC-FILENAME: maps doc keys to their filenames

    Since the Meta Service is just a remote map, this class which
    defines the interface for accessing Meta Service, has to
    provide methods of a mapping of namespaces to mutable mappings.

    The top level MetaMapping instance is not mutable, but mappings
    within each namespace are mutable.
    """

    def __getitem__(self, meta: Meta) -> AbstractNamespace:
        """
        Retrieve the namespace corresponding to the given meta

        Args:
            meta (Meta):
                Meta that we want to get the namespace of

        Returns:
            AbstractNamespace:
                Namespace corresponding to specified meta
        """
        raise NotImplementedError

    def __iter__(self) -> Iterator[str]:
        """
        Iterate over existing namespaces, returning their names

        Returns:
            Iterator[str]: Iterator of namespace names
        """
        raise NotImplementedError


class RedisNamespace(AbstractNamespace):
    def __init__(self, r: redis.Redis, meta: Meta):
        self._r = r
        self._name = meta.value

    def __setitem__(self, key: str, value: str) -> None:
        self._r.hset(self._name, key, value)

    def __getitem__(self, key: str) -> str:
        if val := self._r.hget(self._name, key):
            return cast(str, val)
        raise KeyError(f"Key {key} does not exist")

    def __delitem__(self, key: str) -> None:
        self._r.hdel(self._name, key)

    def __iter__(self) -> Iterator[str]:
        for key, _ in self._r.hscan_iter(self._name):
            yield key

    def __len__(self) -> int:
        return cast(int, self._r.hlen(self._name))


class RedisMetaMapping(AbstractMetaMapping):
    def __init__(self):
        self._r = redis.Redis(**get_redis_mapping_connection_params())
        self._namespaces: Dict[Meta, RedisNamespace] = {}

    def __getitem__(self, meta: Meta) -> RedisNamespace:
        self._namespaces[meta] = self._namespaces.get(
            meta, RedisNamespace(self._r, meta)
        )
        return self._namespaces[meta]

    def __iter__(self) -> Iterator[str]:
        for meta in Meta:
            try:
                next(self._r.hscan_iter(meta.value))
                yield meta.value
            except StopIteration:
                pass

    def __len__(self) -> int:
        return len(list(self))


class FakeMetaMapping(AbstractMetaMapping):

    def __init__(self):
        self._namespaces: Dict[Meta, AbstractNamespace] = defaultdict(dict)

    def __getitem__(self, meta: Meta) -> AbstractNamespace:
        return self._namespaces[meta]

    def __iter__(self) -> Iterator[str]:
        for ns in self._namespaces:
            yield ns

    def __len__(self) -> int:
        return len(self._namespaces)
