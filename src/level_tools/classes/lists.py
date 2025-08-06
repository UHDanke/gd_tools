# Imports
from dataclasses import dataclass

# Package Imports
from level_tools.classes.types import ListClass
from level_tools.classes.serialization import ArrayDeserializableMixin


class IntList(ArrayDeserializableMixin,ListClass):
    
    __slots__ = ()
    
    def __init__(self, *iterable):
        super().__init__(*iterable)
    

@dataclass(slots=True)
class Pair:    
    key: int
    value: int

    def __post_init__(self):
        self.key = int(self.key)
        self.value = int(self.value)
        

class PairList(ArrayDeserializableMixin,ListClass):
    
    __slots__ = ()
    
    GROUP_SIZE = 2
    FORMAT_TO = lambda array: Pair(*array)
    
    def __init__(self, *iterable):
        super().__init__(*iterable)

    def keys(self):
        for p in self:
            yield p.key
    
    def values(self):
        for p in self:
            yield p.value
    
    def replace(self, *keys:str, value_map:dict=None, key_map:dict=None):
        
        value_map = value_map or {}
        key_map = key_map or {}
        
        for pair in self:
            if pair.key in keys or not keys:
                pair.key = key_map.get(pair.key, pair.key)
                pair.value = value_map.get(pair.value, pair.value)
                    
        return self