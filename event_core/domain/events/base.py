from dataclasses import dataclass


@dataclass
class Event: ...


@dataclass
class ObjStored(Event):
    key: str


@dataclass
class DocStored(ObjStored): ...


@dataclass
class DocThumbnailStored(ObjStored): ...


@dataclass
class ElementThumbnailStored(ObjStored): ...
