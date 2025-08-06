import obj
import json

data = obj.from_file("test_level.txt")
    
with open("obj_ids.json","r") as file:
    obj_ids = json.load(file)

base_props = dict()
for i in range(2,599):
    base_props[i] = "1.2.3.4"

objects = list()
for o in obj_ids:
    new_obj = obj.Object();
    props = new_obj.properties
    props[1] = o
    props.update(base_props)
    objects.append(new_obj)
    
with open("output.txt","w") as file:
    file.write(obj.to_string(objects))