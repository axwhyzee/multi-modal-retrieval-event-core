import json
import logging
from dataclasses import asdict

import redis

from event_core.adapters.pubsub.base import AbstractPublisher
from event_core.config import get_redis_connection_params
from event_core.domain.events import CHANNELS, Event

logger = logging.getLogger(__name__)


class RedisPublisher(AbstractPublisher):
    def __init__(self):
        self._r = redis.Redis(**get_redis_connection_params())

    def publish(self, event: Event) -> None:
        channel = CHANNELS[event.__class__]
        event_json = json.dumps(asdict(event))
        logger.info(f"Publishing {event_json} to channel {channel}")
        self._r.publish(channel, event_json)

    def __exit__(self, *_):
        self._r.close()
