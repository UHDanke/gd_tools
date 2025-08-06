from level_objects import Object, ObjectList

from mappings import obj_id, prop_id

pool = ObjectList.from_file("C:/Users/porum/Geometry Dash/library/library/data/txt/default.txt")


def clean_obj(obj):
    
    obj.pop(155,None)
    obj.pop(156,None)
    
    if 2 in obj:
        obj[2] = 0
    
    if 3 in obj:
        obj[3] = 0
        
    for k,v in obj.items():
        if isinstance(v,(int,bool,float)):
            pass
        else:
            obj[k] = str(v)
    
    if obj.get(prop_id.id) == obj_id.particle_object:
        
        obj[prop_id.particle.data] = "30a-1a1a0.3a30a90a90a29a0a11a0a0a0a0a0a0a0a2a1a0a0a1a0a1a0a1a0a1a0a1a1a0a0a1a0a1a0a1a0a1a0a0a0a0a0a0a0a0a0a0a0a0a2a1a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0"
        
        
pool.apply(clean_obj)


default = dict()

for obj in pool:
    obj_id = obj.get(1)
    default.setdefault(obj_id,dict())
    
    default[obj_id].update(obj)

import json


lines = list()

for key, value in default.items():
    lines.append(f"    {repr(key)}: {repr(value)}")
                 

with open("objects.py","w") as file:
    
    file.write("Default = {\n")
    
    file.write(',\n'.join(lines))
    
    file.write('\n')
    
    file.write('    }')
