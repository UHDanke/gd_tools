# Imports
from typing import Union, Self
from os import PathLike

# Package Imports
from level_tools.classes.types import DictList, DictClass
from level_tools.classes.serialization import DictDeserializableMixin, ArrayDeserializableMixin, decode_string, encode_string
from level_tools.casting.object_properties import PROPERTY_TYPES
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
        try:      
            return super().from_string(string.rstrip(";"),format_to=key_format)
        except:
            print(string)
            raise ValueError
    
    def to_string(self) -> str:
        
        return super().to_string() + ";"

    @classmethod
    def default(cls, object_id) -> Self:
        
        return cls(cls.DEFAULTS.get(object_id,{}))


class ObjectList(ArrayDeserializableMixin,DictList):
    
    __slots__ = ()
    
    SEPARATOR = ";"
    FORMAT_TO = Object.from_string
    
    def __init__(self, *args):
        
        super().__init__(*args)
    

    def to_string(self, encoded:bool=False) -> str:
        
        string = "".join([obj.to_string() for obj in self])
        
        if encoded:
            string = encode_string(string)
            
        return string
    
    
    @classmethod
    def from_string(cls, string, encoded:bool=False, key_format:dict=None):
        
        if encoded:
            string = decode_string(string)
        
        return super().from_string(string.strip(";"), format_to=key_format)

    
    
    def to_file(self, path:str|PathLike, encoded:bool=True):
        
        with open(path, "w") as file:
            string = self.to_string(encoded=encoded)
            
            file.write(string)


    @classmethod
    def from_file(cls, path: Union[str, PathLike], encoded:bool=True) -> Self:
        
        with open(path, "r") as file:
            
            string = file.read()
            
            return cls.from_string(string,encoded=encoded)
