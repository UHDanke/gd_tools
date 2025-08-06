# -*- coding: utf-8 -*-
from object_class import Level

from properties import ids

level = Level.gmd_load('color_test.gmd')

colors = level.start[ids.level.colors]

#color_ids = colors.unique_values(lambda color: color.color_id)