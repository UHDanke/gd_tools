# -*- coding: utf-8 -*-
import pandas as pd
import re


# Open property table
prop_table = pd.read_csv("../../data/csv/prop_table.csv")


# Sort Key IDs
def sort_id(s):
    if str(s).isdigit():
        return (0, int(s), '')
    m = re.match(r"([^\d]+)(\d+)$", str(s))
    if m:
        prefix, num = m.group(1), int(m.group(2))
        return (1, prefix, num)
    # Otherwise, sort these last by string
    return (2, str(s), -1)


prop_table['sort_key'] = prop_table['id'].map(sort_id)
prop_table = prop_table.sort_values(by='sort_key').reset_index(drop=True)
prop_table = prop_table.drop(columns=['sort_key'])
prop_table['id'] = prop_table['id'].apply(lambda x: int(x) if str(x).isdigit() else str(x))

# Map CSV types to library types
def map_gd_types(gd_type, gd_format):
    
    match gd_type:
        
        case 'int' | 'integer' | 'number':
            return 'int'
        
        case 'bool':
            return 'ibool'
        
        case 'float' | 'real':
            return 'float'
        
        case 'str' | 'string':
            
            match gd_format:
                
                case 'base64':
                    return 'EncodedString.decode_string'
                
                case 'hsv':
                    return 'HSV.from_string'
                
                case 'particle':
                    return 'Particle.from_string'
                
                case 'groups' | 'parent_groups' | 'events':
                    return 'IntList.from_string'
                
                case 'remaps' | 'weights' | 'sequence' | 'group remaps' | 'group weights' | 'group counts':
                    return 'PairList.from_string'
                
                case 'colors':
                    return 'ColorList.from_string'
                
                case 'color':
                    return 'Color.from_string'
                
                case _:
                    return 'str'
        case _:
            return 'str'

    
prop_class = (
    prop_table.dropna(how='all').groupby('id')
    .apply(lambda g: pd.Series({
        'aliases': None if g['alias'].isna().all() else tuple(g['alias']),
        'type': map_gd_types(g['type'].iloc[0], g['format'].iloc[0]),
        'gd_type': g['type'].iloc[0],
        'format': g['format'].iloc[0],
    }))
    .reset_index()
)

prop_class = prop_class.where(pd.notnull(prop_class), None)

    
def list_to_file(path, iterable):
    with open(path,"w") as file:
        for line in iterable:
            file.write(line+'\n')

# Write type_casting/object_properties.py
lines = list()
lines.append("from level_tools.classes.text import EncodedString")
lines.append("from level_tools.classes.lists import PairList, IntList")
lines.append("from level_tools.classes.hsv import HSV")
lines.append("from level_tools.classes.particle import Particle")
lines.append("from level_tools.classes.colors import Color, ColorList")
lines.extend([""]*2)
lines.append("ibool = lambda x: bool(int(x))")
lines.extend([""]*2)
lines.append("PROPERTY_TYPES = {")

for _, row in prop_class.iterrows():
    lines.append(f"    {repr(row['id'])}: {row['type']},")
    
lines.append("}")

list_to_file("type_casting/object_properties.py",lines)


from collections import defaultdict

alias_ids = prop_table[['id','alias']]
alias_ids=alias_ids.dropna()
aliases = dict(zip(alias_ids['alias'],alias_ids['id']))


def tree():
    return defaultdict(tree)


def build_tree(root, aliases):

    for path, val in aliases.items():
        parts = path.split('.')
        node = root
        for part in parts[:-1]:
            node = node[part]
        node[parts[-1]] = val


def render_tree(node, indent=0):
    lines = []
    indent_str = '    ' * indent
    
    
    val_keys = [k for k, v in node.items() if not isinstance(v, defaultdict)]
    dd_keys = [k for k, v in node.items() if isinstance(v, defaultdict)]
    
    def sort_key(k):
        v = node[k]
        if isinstance(v, int):
            return (0, v)
        if isinstance(v, str) and v.isdigit():
            return (0, int(v))
        return (1, str(v))
    
    
    for key in sorted(val_keys, key=sort_key):
        val = node[key]
        
        lines.append(f"{indent_str}{key} = {repr(val)}")
    
    if val_keys: lines.append('')
    
    for key in sorted(dd_keys):
        val = node[key]
        lines.append(f"{indent_str}class {key}:")
        children = render_tree(val, indent + 1)
        if children:
            lines.extend(children)
        else:
            lines.append(f"{indent_str}    pass")
                
    if dd_keys or not val_keys: lines.append('')
            
    return lines


