from dataclasses import dataclass


@dataclass
class Event: ...


@dataclass
class ObjStored(Event):
    obj_path: str


@dataclass
class DocStored(ObjStored): ...


@dataclass
class ChunkStored(ObjStored): ...


@dataclass
class DocThumbnailStored(ObjStored): ...


@dataclass
class ChunkThumbnailStored(ObjStored): ...
