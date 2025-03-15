"""
On successful storage of objects, the Storage Service emits events
defined in this event schema. Events are not emitted in any other ways.
Events are consumed by the other services that typically fetch data of
the object using the key in the event payload.

Everything that can be stored by the Storage Service, quantifies as an
Object. Objects can be whole documents, thumbnails, or document
elements, where elements are chunks of data with well-defined
boundaries, extracted from the parent document.
"""

from typing import Dict, Type

from .base import DocStored, DocThumbnailStored, ElementThumbnailStored, Event
from .elements import (
    ElementStored,
    ImageElementStored,
    PlotElementStored,
    TextElementStored,
)

CHANNELS: Dict[Type[Event], str] = {}
EVENTS: Dict[str, Type[Event]] = {}


def _register_event(event_cls: Type[Event]) -> None:
    """Only registered events have an associated channel"""

    CHANNELS[event_cls] = event_cls.__name__
    EVENTS[event_cls.__name__] = event_cls


_register_event(ElementStored)
_register_event(PlotElementStored)
_register_event(TextElementStored)
_register_event(ImageElementStored)
_register_event(ElementThumbnailStored)
_register_event(DocStored)
_register_event(DocThumbnailStored)
