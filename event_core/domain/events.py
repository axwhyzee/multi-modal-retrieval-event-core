from dataclasses import dataclass
from typing import Dict, Type


@dataclass
class Event: ...


@dataclass
class _ObjStored(Event):
    obj_path: str


@dataclass
class DocStored(_ObjStored): ...


@dataclass
class ChunkStored(_ObjStored): ...


@dataclass
class DocThumbnailStored(_ObjStored): ...


@dataclass
class ChunkThumbnailStored(_ObjStored): ...


def _register_event(event: Type[Event]) -> None:
    CHANNELS[event] = event.__name__
    EVENTS[event.__name__] = event


CHANNELS: Dict[Type[Event], str] = {}
EVENTS: Dict[str, Type[Event]] = {}

_register_event(DocStored)
_register_event(DocThumbnailStored)
_register_event(ChunkStored)
_register_event(ChunkThumbnailStored)
