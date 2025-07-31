import base64
import gzip
import os
from pathlib import Path


from level_tools.classes.types import DictList, DictClass

LOCALPATH = Path(os.getenv("LOCALAPPDATA")) / "GeometryDash


class SaveFile:

    @staticmethod
    def xor(string: str, key: int) -> str:
    	return ("").join(chr(ord(char) ^ key) for char in string)
    
    @staticmethod
    def decrypt_data(data: str) -> str:
    	base64_decoded = base64.urlsafe_b64decode(SaveFile.xor(data, key=11).encode())
    	decompressed = gzip.decompress(base64_decoded)
    	return decompressed.decode()
    
    @staticmethod
    def encrypt_data(data: str) -> str:
    	gzipped = gzip.compress(data.encode())
    	base64_encoded = base64.urlsafe_b64encode(gzipped)
    	return SaveFile.xor(base64_encoded.decode(), key=11)


with open(file_path, 'r', encoding='utf-8-sig') as f:
    xml = SaveFile.decrypt_data(f.read())
    
with open("save2.xml","w") as file:
    file.write(xml)
    

class CCLocalLevels(SaveFile,DictClass):
    
    __slots__ = ("path")
    
    
    def __init__(self, path:str|PathLike=None):
        
        if path is None:
            
            path = LOCALPATH / "CCLocalLevels.dat"
            
        self.path = path
        self.stream
        
    def open(self):
        
        
    
    