from level_tools.mappings import prop_id, color_id, obj_id, color_prop
from level_tools.casting import ID_RULES, filter_rules
from level_tools.classes.level import Level
from level_tools.classes.colors import Color
from level_tools.classes.object import ObjectList, Object
from level_tools.functions.object_functions import get_ids

def create_color_triggers(level:Level, offset_x:float=0, offset_y:float=-30, color_filter:callable=None) -> ObjectList:
    """
    Converts a level's default colors into color triggers.

    Parameters
    ----------
    level : Level
        The level to retrieve colors from.
    offset_x : float, optional
        Horizontal offset between triggers. The default is 0.
    offset_y : float, optional
        Vertical offset between triggers. The default is -30.

    Returns
    -------
    ObjectList
        An ObjectList containing the generated color triggers.
    """

    mapping = {
        color_prop.red: prop_id.trigger.color.red,
        color_prop.green: prop_id.trigger.color.green,
        color_prop.blue: prop_id.trigger.color.blue,
        color_prop.blending: prop_id.trigger.color.blending,
        color_prop.channel: prop_id.trigger.color.channel,
        color_prop.copy_id: prop_id.trigger.color.copy_id,
        color_prop.opacity: prop_id.trigger.color.opacity,
        color_prop.hsv: prop_id.trigger.color.hsv,
        color_prop.copy_opacity: prop_id.trigger.color.copy_opacity,
        }
    
    pool = ObjectList()
    
    x = y = 0
    
    if (colors := level.start.get(prop_id.level.colors)) is not None:
        
        def filter_predefined(color:Color):
            
                exclude = [color_id.black, color_id.white, color_id.lighter, color_id.player_1, color_id.player_2]
                
                return (color[color_prop.channel] not in exclude)
        
        color_filter = color_filter or filter_predefined
        
        for color in colors.where(color_filter):
            
            obj = Object.default(obj_id.trigger.color)
            
            pool.append(obj)
            
            for color_key, obj_key in mapping.items():
                
                if color_key in color:
                    obj[obj_key] = color[color_key]
                
                match color.get(color_prop.copy_id):
                    case 1:
                        obj[prop_id.trigger.color.player_1] = True
                    
                    case 2:
                        obj[prop_id.trigger.color.player_2] = True
                    
                    case _:
                        pass
            
            obj[prop_id.trigger.color.duration] = 0
            
            obj[prop_id.x] = x
            obj[prop_id.y] = y
            
            x += offset_x
            y += offset_y
    
    
    return pool


def reset_unused(level:Level):
    
    rule_dict = filter_rules(lambda x: x[1] in ["color_id","remap_base"])
    
    values = level.objects.unique_values(get_ids, rule_dict=rule_dict)
    

def chunks(pool, func:callable=ObjectList):
    
    result = dict()
    
    for obj in pool:

        chunk_x = result.setdefault(int(obj.get(prop_id.x,0)/100), {})
        chunk_y = chunk_x.setdefault(int(obj.get(prop_id.y,0)/100), list())
        chunk_y.append(obj)
    
    for chunks in result.values():
        for y, value in chunks.items():
            chunks[y] = func(value)
            
    return result


test = Level.from_plist('C:/Users/porum/Geometry Dash/library/gd_tools/data/gmd/P2 Memory Lane.gmd')


def merge_levels(level_list, **kwargs):
    
    groups = list()
    
    # calculate group usage
    for level in levels:
        
        pools = list(ObjectList([level.start]),level.objects)
        
        for pool in pools:
        
        values = list(filter(lambda x: x[3] <= x[0] <= x[4], pool.unique_values(get_ids)))
        
        groups.append(values)

    
    