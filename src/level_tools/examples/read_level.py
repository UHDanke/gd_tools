from level_tools.classes.level import Level

from level_tools.functions.level import LevelColor, per_chunk

level = Level.from_gmd("C:/Users/porum/Geometry Dash/library/gd_tools/data/gmd/P2 Memory Lane.gmd")

chunks = per_chunk(level.objects)