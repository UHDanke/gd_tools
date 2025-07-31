from dataclasses import fields
from typing import Literal
from itertools import islice
from typing import get_type_hints
from pathlib import Path
from os import PathLike


def serialize(value):
    
    if value is None:
        return ''
        
    elif isinstance(value, str):
        return value
        
    elif isinstance(value, bool):
        return str(int(value))
        
    else:
        return str(value)


class DataclassDeserializableMixin:
    
    __slots__ = ()
    
    SEPARATOR = 'a'
    STRICT = False
    STR_FORMAT = "list"
    
    @classmethod
    def from_string(cls, string:str, separator:str=None):
        
    
        separator = separator or cls.SEPARATOR
        
        if string == '':
            return cls()
        
        tokens = iter(string.split(separator))
        
        class_fields = fields(cls)
        class_types = get_type_hints(cls)

        class_args = dict()

        for f in class_fields:
            try:
                class_args[f.name] = class_types[f.name](next(tokens))
            
            except StopIteration:
                break
        
        return cls(**class_args)
    
    
    def to_string(self, str_format: Literal["list","dict"]=None):
        
        str_format = str_format or self.STR_FORMAT
        
        parts = []
        
        for i, field in enumerate(fields(self)):
            
            value = getattr(self, field.name)
            
            if str_format == "dict":
            
                if value is None:
                    continue
    
                parts.append(str(i))

            parts.append(serialize(value))
            
            
        return self.SEPARATOR.join(parts)

    
    def __str__(self):
        return self.to_string()


class DictDeserializableMixin:
    
    __slots__ = ()
    
    SEPARATOR = ','
    FORMAT_TO = {}
    
    @classmethod
    def from_string(cls, string:str, separator:str=None, format_to:callable=None):
        
        separator = separator or cls.SEPARATOR
        format_to = format_to or cls.FORMAT_TO
        
        result = cls()
        tokens = iter(string.split(separator))
    
        for key in tokens:
            
            if key.isdigit(): key = int(key)
            
            value = format_to.get(key, str)(next(tokens))
            
            result[key] = value
                
        return result
    
    
    def to_string(self) -> str:
                    
        return self.SEPARATOR.join([f"{k}{self.SEPARATOR}{serialize(v)}" for k, v in self.items()])


    def __str__(self):
        
        return self.to_string()
    
    
class ArrayDeserializableMixin:
    
    __slots__ = ()
    
    SEPARATOR = '.'
    GROUP_SIZE = 1
    FORMAT_TO = int
    
    @classmethod
    def from_string(cls, string:str, separator:str=None, group_size:int=None, format_to:callable=None):
        
        separator = separator or cls.SEPARATOR
        group_size = group_size or cls.GROUP_SIZE
        format_to = format_to or cls.FORMAT_TO
        
        if string == '':
            return cls()
        
        result = list()
        
        tokens = iter(string.split(separator))
        
        while True:
            if group_size > 1:
                item = list(islice(tokens, group_size))
            else:
                try:
                    item = next(tokens)
                except StopIteration:
                    break
                
            if not item:
                break
            else:
                result.append(format_to(item))
        
        return cls(result)

    
    def to_string(self):
        
        return self.SEPARATOR.join([serialize(x) for x in self])
    
    
    def __str__(self):

        return self.to_string()


def parse_elem(elem):
        
    match elem.tag:
        case 'i':
            return int(elem.text)
        case 'r':
            return float(elem.text)
        case 's':
            return str(elem.text)
        case 't':
            return None
        case 'd':
            return read_elem(elem)
        
        
def read_xml(node):
    
    nodes = len(node)
    
    if nodes == 0:
        return None
      
    if (    
            nodes > 0 and
            node[0].tag == "k" and node[0].text == "_IsArr" and
            node[1].tag == "t" and node[1].text == None
            ):
        
        result = []
        
        for child in islice(node, 2, None):
            match child.tag:
                case 'k':
                    continue
                case _:
                    result.append(parse_elem(child))
        
    else:
        
        result = {}
        
        for child in node:
            match child.tag:
                case 'k':
                    continue
                    key = child.text
                case _:
                    value = parse_elem(child)
        
                    if key is not None:
                        result[key] = value
                        
                        key = None
    
    return result


def write_elem(parent, value):
    
    if isinstance(value, int):
        ET.SubElement(parent, "i").text = str(value)
    
    elif isinstance(value, float):
        ET.SubElement(parent, "r").text = str(value)
    
    elif isinstance(value, str):
        ET.SubElement(parent, "s").text = value
    
    elif value is None:
        ET.SubElement(parent, "t")
    
    elif isinstance(value, (dict, list, tuple)):
        to_xml(value, ET.SubElement(parent, "d"))
    
    else:
        ET.SubElement(parent, "s").text = str(value)


def parse_xml(node, obj):
    
    if isinstance(obj, dict):
        
        for key, value in data.items():
            
            ET.SubElement(node, "k").text = key
            
            write_elem(node, value)
            
    elif isinstance(obj, (list,tuple)):
        
        ET.SubElement(node, "k").text = "_IsArr"
        
        ET.SubElement(node, "t")
        
        for i, value in enumerate(data,start=1):
            
            ET.SubElement(node, "k").text = f"k_{i}"
            
            write_elem(node, value)
            

class PlistMixin:
    
    __slots__ = ()
    
    
    @classmethod
    def from_plist(cls, path:str|PathLike):
        
        tree = ET.parse(path)
        root = tree.getroot()

        plist = read_xml(root.find("dict"))
               
        return cls(plist)
    
    
    def to_plist(self, path:str|PathLike):
        
        root = ET.Element("plist", version="1.0", gjver="2.0")
       
        dict_elem = ET.SubElement(root, "dict")
        
        parse_xml(dict_elem, self)
               
        tree = ET.ElementTree(root)
        
        tree.write(path, encoding="utf-8", xml_declaration=True)
