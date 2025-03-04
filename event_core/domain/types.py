from enum import StrEnum
from pathlib import Path
from typing import Union


class ObjectType(StrEnum):
    CHUNK = "CHUNK"
    CHUNK_THUMBNAIL = "CHUNK_THUMBNAIL"
    DOC = "DOCUMENT"
    DOC_THUMBNAIL = "DOCUMENT_THUMBNAIL"


class Modal(StrEnum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"


class FileExt(StrEnum):
    JPG = ".jpg"
    JPEG = ".jpeg"
    PNG = ".png"
    MP4 = ".mp4"
    TXT = ".txt"
    PDF = ".pdf"


def ext_from_path(path: Union[str, Path]) -> FileExt:
    if isinstance(path, str):
        path = Path(path)
    suffix = path.suffix
    return FileExt._value2member_map_[suffix]
