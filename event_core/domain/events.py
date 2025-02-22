from dataclasses import dataclass
from typing import Dict, Type


@dataclass
class Event: ...


@dataclass
class ObjStored(Event):
    parent_key: str
    key: str


@dataclass
class DocStored(ObjStored): ...


@dataclass
class ChunkStored(ObjStored): ...


@dataclass
class DocThumbnailStored(ObjStored): ...


@dataclass
class ChunkThumbnailStored(ObjStored): ...


CHANNELS: Dict[Type[Event], str] = {}
EVENTS: Dict[str, Type[Event]] = {}


def _register_event(event_cls: Type[Event]) -> None:
    CHANNELS[event_cls] = event_cls.__name__
    EVENTS[event_cls.__name__] = event_cls


_register_event(ChunkStored)
_register_event(ChunkThumbnailStored)
_register_event(DocStored)
_register_event(DocThumbnailStored)
