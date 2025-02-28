import logging
from abc import ABC, abstractmethod
from io import BytesIO
from typing import Dict
from urllib.parse import urljoin

import requests

from event_core.adapters.services.exceptions import (
    FailedToStore,
    ObjectNotExists,
)
from event_core.config import get_storage_service_api_url
from event_core.domain.types import Modal, ObjectType

logger = logging.getLogger(__name__)


class StorageClient(ABC):

    @abstractmethod
    def add(
        self, data: bytes, key: str, obj_type: ObjectType, modal: Modal
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, key: str) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str) -> None:
        raise NotImplementedError


class StorageAPIClient(StorageClient):
    def __init__(self):
        self._api_url = get_storage_service_api_url()

    def add(
        self, data: bytes, key: str, obj_type: ObjectType, modal: Modal
    ) -> None:
        logger.info(f"Storing {key=} {obj_type=} {modal=}")
        url = urljoin(self._api_url, "add")
        file = {"file": (key, BytesIO(data))}
        res = requests.post(
            url,
            data={"key": key, "obj_type": obj_type, "modal": modal},
            files=file,
        )
        if res.status_code != 200:
            raise FailedToStore(f"Failed to store object {key}")

    def get(self, key: str) -> bytes:
        logger.info(f"Fetching {key}")
        url = urljoin(self._api_url, f'get/{key.strip("/")}')
        res = requests.get(url)
        if res.status_code == 400:
            raise ObjectNotExists(f"Object {key} does not exist")
        return res.content

    def delete(self, key: str) -> None:
        logger.info(f"Deleting {key}")
        url = urljoin(self._api_url, f'delete/{key.strip("/")}')
        res = requests.get(url)
        if res.status_code == 400:
            raise ObjectNotExists(f"Object {key} does not exist")


class FakeStorageClient(StorageClient):

    def __init__(self):
        self._objects: Dict[str, bytes] = {}

    def add(
        self, data: bytes, key: str, obj_type: ObjectType, modal: Modal
    ) -> None:
        self._objects[key] = data

    def get(self, key: str) -> bytes:
        return self._objects[key]

    def delete(self, key: str) -> None:
        self._objects.pop(key)
