from level_tools.classes.serialization import DataclassDeserializableMixin

from dataclasses import dataclass


@dataclass(slots=True)
class HSV(DataclassDeserializableMixin):
    
    hue: float = 0
    saturation: float = 1
    value: float = 1
    saturation_add: bool = False
    value_add: bool = False