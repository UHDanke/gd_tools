from .types import StrClass

import base64


class EncodedString(StrClass):
    
    __slots__ = ()
    
    @classmethod
    def decode_string(cls, string):
        try:
            return cls(base64.urlsafe_b64decode(string.encode()).decode())
        except:
            return cls("")
    def encode_string(self):
        return base64.urlsafe_b64encode(self.encode()).decode()

    def __str__(self):
        return self.encode_string()
    