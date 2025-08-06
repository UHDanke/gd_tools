from object_class import Level, Object

level = Level.gmd_load(r"D:\Downloads\new hole.gmd")

pool = level.objects

start = level.init



new_pool = pool.copy()

from object_functions import clean_gid_parents

new_pool.apply(clean_gid_parents)


del new_pool[100:1250]


