from enum import StrEnum
from typing import Dict


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

