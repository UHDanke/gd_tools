# Imports
from typing import Union, Self
from pathlib import Path
from os import PathLike

# Package Imports
from level_tools.classes.object import Object, ObjectList
from level_tools.classes.types import DictList, DictClass
from level_tools.classes.serialization import decode_string, encode_string, parse_plist, write_plist
    

class Level(DictClass):
    
    __slots__ = ('start','objects')
    
    
    def __init__(self, *args, lazy_load:bool=False, **kwargs):
        
        super().__init__(*args, **kwargs)
                
        if not lazy_load:
            self.load()
    
    
    @property
    def object_string(self):
        
        return decode_string(self.get('k4'))
        
        
    def save(self):
        
        string = (ObjectList([self.start]) + self.objects).to_string()
        self['k4'] = encode_string(string)
        
        
    def load(self):

        string = decode_string(self.get('k4'))
        
        pool = ObjectList.from_string(string)

        self.start = pool.pop(0)
        self.objects = pool
    
    
    @classmethod
    def from_template(cls, path:str|PathLike, **kwargs):
        
        level_dict = LEVEL_TEMPLATE.copy()
        
        level_dict.update(kwargs)
        
        return cls(**level_dict)
    
    
    @classmethod
    def from_plist(cls, path:str|PathLike, lazy_load:bool=False):
        
        parsed = parse_plist(path)

        return cls(parsed, lazy_load=lazy_load)
    
    
    def to_plist(self, path:str|PathLike, extension:str="gmd", update:bool=True):
        
        path = Path(path)
        
        if not path.suffix:
            path = (path / self['k2']).with_suffix('.' + extension.lstrip('.'))
                    
        if update:
            self.save()
        
        write_plist(self, path)
        

# Load a template from plist
try:
    LEVEL_TEMPLATE = Level.from_plist()
except:
    LEVEL_TEMPLATE = Level(lazy_load=True)


class LevelList(DictList):
    
    def __init__(self, *args):
        
        super().__init__(*args, **kwargs)      
    
    
    @classmethod
    def from_plist(cls, path:str|PathLike, lazy_load:bool=False):
        
        return cls(*[Level(obj, lazy_load=lazy_load) for obj in parse_plist(path)])
    
    
    @classmethod
    def to_plist(self, path:str|PathLike, update:bool=True):
        
        if update:
            for level in self:
                level.save()
        
        write_plist(self, path)



