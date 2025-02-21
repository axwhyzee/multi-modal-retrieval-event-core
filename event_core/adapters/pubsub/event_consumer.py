import json
import logging
from typing import Callable

import redis
import redis.client

from event_core.adapters.pubsub.base import AbstractConsumer
from event_core.config import get_redis_connection_params
from event_core.domain.events import CHANNELS, EVENTS, Event

logger = logging.getLogger(__name__)


class RedisConsumer(AbstractConsumer):
    def __init__(self):
        self._r = redis.Redis(**get_redis_connection_params())
        self._consumer = self._r.pubsub(ignore_subscribe_messages=True)

    def listen(self, callback: Callable[[Event], None]) -> None:
        for message in self._consumer.listen():
            data = json.loads(message["data"])
            event_cls = EVENTS[message["channel"]]
            event = event_cls(**data)
            logger.info(f"Received: {event}")
            callback(event)

    def subscribe(self, event: Event) -> None:
        channel = CHANNELS[event.__class__]
        self._consumer.subscribe(channel)

    def __exit__(self, *_):
        self._r.close()
        self._consumer.close()
