"""
A document contains:
 - Assets
   - Document: Full document data
   - Document thumbnail (Optional): Thumbnail of document
   - Element thumbnails (optional): Thumbnails of elements

  - Elements (at least 1)
   - Image elements
   - Text elements
   - Plot elements
   - Code elements

A single file can contain elements of multiple element types.

E.g.,
- A PDF can contain images, texts and plots
- A Markdown can contain codes and texts
"""

from enum import StrEnum
from pathlib import Path
from typing import Union, cast


class RepoObject: ...


class Asset(RepoObject, StrEnum):
    DOC = "DOCUMENT"
    DOC_THUMBNAIL = "DOCUMENT_THUMBNAIL"
    ELEM_THUMBNAIL = "ELEMENT_THUMBNAIL"


class Element(RepoObject, StrEnum):
    PLOT = "PLOT"
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    CODE = "CODE"


class FileExt(StrEnum):
    JPG = ".jpg"
    JPEG = ".jpeg"
    PNG = ".png"
    MP4 = ".mp4"
    TXT = ".txt"
    PDF = ".pdf"
    MD = ".md"
    PY = ".py"


def path_to_ext(path: Union[str, Path]) -> FileExt:
    if isinstance(path, str):
        path = Path(path)
    suffix = path.suffix
    return cast(FileExt, FileExt._value2member_map_[suffix])