def remove_trailing(lines, value=''):
    while lines and lines[-1] == value:
        lines.pop()
    return lines


# Write mappings/object_properties.py
lines = list()
lines.append("class PropertyID:")
root = tree()
build_tree(root, aliases)
lines.extend(remove_trailing(render_tree(root, indent=1)))
list_to_file("mappings/object_properties.py",lines)



# Open object id table
obj_id_table = prop_table = pd.read_csv("../../data/csv/object_table.csv")


obj_alias_ids = prop_table[['id','alias']]
obj_alias_ids=obj_alias_ids.dropna()
obj_alias_ids.sort_values(by='id')
obj_aliases = dict(zip(obj_alias_ids['alias'],obj_alias_ids['id']))


# Write mappings/object_ids.py
lines = list()
lines.append("class ObjectID:")
obj_root = tree()
build_tree(obj_root, obj_aliases)
lines.extend(remove_trailing(render_tree(obj_root, indent=1)))
list_to_file("mappings/object_ids.py",lines)


remap_table = pd.read_csv("../../data/csv/remap_table.csv")

def convert_condition(data):
    
    if isinstance(data, str):
        t = data.split()
    
        return f"lambda obj: obj.get(prop_id.{t[0]},0) {t[1]} {t[2]}"
    
    else:
        return data

def convert_default(data):
    
    if isinstance(data, str):
        
        return f"lambda obj_id: {data}.get(obj_id,0)"

remap_table.columns = remap_table.columns.str.replace(' ', '_')
remap_table["type"] = remap_table["type"].str.replace(' ', '_')
remap_table["object_id"].fillna("'any'", inplace=True)
remap_table["min"].fillna(-2**31, inplace=True)
remap_table["max"].fillna(2**31-1, inplace=True)
remap_table["default"].fillna(0, inplace=True)
remap_table = remap_table.where(pd.notnull(remap_table), None)

def try_convert_int(val):
    try:
        return int(val)
    except (ValueError, TypeError):
        return val

# First convert strings to int where possible
remap_table["object_id"] = remap_table["object_id"].apply(try_convert_int)


remap_table['min'] = remap_table['min'].astype(int)
remap_table['max'] = remap_table['max'].astype(int)




result = defaultdict(list)

for _, row in remap_table.iterrows():
    obj_id = row['object_id']
    entry = row.drop(labels='object_id').to_dict()
    result[obj_id].append(entry)
    
lines = list()
lines.append("from level_tools.mappings.object_ids import ObjectID as obj_id")
lines.append("from level_tools.mappings.object_properties import PropertyID as prop_id")
lines.append("from level_tools.mappings.color_props import ColorProp as color_prop")
lines.append("from level_tools.defaults.color_default import COLOR_1_DEFAULT, COLOR_2_DEFAULT")
lines.extend([""]*2)
lines.append("ID_RULES = {")


def dict_repr(d, keys):
    parts = []
    for k, v in d.items():
        if v is not None:
            key_str = repr(k)
            val_str = repr(v) if k in keys else str(v)
            parts.append(f"{key_str}: {val_str}")
    return "{" + ", ".join(parts) + "}"

mlist = []
for key, value in result.items():
    nlist = []
    for item in value:
        nlist.append("    "*3+dict_repr(item,['type']))
    mlist.append("    "+f"{key}: "+"[\n"+',\n'.join(nlist)+"\n"+"    "*2+"]")

lines.append(',\n'.join(mlist))

lines.append("    "+"}")
lines.extend([""]*1)
lines.append(
"""
def filter_rules(condition:callable, rule_list=ID_RULES):
    
    new_dict = {}
    
    for key, value in rule_list.items():
        
        new_list = []
        
        for item in value:
            
            if condition(item):
                
                new_list.append(item)
            
        if new_list != []:
            
            new_dict[key] = new_list
            
    return new_dict
""")

list_to_file("type_casting/id_rules.py",lines)