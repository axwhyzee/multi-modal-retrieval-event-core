import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, data: bytes, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, key: str) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str) -> None:
        raise NotImplementedError
