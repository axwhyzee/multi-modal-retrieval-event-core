import logging
from io import BytesIO
from urllib.parse import urljoin

import requests

from event_core.adapters.repository.base import AbstractRepository
from event_core.adapters.repository.exceptions import (
    FailedToStore,
    ObjectNotExists,
)
from event_core.config import get_storage_service_api_url

logger = logging.getLogger(__name__)


class StorageClient(AbstractRepository):
    _API_URL = get_storage_service_api_url()

    def add(self, data: bytes, key: str) -> None:
        logger.info(f"Storing {key}")
        url = urljoin(self._API_URL, "add")
        res = requests.post(
            url,
            data={"key": key},
            files={"file": (key, BytesIO(data))},
        )
        if res.status_code != 200:
            raise FailedToStore(f"Failed to store object {key}")

    def get(self, key: str) -> bytes:
        logger.info(f"Fetching {key}")
        url = urljoin(self._API_URL, f'get/{key.strip("/")}')
        res = requests.get(url)
        if res.status_code == 400:
            raise ObjectNotExists(f"Object {key} does not exist")
        return res.content

    def delete(self, key: str) -> None:
        logger.info(f"Deleting {key}")
        url = urljoin(self._API_URL, f'delete/{key.strip("/")}')
        res = requests.get(url)
        if res.status_code == 400:
            raise ObjectNotExists(f"Object {key} does not exist")
