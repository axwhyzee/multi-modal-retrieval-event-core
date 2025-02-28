import logging
from io import BytesIO
from urllib.parse import urljoin

import requests

from event_core.adapters.services.exceptions import (
    FailedToStore,
    ObjectNotExists,
)
from event_core.config import get_storage_service_api_url
from event_core.domain.types import ObjectType

logger = logging.getLogger(__name__)

API_URL = get_storage_service_api_url()


def add(data: bytes, key: str, obj_type: ObjectType) -> None:
    logger.info(f"Storing {key=} {obj_type}")
    url = urljoin(API_URL, "add")
    file = {"file": (key, BytesIO(data))}
    res = requests.post(
        url,
        data={"key": key, "obj_type": obj_type},
        files=file,
    )
    if res.status_code != 200:
        raise FailedToStore(f"Failed to store object {key}")


def get(key: str) -> bytes:
    logger.info(f"Fetching {key}")
    url = urljoin(API_URL, f'get/{key.strip("/")}')
    res = requests.get(url)
    if res.status_code == 400:
        raise ObjectNotExists(f"Object {key} does not exist")
    return res.content


def delete(key: str) -> None:
    logger.info(f"Deleting {key}")
    url = urljoin(API_URL, f'delete/{key.strip("/")}')
    res = requests.get(url)
    if res.status_code == 400:
        raise ObjectNotExists(f"Object {key} does not exist")
