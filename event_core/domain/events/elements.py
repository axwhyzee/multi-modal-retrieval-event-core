from dataclasses import dataclass

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
