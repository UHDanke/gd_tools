from dataclasses import fields
from typing import Literal
from itertools import islice
from typing import get_type_hints
from pathlib import Path
from os import PathLike, getenv
import xml.etree.ElementTree as ET
import base64
import zlib
import gzip

def serialize(value):
    
    if value is None:
        return ''
        
    elif isinstance(value, str):
        return value
        
    elif isinstance(value, bool):
        return str(int(value))
        
    elif isinstance(value, (int, float)):
        return f"{value:g}"
    
    else:
        return str(value)


def read_elem(elem):
        
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
            return read_xml(elem)
        
        
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
                    result.append(read_elem(child))
        
    else:
        
        result = {}
        key = None
        
        for child in node:
            match child.tag:
                case 'k':
                    key = child.text
                    continue
                case _:
                    value = read_elem(child)
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
        write_xml(value, ET.SubElement(parent, "d"))
    
    else:
        ET.SubElement(parent, "s").text = str(value)


def write_xml(node, obj):
    
    if isinstance(obj, dict):
        
        for key, value in obj.items():
            
            ET.SubElement(node, "k").text = key
            
            write_elem(node, value)
            
    elif isinstance(obj, (list,tuple)):
        
        ET.SubElement(node, "k").text = "_IsArr"
        
        ET.SubElement(node, "t")
        
        for i, value in enumerate(obj,start=1):
            
            ET.SubElement(node, "k").text = f"k_{i}"
            
            write_elem(node, value)
            

def decode_string(string:str) -> str:

    base64_decoded = base64.urlsafe_b64decode(string.encode())
    
    decompressed = gzip.decompress(base64_decoded)
        
    return decompressed.decode()


def encode_string(string:str) -> str:
    
    gzipped = gzip.compress(string.encode(),mtime=0)
        
    base64_encoded = base64.urlsafe_b64encode(gzipped)
    
    return base64_encoded.decode()


def from_plist(string:str):
    
    tree = ET.fromstring(string)
    
    root = tree.getroot()
    
    return read_xml(root.find("dict"))


def to_plist(data:dict|list|tuple) -> str:
    
    root = ET.Element("plist", version="1.0", gjver="2.0")
    
    dict_elem = ET.SubElement(root, "dict")
    
    write_xml(dict_elem, data)
    
    return ET.tostring(root, encoding='unicode') 


def parse_plist(path:str|PathLike):
    
    tree = ET.parse(path)
    
    root = tree.getroot()
    
    parsed_xml = read_xml(root.find("dict"))

    return parsed_xml


def write_plist(data:dict|list|tuple, path:str|PathLike):
    
    root = ET.Element("plist", version="1.0", gjver="2.0")
   
    dict_elem = ET.SubElement(root, "dict")
    
    write_xml(dict_elem, data)
           
    tree = ET.ElementTree(root)
    
    tree.write(path, encoding="utf-8", xml_declaration=True)


def xor(string: str, key: int) -> str:
    
    return ("").join(chr(ord(char) ^ key) for char in string)


def decode_xml(data: str) -> str:

    return decode_string(xor(data, key=11))


def encode_xml(data: str) -> str:

    return xor(encode_string(data), key=11)


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
        
        result = cls()
        
        if string == '':
            return result
        
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
        
        return result

    
    def to_string(self):
        
        return self.SEPARATOR.join([serialize(x) for x in self])
    
    
    def __str__(self):

        return self.to_string()   


class CCDatMixin:
    
    BASEPATH = Path(getenv("LOCALAPPDATA")) / "GeometryDash"
    
    @classmethod
    def parse(cls,path:str|PathLike):
        pass
    
    @classmethod
    def write():
        pass
    