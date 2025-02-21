from typing import Dict, Iterator

import pytest

from event_core.adapters.repository.base import AbstractRepository
from event_core.adapters.repository.exceptions import ObjectNotExists


class FakeRepository(AbstractRepository):
    def __init__(self):
        self._docs: Dict[str, bytes] = {}

    def add(self, data: bytes, key: str) -> None:
        self._docs[key] = data

    def delete(self, key: str) -> None:
        if key not in self._docs:
            raise ObjectNotExists
        self._docs.pop(key)

    def get(self, key: str) -> bytes:
        if key not in self._docs:
            raise ObjectNotExists
        return self._docs[key]


@pytest.fixture
def fake_repo() -> AbstractRepository:
    return FakeRepository()


@pytest.fixture
def obj_key() -> str:
    return "user1/test.txt"


@pytest.fixture
def obj_data() -> bytes:
    return b"test content"
