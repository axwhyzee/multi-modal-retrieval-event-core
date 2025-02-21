import pytest

from event_core.adapters.repository.base import AbstractRepository
from event_core.adapters.repository.exceptions import ObjectNotExists
from event_core.conftest import FakeRepository


def test_add_doc(
    fake_repo: FakeRepository, obj_key: str, obj_data: bytes
) -> None:
    fake_repo.add(obj_data, obj_key)
    assert fake_repo._docs[obj_key] == obj_data


def test_get_doc(
    fake_repo: FakeRepository, obj_key: str, obj_data: bytes
) -> None:
    fake_repo._docs[obj_key] = obj_data
    assert fake_repo.get(obj_key) == obj_data


def test_delete_doc(
    fake_repo: FakeRepository, obj_key: str, obj_data: bytes
) -> None:
    fake_repo._docs[obj_key] = obj_data
    fake_repo.delete(obj_key)
    with pytest.raises(ObjectNotExists) as e:
        fake_repo.get(obj_key)


def test_add_and_get_doc(
    fake_repo: AbstractRepository, obj_key: str, obj_data: bytes
) -> None:
    fake_repo.add(obj_data, obj_key)
    assert fake_repo.get(obj_key) == obj_data


def test_non_idempotent_delete(
    fake_repo: AbstractRepository, obj_key: str, obj_data: bytes
) -> None:
    fake_repo.add(obj_data, obj_key)
    fake_repo.delete(obj_key)
    with pytest.raises(ObjectNotExists) as e:
        fake_repo.delete(obj_key)


def test_idempotent_add(
    fake_repo: AbstractRepository, obj_key: str, obj_data: bytes
) -> None:
    fake_repo.add(obj_data, obj_key)
    fake_repo.add(obj_data, obj_key)
    assert fake_repo.get(obj_key) == obj_data
