# -*- coding: utf-8 -*-
"""
Created on Mon Aug  4 15:54:06 2025

@author: porum
"""

from websocket import create_connection

from level_tools.classes.types import DictList, DictClass
from level_tools.classes.level import Level

class LiveEditor(Level):
    
    __slots__ = ('start','objects','socket')
    
    def __init__(self, lazy_load:bool=False):
        
        
        
    def 
        try:
           self.socket = create_connection("ws://127.0.0.1:1313")
           
       except ConnectionRefusedError:
           raise ConnectionRefusedError('No editor socket found!\nCheck that you have WSLiveEdit enabled and your editor is open.') 
           