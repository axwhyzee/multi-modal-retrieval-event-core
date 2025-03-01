import json
import logging
from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import Callable, List, Type

import redis

from ..config import get_redis_pubsub_connection_params
from ..domain.events import CHANNELS, EVENTS, Event

logger = logging.getLogger(__name__)


class AbstractPublisher(ABC):
    @abstractmethod
    def publish(self, event: Event) -> None:
        raise NotImplementedError

    def __exit__(self, *_): ...

    def __enter__(self):
        return self


class AbstractConsumer(ABC):
    @abstractmethod
    def listen(self, callback: Callable[[Event], None]) -> None:
        raise NotImplementedError

    @abstractmethod
    def subscribe(self, event: Type[Event]) -> None:
        raise NotImplementedError

    def __exit__(self, *_): ...

    def __enter__(self):
        return self


class RedisConsumer(AbstractConsumer):
    def __init__(self):
        self._r = redis.Redis(**get_redis_pubsub_connection_params())
        self._consumer = self._r.pubsub(ignore_subscribe_messages=True)

    def listen(self, callback: Callable[[Event], None]) -> None:
        for message in self._consumer.listen():
            data = json.loads(message["data"])
            event_cls = EVENTS[message["channel"]]
            event = event_cls(**data)
            logger.info(f"Received: {event}")
            callback(event)

    def subscribe(self, event: Type[Event]) -> None:
        channel = CHANNELS[event]
        self._consumer.subscribe(channel)

    def __exit__(self, *_):
        self._r.close()
        self._consumer.close()


class RedisPublisher(AbstractPublisher):
    def __init__(self):
        self._r = redis.Redis(**get_redis_pubsub_connection_params())

    def publish(self, event: Event) -> None:
        channel = CHANNELS[event.__class__]
        event_json = json.dumps(asdict(event))
        logger.info(f"Publishing {event_json} to channel {channel}")
        self._r.publish(channel, event_json)

    def __exit__(self, *_):
        self._r.close()


class FakePublisher(AbstractPublisher):
    def __init__(self):
        self._published: List[Event] = []

    def publish(self, event: Event) -> None:
        self._published.append(event)
