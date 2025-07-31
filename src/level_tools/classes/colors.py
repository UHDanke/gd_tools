# Package Imports
from level_tools.classes.serialization import DictDeserializableMixin, ArrayDeserializableMixin
from level_tools.classes.types import DictClass, DictList
from level_tools.type_casting.color import COLOR_TYPES


class Color(DictDeserializableMixin,DictClass):
    
    __slots__ = ()
    
    SEPARATOR = '_'

    FORMAT_TO = COLOR_TYPES
    

class ColorList(ArrayDeserializableMixin,DictList):

    __slots__ = ()
    
    SEPARATOR = '|'
    FORMAT_TO = Color.from_string
    
    def __init__(self, *iterable):
        super().__init__(*iterable)
    
    def __str__(self):
        return super().__str__()