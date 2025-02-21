from dataclasses import dataclass


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
