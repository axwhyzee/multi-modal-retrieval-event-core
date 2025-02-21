from abc import ABC, abstractmethod
from typing import Callable

from event_core.domain.events import Event


class AbstractPublisher(ABC):
    @abstractmethod
    def publish(self, event: Event) -> None:
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, *_):
        raise NotImplementedError

    def __enter__(self):
        return self


class AbstractConsumer(ABC):
    @abstractmethod
    def listen(self, callback: Callable[[Event], None]) -> None:
        raise NotImplementedError

    @abstractmethod
    def subscribe(self, event: Event) -> None:
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, *_): ...
