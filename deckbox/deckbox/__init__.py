import pysvg_util as util

from .args import (
    CustomArgs,
    SleevedLandscapeArgs,
    SleevedPortaitArgs,
    UnsleevedLandscapeArgs,
    UnsleevedPortraitArgs,
)
from .components import *


def custom(args: CustomArgs):
  return util.write_svgs(util.generate_svgs(args))


def sleeved_landscape(args: SleevedLandscapeArgs):
  return util.write_svgs(util.generate_svgs(args))


def sleeved_portrait(args: SleevedPortaitArgs):
  return util.write_svgs(util.generate_svgs(args))


def unsleeved_landscape(args: UnsleevedLandscapeArgs):
  return util.write_svgs(util.generate_svgs(args))


def unsleeved_portrait(args: UnsleevedPortraitArgs):
  return util.write_svgs(util.generate_svgs(args))
