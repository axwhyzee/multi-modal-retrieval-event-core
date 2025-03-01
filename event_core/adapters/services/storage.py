import logging
from collections import abc
from dataclasses import dataclass
from io import BytesIO
from typing import Dict, Iterator
from urllib.parse import urljoin

import requests

from ...config import get_storage_service_api_url
from ...domain.types import Modal, ObjectType
from .exceptions import FailedToStore

logger = logging.getLogger(__name__)


@dataclass
class Payload:
    """
    Payload to send over to Storage Service to add an object.

    `obj_type` allows Storage Service to publish the associated
    ObjectStored event.

    `modal` allows event handlers to handle the ObjectStored
    events accordingly.
    """

    data: bytes
    obj_type: ObjectType
    modal: Modal


class StorageClient(abc.MutableMapping):
    """
    ABC for interacting with Storage Service. The Storage Service
    acts like an object repository, where objects are stored as
    `<object key>: <object bytes>` key value pairs.

    This client interface implements that of a mutable mapping so
    that objects can be accessed in a more Pythonic manner.

    Currently, the Storage Service is accessible via REST APIs
    over HTTP, but in future gRPC could be considered as well
    for low latency file transfers. Nonetheless, such clients
    will still implement the same interface defined by this class.
    """

    def __setitem__(self, key: str, value: Payload) -> None:
        raise NotImplementedError

    def __getitem__(self, key: str) -> bytes:
        raise NotImplementedError

    def __delitem__(self, key: str) -> None:
        raise NotImplementedError

    def __iter__(self) -> Iterator[str]:
        raise NotImplementedError


class StorageAPIClient(StorageClient):
    def __init__(self):
        self._api_url = get_storage_service_api_url()

    def _build_endpoint(self, *parts: str) -> str:
        url = self._api_url
        for part in parts:
            part = part.strip("/")
            url = urljoin(url, part)
        return url

    def __setitem__(self, key: str, value: Payload) -> None:
        logger.info(f"Storing {key}: {value}")

        url = self._build_endpoint("add")
        res = requests.post(
            url,
            data={
                "key": key,
                "obj_type": value.obj_type,
                "modal": value.modal,
            },
            files={"file": (key, BytesIO(value.data))},
        )

        if res.status_code != 200:
            raise FailedToStore(f"Failed to store object {key}")

    def __getitem__(self, key: str) -> bytes:
        logger.info(f"Fetching {key}")

        url = self._build_endpoint("get", key)
        res = requests.get(url)
        if res.status_code == 400:
            raise KeyError(f"Object {key=} not found")
        return res.content

    def __delitem__(self, key: str) -> None:
        logger.info(f"Deleting {key}")
        url = self._build_endpoint("delete", key)
        res = requests.get(url)
        if res.status_code == 400:
            raise KeyError(f"Object {key=} not found")

    def __iter__(self) -> Iterator[str]:
        url = self._build_endpoint("list")
        res = requests.get(url)
        for key in res.json():
            yield key

    def __len__(self) -> int:
        url = self._build_endpoint("len")
        res = requests.get(url)
        return res.json()


class FakeStorageClient(StorageClient):

    def __init__(self):
        self._objects: Dict[str, Payload] = {}

    def __setitem__(self, key: str, value: Payload) -> None:
        self._objects[key] = value

    def __getitem__(self, key: str) -> bytes:
        return self._objects[key].data

    def __delitem__(self, key: str) -> None:
        self._objects.pop(key)

    def __iter__(self) -> Iterator[str]:
        for key in self._objects:
            yield key

    def __len__(self) -> int:
        return len(self._objects)
