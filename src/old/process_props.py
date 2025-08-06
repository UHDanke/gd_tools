# -*- coding: utf-8 -*-
import obj
import json

data = obj.from_file("all_1234_sanit.txt")

prop_set = dict()
prop_set["int"] = set()
prop_set["float"] = set()
prop_set["list"] = set()
prop_set["all"] = set()
prop_set["invalid"] = set()
for ob in data:  
    for key, value in ob.properties.items():
        match value:
            case "1":
                prop_set["int"].add(key)
            case "1.2":
                prop_set["float"].add(key)
            case "1.2.3.4":
                prop_set["list"].add(key)
            case _:
                prop_set["invalid"].add(key)

for key, value in prop_set.items():
    if key != "all":
        prop_set["all"] = prop_set["all"].union(value)
prop_list = dict()
for key, value in prop_set.items():
    
        
with open("props_1234.json","w") as file:
    json.dump(prop_set,file,indent="\t")