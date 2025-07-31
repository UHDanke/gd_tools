# -*- coding: utf-8 -*-
import pandas as pd
import re

prop_table = pd.read_csv("../../data/csv/prop_table.csv")

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

def map_gd_types(gd_type, gd_format):
    
    match gd_type:
        
        case 'int' | 'integer' | 'number':
            return 'int'
        
        case 'bool':
            return 'bool'
        
        case 'float' | 'real':
            return 'float'
        
        case 'str' | 'string':
            
            match gd_format:
                
                case 'base64':
                    return 'EncodedString.from_encoded_str'
                
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

    
lines = list()

def list_to_file(path, iterable):
    with open(path,"w") as file:
        for line in lines:
            file.write(line+'\n')

lines.append("from prop_class import EncodedString, PairList, IntList, HSV, Particle, Color, ColorList")

lines.extend([""]*2)
lines.append("TYPES = {")

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

lines = list()
lines.append("class Mapping:")
root = tree()
build_tree(root, aliases)
lines.extend(remove_trailing(render_tree(root, indent=1)))
list_to_file("mappings/object_properties.py",lines)




obj_id_table = prop_table = pd.read_csv("../../data/csv/obj_table.csv")


obj_alias_ids = prop_table[['id','alias']]
obj_alias_ids=obj_alias_ids.dropna()
obj_alias_ids.sort_values(by='id')
obj_aliases = dict(zip(obj_alias_ids['alias'],obj_alias_ids['id']))

lines = list()
lines.append("class Mapping:")
obj_root = tree()
build_tree(obj_root, obj_aliases)
lines.extend(remove_trailing(render_tree(obj_root, indent=1)))
list_to_file("mappings/object_ids.py",lines)

