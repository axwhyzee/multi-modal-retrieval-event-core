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
    """Defines the interface for event publishers"""

    @abstractmethod
    def publish(self, event: Event) -> None:
        """
        Publish an event to the message queue

        Args:
            event (Event): Event payload
        """
        raise NotImplementedError

    def __exit__(self, *_): ...

    def __enter__(self):
        return self


class AbstractConsumer(ABC):
    """
    Defines the interface for event consumers. Event consumers
    subscribe to 1 or more channels. A single callback is provided
    to handle events received on all channels
    """

    @abstractmethod
    def listen(self, callback: Callable[[Event], None]) -> None:
        """
        Listen to multiple message queues at once, using the same
        callback to handle all events
        
        Args:
            callback (Callable[[Event], None]): 
                Callback to handle events as they arrive
        """
        raise NotImplementedError

    @abstractmethod
    def subscribe(self, event: Type[Event]) -> None:
        """
        Subscribe to one or more message queues

        Args:
            event (Type[Event]): Class of event to subscribe to
        """
        raise NotImplementedError

    def __exit__(self, *_): ...

    def __enter__(self):
        return self


class RedisConsumer(AbstractConsumer):

    def __init__(self):
        self._r = redis.Redis(**get_redis_pubsub_connection_params())
        self._channels: List[str] = []

    def listen(self, callback: Callable[[Event], None]) -> None:
        while True:
            channel, event = self._r.blpop(self._channels)
            logger.info(f"Processing {channel}: {event}")
            event_cls = EVENTS[channel]
            event = event_cls(**json.loads(event))
            callback(event)

    def subscribe(self, event: Type[Event]) -> None:
        channel = CHANNELS[event]
        self._channels.append(channel)

    def __exit__(self, *_):
        self._r.close()


class RedisPublisher(AbstractPublisher):
    def __init__(self):
        self._r = redis.Redis(**get_redis_pubsub_connection_params())

    def publish(self, event: Event) -> None:
        channel = CHANNELS[event.__class__]
        event_json = json.dumps(asdict(event))
        logger.info(f"Publishing {event_json} to channel {channel}")
        self._r.rpush(channel, event_json)

    def __exit__(self, *_):
        self._r.close()


class FakePublisher(AbstractPublisher):
    def __init__(self):
        self._published: List[Event] = []

    def publish(self, event: Event) -> None:
        self._published.append(event)
