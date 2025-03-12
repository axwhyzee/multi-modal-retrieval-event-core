from enum import StrEnum
from pathlib import Path
from typing import Dict, Union, cast


class RepoObject: ...


class Asset(RepoObject, StrEnum):
    DOC = "DOCUMENT"
    DOC_THUMBNAIL = "DOCUMENT_THUMBNAIL"
    ELEM_THUMBNAIL = "ELEMENT_THUMBNAIL"


class Element(RepoObject, StrEnum):
    PLOT = "PLOT_ELEMENT"
    TEXT = "TEXT_ELEMENT"
    IMAGE = "IMAGE_ELEMENT"


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

ELEM_TO_MODAL: Dict[Element, Modal] = {
    Element.PLOT: Modal.TEXT,
    Element.TEXT: Modal.TEXT,
    Element.IMAGE: Modal.IMAGE,
}


def path_to_ext(path: Union[str, Path]) -> FileExt:
    if isinstance(path, str):
        path = Path(path)
    suffix = path.suffix
    return cast(FileExt, FileExt._value2member_map_[suffix])
