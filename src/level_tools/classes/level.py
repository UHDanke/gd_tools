# Typing
from typing import Union, Self
from pathlib import Path
from os import PathLike

# level decoding
import base64
import gzip
import zlib
import xml.etree.ElementTree as ET

# utils
from level_tools.classes.object import Object, ObjectList
from level_tools.classes.types import DictList, DictClass
from level_tools.classes.serialization import PlistMixin
    

class Level(PlistMixin,DictClass):
    
    __slots__ = ('start','objects')
    
    
    def __init__(self, *args, lazy_load:bool=False, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        if not lazy_load:
            self.load()
    
       
    @staticmethod
    def encode(object_pool: ObjectList) -> str:
        
        level_string = object_pool.to_string()
        
        compressed = gzip.compress(level_string.encode())
        
        encoded = base64.urlsafe_b64encode(compressed)
                                           
        return encoded.decode()
    
    
    def decode(self, level_string: str) -> ObjectList:
        
        decoded = base64.urlsafe_b64decode(level_string.encode())
        
        decompressed = zlib.decompress(decoded, 15 | 32)
        
        return ObjectList.from_string(decompressed.decode())
    
    @property
    def object_string(self):
        
        decoded = base64.urlsafe_b64decode(self['k4'].encode())
        
        decompressed = zlib.decompress(decoded, 15 | 32)
        
        return decompressed.decode()
        
        
    def save(self):
        
        self['k4'] = self.encode(ObjectList([self.start]) + self.objects)
        
        
    def load(self):
        
        pool = self.decode(self.get('k4'))
        self.start = pool.pop(0)
        self.objects = pool
        
        
    @classmethod
    def from_plist(cls, path:str|PathLike, lazy_load:bool=False):
        
        plist_dict = super().from_plist(path)
        
        return cls(plist_dict,lazy_load=lazy_load)
    
    
    def to_plist(self, path:str|PathLike, extension:str="gmd", update:bool=True):
        
        path = Path(path)
        
        if not path.suffix:
            path = (path / self['k2']).with_suffix('.' + extension.lstrip('.'))
                    
        if update:
            self.save()
        
        super().to_plist(path)
           
       
class LevelList(DictList):
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)      







