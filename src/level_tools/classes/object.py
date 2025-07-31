# Imports
from typing import Union, Self
from os import PathLike

# Package Imports
from level_tools.classes.types import DictList, DictClass
from level_tools.classes.serialization import DictDeserializableMixin
from level_tools.type_casting.object_properties import PROPERTY_TYPES
from level_tools.defaults.objects import OBJECT_DEFAULT


class Object(DictDeserializableMixin,DictClass):
    
    __slots__ = ()
    
    SEPARATOR = ","
    FORMAT_TO = PROPERTY_TYPES
    DEFAULTS = OBJECT_DEFAULT
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @classmethod
    def from_string(cls, string, key_format:dict=None) -> Self:
                
        return super().from_string(string.rstrip(";"),format_to=key_format)
    
    
    def to_string(self) -> str:
        
        return super().to_string() + ";"

    @classmethod
    def default(cls, object_id) -> Self:
        
        return cls(cls.DEFAULTS.get(object_id,{}))


class ObjectList(DictList):
    
    __slots__ = ()
    
    def __init__(self, *args):
        
        super().__init__(*args)
    

    def to_string(self) -> str:
        return "".join([obj.to_string() for obj in self])
    
    def __str__(self) -> str:
        return self.to_string()
    
    @classmethod
    def from_string(cls, object_string, encoded:bool=False) -> Self:
        pool = cls()
        for i, obj in enumerate(object_string.split(';')):
            if obj == '':
                continue
            else:
                pool.append(Object().from_string(obj))
    
        return pool
    
    
    def to_file(self, path:str|PathLike):
        with open(path, "w") as file:
            file.write(self.to_string())
    
            
    @classmethod
    def from_file(cls, path: Union[str, PathLike]) -> Self:
        with open(path, "r") as file:
            return cls.from_string(file.read())