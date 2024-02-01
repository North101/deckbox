import pathlib

import typed_argparse as tap

from deckbox.shared import *

from . import const, types


class CustomArgs(tap.TypedArgs, SVGArgs):
  output: pathlib.Path = tap.arg(
      default=const.OUTPUT,
      help='output path',
  )
  dimension: Dimension = tap.arg(
      action=types.NamedTupleAction,
      help='card dimensions [length] [width] [height] (mm)',
  )
  outer_thickness: float = tap.arg(
      type=types.positive_float,
      help='outer material thickness (mm)',
  )
  inner_thickness: float = tap.arg(
      type=types.positive_float,
      help='inner material thickness (mm)',
  )
  kerf: float = tap.arg(
      type=types.positive_float,
      help='kerf (mm)',
  )
  base_percent: float = tap.arg(
      type=types.percentage,
      default=const.BASE_PERCENT,
      help='base height as a percentage (0.0 - 1.0)',
  )
  tray_percent: float = tap.arg(
      type=types.percentage,
      default=const.TRAY_PERCENT,
      help='tray height as a percentage (0.0 - 1.0)',
  )
  tab: float = tap.arg(
      type=types.positive_float,
      default=const.TAB,
      help='tab size (mm)',
  )
  magnet_r: float = tap.arg(
      type=types.positive_float,
      help='magnet radius (mm)',
  )
  divider: bool = tap.arg(
      default=const.DIVIDER,
      help='divider (true/false)',
  )

  end_icon: Icon | None = tap.arg(
      default=None,
      action=types.NamedTupleAction,
  )
  top_icon: Icon | None = tap.arg(
      default=None,
      action=types.NamedTupleAction,
  )
  bottom_icon: Icon | None = tap.arg(
      default=None,
      action=types.NamedTupleAction,
  )

  side_icon: Icon | None = tap.arg(
      default=None,
      action=types.NamedTupleAction,
  )
  left_icon: Icon | None = tap.arg(
      default=None,
      action=types.NamedTupleAction,
  )
  right_icon: Icon | None = tap.arg(
      default=None,
      action=types.NamedTupleAction,
  )

  face_icon: Icon | None = tap.arg(
      default=None,
      action=types.NamedTupleAction,
  )
  front_icon: Icon | None = tap.arg(
      default=None,
      action=types.NamedTupleAction,
  )
  back_icon: Icon | None = tap.arg(
      default=None,
      action=types.NamedTupleAction,
  )


class UnsleevedPortraitArgs(CustomArgs):
  dimension: Dimension = tap.arg(
      action=types.NamedTupleAction,
      default=Dimension(const.UNSLEEVED_LENGTH, const.UNSLEEVED_WIDTH, const.UNSLEEVED_HEIGHT),
      help='card dimensions [length] [width] [height] (mm)',
  )


class UnsleevedLandscapeArgs(CustomArgs):
  dimension: Dimension = tap.arg(
      action=types.NamedTupleAction,
      default=Dimension(const.UNSLEEVED_HEIGHT, const.UNSLEEVED_WIDTH, const.UNSLEEVED_LENGTH),
      help='card dimensions [length] [width] [height] (mm)',
  )


class SleevedPortaitArgs(CustomArgs):
  dimension: Dimension = tap.arg(
      action=types.NamedTupleAction,
      default=Dimension(const.SLEEVED_LENGTH, const.SLEEVED_WIDTH, const.SLEEVED_HEIGHT),
      help='card dimensions [length] [width] [height] (mm)',
  )


class SleevedLandscapeArgs(CustomArgs):
  dimension: Dimension = tap.arg(
      action=types.NamedTupleAction,
      default=Dimension(const.SLEEVED_HEIGHT, const.SLEEVED_WIDTH, const.SLEEVED_LENGTH),
      help='card dimensions [length] [width] [height] (mm)',
  )
