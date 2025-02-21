from dataclasses import dataclass
from enum import StrEnum
from typing import Dict, Type


class ObjectType(StrEnum):
    CHUNK = "CHUNK"
    CHUNK_THUMBNAIL = "CHUNK_THUMBNAIL"
    DOC = "DOCUMENT"
    DOC_THUMBNAIL = "DOCUMENT_THUMBNAIL"


@dataclass
class Event: ...


@dataclass
class ObjectStored(Event):
    obj_path: str
    obj_type: ObjectType


def _register_event(event: Type[Event]) -> None:
    CHANNELS[event] = event.__name__
    EVENTS[event.__name__] = event


# channel to event map and reverse map
CHANNELS: Dict[Type[Event], str] = {}
EVENTS: Dict[str, Type[Event]] = {}

_register_event(ObjectStored)
