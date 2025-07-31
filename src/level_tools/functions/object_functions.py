from level_objects import Object

from mappings import color_id, prop_id


def clean_gid_parents(obj:Object):
    
    groups = obj.get(prop_id.groups,[])
    parents = obj.get(prop_id.parent_groups,[])
    
    for i, parent in enumerate(parents):
        if parent not in groups:
            parents.pop(i)

            
def clean_duplicate_groups(obj:Object):
    
    groups = obj.get(prop_id.groups,[])
    seen = set()

    for i, group in enumerate(groups):
        if group in seen:
            group.pop(i)
            
        seen.add(group)


def clean_lighter(obj:Object, replacement:int=color_id.white):
    
    if obj.get(prop_id.color_1) == color_id.lighter:
        obj[prop_id.color_1] = replacement
    
    
def offset_position(obj:Object, offset_x:float=0, offset_y:float=0):
        
    if (val := obj.get(prop_id.x)): obj[prop_id.x] = val + offset_x
    if (val := obj.get(prop_id.y)): obj[prop_id.x] = val + offset_y

    