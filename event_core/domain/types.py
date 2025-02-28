from enum import StrEnum


class ObjectType(StrEnum):
    CHUNK = "CHUNK"
    CHUNK_THUMBNAIL = "CHUNK_THUMBNAIL"
    DOC = "DOCUMENT"
    DOC_THUMBNAIL = "DOCUMENT_THUMBNAIL"


class Modal(StrEnum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
