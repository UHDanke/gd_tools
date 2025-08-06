# -*- coding: utf-8 -*-
"""
Created on Sat Jul 12 14:24:08 2025

@author: porum
"""

import pandas as pd

df = pd.read_csv('new_groups (1) - Sheet2.csv')
df['id'] = df['id'].astype(str)

df_filtered = df[~df['test value'].isna()]

df_filtered = df_filtered.drop_duplicates(subset=df.columns[0])

import json

with open("obj_ids.json") as file:
    obj_ids = json.load(file)

from ObjectClass import ObjectPool, Object, from_file

paste = False

if paste:
    prop_dict = dict(zip(df_filtered["id"], df_filtered["test value"]))
    
    pool = ObjectPool()
    
    for obj in obj_ids:
        new_obj = Object()
        new_obj[1] = obj
        new_obj.update(prop_dict)
        pool.append(new_obj)
    
    with open("level_string_output.txt","w") as file:
        file.write(pool.to_string())


pasted_pool = from_file("level_string_without_save.txt")

result_dict = dict()
for obj in pasted_pool:
    for key, value in obj.items():
        result_dict.setdefault(str(key),set())
        result_dict[str(key)].add(value)

group_names = pd.read_csv('Prop Tables - Sheet7.csv')

for key,value  in result_dict.items():
    result_dict[key] = ", ".join(list(value))
    

from collections import defaultdict

temp_groups = defaultdict(list)

all_set = set()

for d in pasted_pool:
    for k in d.keys():
        all_set.add(k)

common_set = all_set

for d in pasted_pool:
    common_set.intersection_update(d.keys())

for d in pasted_pool:
    id_val = d[1]
    key_set = frozenset(d.keys()-common_set)
    temp_groups[key_set].append(id_val)



# Generate final output with placeholder group names
output = list()

for i, (key_set, ids) in enumerate(temp_groups.items(), start=1):
    group_name = f"group_{i}"
    try:
        alias = group_names.loc[group_names['id'] == i, 'group'].values[0]
        output.append({
            "alias": alias,
            "group_members": ids,
            "group_keys": list(key_set)  # optional: sort keys for consistency
        })
    except:
        pass

output.append({
        "alias": "common",
        "group_members": obj_ids,
        "group_keys": list(common_set)  # optional: sort keys for consistency
})


df['result value'] = df['id'].map(result_dict)

result_dict = dict()
for obj in output:
    for key in obj["group_keys"]:
        result_dict.setdefault(str(key),list())
        result_dict[str(key)].append(obj["alias"])

opposite_dict = dict()
all_group_names = set(group_names["group"])
print(all_group_names)
for key, value in result_dict.items():

    opposite_dict[str(key)] = list(all_group_names-set(value))   


for key,value  in result_dict.items():
    result_dict[key] = ", ".join(list(value))

for key,value  in opposite_dict.items():
    if len(value) > 10:
        opposite_dict[key] = "-"
    opposite_dict[key] = ", ".join(list(value))
    
df['groups'] = df['id'].map(result_dict)
df['not in'] = df['id'].map(opposite_dict)


pretty_output = list()
for o in output:
    n = o.copy()
    n["group_members"] = ', '.join([str(x) for x in n["group_members"]])
    n["group_keys"] =  ', '.join([str(x) for x in n["group_keys"]])
    pretty_output.append(n)
    
groups_df = pd.DataFrame(pretty_output)
groups_df.to_csv("groups_df.csv")    


output_pool = ObjectPool()


import base64

y = 15
for value in output:
    x = 15
    key = value["alias"]
    text = base64.urlsafe_b64encode(key.encode()).decode('utf-8')
    output_pool.append(Object({1:914,2:x,3:y,31:text}))
    x += 30*5
    for obj_id in value["group_members"]:
        output_pool.append(Object({1:obj_id,2:x,3:y}))
        x += 30
    
    y-=30

with open("groups_output.txt","w") as file:
    file.write(output_pool.to_string())


df.to_csv("new_groups.csv", index=False)