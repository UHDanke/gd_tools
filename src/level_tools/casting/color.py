from level_tools.classes.hsv import HSV


ibool = lambda x: bool(int(x))


COLOR_TYPES = {
    1: int,
    2: int,
    3: int,
    4: int,
    5: ibool,
    6: int,
    7: float,
    8: ibool,
    9: int,
    10: HSV.from_string,
    11: int,
    12: int,
    13: int,
    14: float,
    15: float,
    16: float,
    17: float,
    18: ibool
    }