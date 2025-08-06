from object_class import Level

from property_class import ColorPool


from properties import ids

import json

with open("obj_ids.json","r") as file:
    all_ids = json.load(file)

pool = ObjectPool
    