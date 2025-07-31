from .types import StrClass

import base64


class EncodedString(StrClass):
    
    __slots__ = ()
    
    @classmethod
    def from_encoded_str(cls, string):
        return cls(base64.urlsafe_b64decode(string.encode()).decode())

    def to_encoded_str(self):
        return base64.urlsafe_b64encode(self.encode()).decode()

    def __str__(self):
        return self.to_encoded_str()
    
    



    
