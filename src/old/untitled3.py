
from object_class import Level,Object

from properties import ids

import json

with open("obj_ids.json","r") as file:
    all_ids = json.load(file)

level = Level.gmd_load('test.gmd')

pool = level.objects


test_colors = list(range(0, 10)) + list(range(1000, 1020))

x = y = 15

for color in test_colors:
    
    x = 15
    
    for obj_id in all_ids:
        
        obj = Object({
            ids.id: obj_id,
            ids.color_1: color,
            ids.color_2: color,
            ids.x: x,
            ids.y: y
            })
        
        pool.append(obj)
    
        x += 30
        
    y += 30
        
level.gmd_save('obj_color_test.gmd')

