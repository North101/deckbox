import pathlib

from pysvg_util import types

OUTPUT = pathlib.Path('output')

BASE_PERCENT = 0.4
TRAY_PERCENT = 0.6
TAB = 5.0

DIVIDER = True

UNSLEEVED_LENGTH = types.PositiveFloat(64.0)
UNSLEEVED_WIDTH = types.PositiveFloat(35.0)
UNSLEEVED_HEIGHT = types.PositiveFloat(88.0)

SLEEVED_LENGTH = types.PositiveFloat(68.0)
SLEEVED_WIDTH = types.PositiveFloat(65.0)
SLEEVED_HEIGHT = types.PositiveFloat(93.0)
