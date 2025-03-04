from enum import StrEnum
from pathlib import Path
from typing import Dict, Union, cast


class UnitType(StrEnum):
    CHUNK = "CHUNK"
    CHUNK_THUMBNAIL = "CHUNK_THUMBNAIL"
    DOC = "DOCUMENT"
    DOC_THUMBNAIL = "DOCUMENT_THUMBNAIL"


class Modal(StrEnum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"


class FileExt(StrEnum):
    JPG = ".jpg"
    JPEG = ".jpeg"
    PNG = ".png"
    MP4 = ".mp4"
    TXT = ".txt"
    PDF = ".pdf"


EXT_TO_MODAL: Dict[FileExt, Modal] = {
    FileExt.TXT: Modal.TEXT,
    FileExt.JPEG: Modal.IMAGE,
    FileExt.JPG: Modal.IMAGE,
    FileExt.PNG: Modal.IMAGE,
}


def path_to_ext(path: Union[str, Path]) -> FileExt:
    if isinstance(path, str):
        path = Path(path)
    suffix = path.suffix
    return cast(FileExt, FileExt._value2member_map_[suffix])
