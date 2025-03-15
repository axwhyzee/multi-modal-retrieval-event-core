from dataclasses import dataclass
from typing import Dict, Type

from ..types import Element
from .base import ObjStored


@dataclass
class ElementStored(ObjStored): ...


@dataclass
class PlotElementStored(ElementStored): ...


@dataclass
class TextElementStored(ElementStored): ...


@dataclass
class ImageElementStored(ElementStored): ...


@dataclass
class CodeElementStored(ElementStored): ...


ELEM_TYPES: Dict[Type[ElementStored], Element] = {
    PlotElementStored: Element.PLOT,
    TextElementStored: Element.TEXT,
    ImageElementStored: Element.IMAGE,
    CodeElementStored: Element.CODE,
}
