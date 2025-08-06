from object_class import Level

from properties import ids

level = Level.gmd_load('obj_color_test_output.gmd')

pool = level.objects


obj_ids = pool.unique_values(lambda obj: [obj.get(ids.id,0)])

colors = {}


test_colors = set(list(range(1, 10)) + list(range(1000, 1020)))

for obj in pool:
    
    obj_id = obj.get(ids.id, 0)
    
    colors.setdefault(obj_id, [])
    colors[obj_id].extend(obj.pluck(ids.color_1,ids.color_2))

defaults = {}

for obj_id, color in colors.items():
    
    default = test_colors.difference(color)
    
    if len(default) > 0:
        defaults[obj_id] = default
    
