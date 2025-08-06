from level_tools.classes.object import Object
from level_tools.mappings import color_id, prop_id
from level_tools.casting import ID_RULES


def clean_gid_parents(obj:Object):
    """
    Removes group ID parents that are not present in the groups of an object.
    
    Group ID parents are used as the target by certain triggers and do not display if they aren't also present as a group, which may lead to "phantom group" issues.

    Parameters
    ----------
    obj : Object
        The object to modify.

    Returns
    -------
    None.

    """
    if (parents:=obj.get(prop_id.parent_groups)) is not None:
        
        new = set(*parents).intersection(obj.get(prop_id.groups,[]))

        obj[prop_id.parent_groups] = parents.__class__(new)

            
def clean_duplicate_groups(obj:Object):
    """
    Removes duplicate groups from an object. 
    
    Duplicate groups may multiply the effects of a trigger on an object.

    Parameters
    ----------
    obj : Object
        The object to modify.

    Returns
    -------
    None.

    """
    if (groups:=obj.get(prop_id.groups)) is not None:
        
        obj[prop_id.groups] = groups.__class__(set(*groups))


def clean_lighter(obj:Object, replacement:int=color_id.white):
    """
    Replaces the base lighter color of an object (which crash the game) with another color.

    Parameters
    ----------
    obj : Object
        The object to modify.
    replacement : int, optional
        DESCRIPTION. Defaults to white.

    Returns
    -------
    None.

    """
    if obj.get(prop_id.color_1) == color_id.lighter:
        
        obj[prop_id.color_1] = replacement
    

def clean_zeros(obj:Object):
    """
    Removes object properties with value 0 in-place.

    Parameters
    ----------
    obj : Object
        The object to modify.

    Returns
    -------
    None.

    """
    for key, value in obj.items():
        
        if value == 0:
            obj.pop(key)
            

    
def offset_position(obj:Object, offset_x:float=0, offset_y:float=0):
    """
    Offsets the position of an object.

    Parameters
    ----------
    obj : Object
        The object for which to offset the position.
    offset_x : float, optional
        The horizontal offset. Default to 0.
    offset_y : float, optional
        The vertical offset. Defaults to 0.

    Returns
    -------
    None.

    """
    if (val := obj.get(prop_id.x)): obj[prop_id.x] = val + offset_x
    if (val := obj.get(prop_id.y)): obj[prop_id.x] = val + offset_y


def get_ids(obj:Object, rule_dict=ID_RULES) -> tuple:
    """
    Compiles unique ID data referenced by an object.

    Parameters
    ----------
    obj : Object
        The object to search for IDs.

    Yields
    ------
    tuple
        A tuple containing the IDs found, with the following structure:
        (id:int, type:str, is_remappable:bool, min:int, max:int)
    """
    result = set()

    rules = list()
    
    # ids are compiled based on a list of rules
    for oid in ("any", obj.get(prop_id.id,0)):
        
        if (val:=rule_dict.get(oid)) is not None:
            
            rules.extend(val)
    
    for rule in rules:

        pid = rule.get("property_id")
        
        if pid is not None and (val:=obj.get(pid)) is not None:
            
            if (cond:=rule.get("condition")) and callable(cond) and not cond(obj):
                continue
            
            if (func:=rule.get("function")) and callable(func):
                val = func(val)

            def id_dict(value):
                
                default = rule.get('default')
                
                if callable(default):
                    
                    value = default(value)
                
                elif value is None:
                    
                    value = default or 0
                    
                return (
                    value,
                    rule.get('type','none'),
                    (rule.get('remappable',False) and obj.get(prop_id.trigger.spawn_triggered,False)),
                    rule.get('min',-2**31),
                    rule.get('max',2**31-1)
                    )
            

            if rule.get("iterable"):
                for v in val:
                    result.add(id_dict(v))
                
            else:
                result.add(id_dict(val))
                
    yield from result