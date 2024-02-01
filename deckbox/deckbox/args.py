import typed_argparse as tap
from pysvg import g, rect, transforms
from pysvg_util import args, types

from . import const


class CustomArgs(args.SVGArgs):
  dimension: types.Dimension = tap.arg(
      help='card dimensions [length] [width] [height] (mm)',
  )
  outer_thickness: float = tap.arg(
      type=types.PositiveFloat,
      help='outer material thickness (mm)',
  )
  inner_thickness: float = tap.arg(
      type=types.PositiveFloat,
      help='inner material thickness (mm)',
  )
  kerf: float = tap.arg(
      type=types.PositiveFloat,
      help='kerf (mm)',
  )
  base_percent: float = tap.arg(
      type=types.Percentage,
      default=const.BASE_PERCENT,
      help='base height as a percentage (0.0 - 1.0)',
  )
  tray_percent: float = tap.arg(
      type=types.Percentage,
      default=const.TRAY_PERCENT,
      help='tray height as a percentage (0.0 - 1.0)',
  )
  tab: float = tap.arg(
      type=types.PositiveFloat,
      default=const.TAB,
      help='tab size (mm)',
  )
  magnet: types.Size = tap.arg(
      type=types.Size,
      help='magnet radius (mm)',
  )
  divider: bool = tap.arg(
      default=const.DIVIDER,
      help='divider (true/false)',
  )

  image: types.Image | None = tap.arg(
      default=None,
  )

  end_image: types.Image | None = tap.arg(
      default=None,
  )
  top_image: types.Image | None = tap.arg(
      default=None,
  )
  bottom_image: types.Image | None = tap.arg(
      default=None,
  )

  side_image: types.Image | None = tap.arg(
      default=None,
  )
  left_image: types.Image | None = tap.arg(
      default=None,
  )
  right_image: types.Image | None = tap.arg(
      default=None,
  )

  face_image: types.Image | None = tap.arg(
      default=None,
  )
  front_image: types.Image | None = tap.arg(
      default=None,
  )
  back_image: types.Image | None = tap.arg(
      default=None,
  )

  images: list[types.Image] = tap.arg(
      default=[],
      nargs=2,
  )

  @property
  def base_height(self):
    return round(self.dimension.height * self.base_percent, 3)

  @property
  def lid_height(self):
    return self.dimension.height - self.base_height

  @property
  def tray_height(self):
    return round(self.dimension.height * self.tray_percent, 3)

  def inner_length(self, with_tabs: bool):
    if with_tabs:
      return self.dimension.length + (self.inner_thickness * 2)
    else:
      return self.dimension.length

  def inner_width(self, with_tabs: bool):
    if with_tabs:
      return self.dimension.width + (self.inner_thickness * 2)
    else:
      return self.dimension.width

  def outer_length(self, with_tabs: bool):
    if with_tabs:
      return self.inner_length(True) + (self.outer_thickness * 2)
    else:
      return self.inner_length(True)

  def outer_width(self, with_tabs: bool):
    if with_tabs:
      return self.inner_width(True) + (self.outer_thickness * 2)
    else:
      return self.inner_width(True)

  def magnet_x(self, outer: bool):
    if outer:
      x = self.outer_thickness
    else:
      x = 0
    return x + self.inner_thickness + self.magnet.width + 2

  def magnet_y(self, _: bool):
    return self.magnet.height + 2

  def magnets(self, cx: float, cy: float, width: float):
    magnet = self.magnet
    magnet_width = magnet.width - self.kerf
    magnet_height = magnet.height - self.kerf
    cx -= (magnet_width / 2)
    cy -= (magnet_height / 2)
    return g(attrs=g.attrs() | self.cut, children=[
        rect(attrs=rect.attrs(
            x=cx,
            y=cy,
            width=magnet_width,
            height=magnet_height,
        )),
        rect(attrs=rect.attrs(
            x=width - cx - magnet_width,
            y=cy,
            width=magnet_width,
            height=magnet_height,
        )),
        rect(attrs=rect.attrs(
            x=cx,
            y=cy + (magnet.height * 2),
            width=magnet_width,
            height=magnet_height,
        )),
        rect(attrs=rect.attrs(
            x=width - cx - magnet_width,
            y=cy + (magnet.height * 2),
            width=magnet_width,
            height=magnet_height,
        )),
    ])

  def face_magnets(self, outer: bool):
    width = self.outer_length(True) if outer else self.inner_length(True)
    y = self.dimension.height - self.tray_height + (self.outer_thickness * 2) if outer else self.outer_thickness
    return g(attrs=g.attrs(transform=transforms.translate(
        x=0,
        y=y - self.magnet_y(outer),
    )), children=[
        self.magnets(
            cx=self.magnet_x(outer),
            cy=self.magnet_y(outer),
            width=width,
        ),
    ])

  def side_magnets(self, outer: bool):
    width = self.outer_width(True) if outer else self.inner_width(True)
    y = self.base_height + (self.outer_thickness * 2) if outer else self.outer_thickness
    return g(attrs=g.attrs(transform=transforms.translate(
        x=0,
        y=y - self.magnet_y(outer),
    )), children=[
        self.magnets(
            cx=self.magnet_x(outer),
            cy=self.magnet_y(outer),
            width=width,
        ),
    ])


class UnsleevedPortraitArgs(CustomArgs):
  dimension: types.Dimension = tap.arg(
      default=types.Dimension(
          length=types.PositiveFloat(const.UNSLEEVED_LENGTH),
          width=types.PositiveFloat(const.UNSLEEVED_WIDTH),
          height=types.PositiveFloat(const.UNSLEEVED_HEIGHT),
      ),
      help='card dimensions [length] [width] [height] (mm)',
  )


class UnsleevedLandscapeArgs(CustomArgs):
  dimension: types.Dimension = tap.arg(
      default=types.Dimension(
          length=types.PositiveFloat(const.UNSLEEVED_HEIGHT),
          width=types.PositiveFloat(const.UNSLEEVED_WIDTH),
          height=types.PositiveFloat(const.UNSLEEVED_LENGTH),
      ),
      help='card dimensions [length] [width] [height] (mm)',
  )


class SleevedPortaitArgs(CustomArgs):
  dimension: types.Dimension = tap.arg(
      default=types.Dimension(
          length=types.PositiveFloat(const.SLEEVED_LENGTH),
          width=types.PositiveFloat(const.SLEEVED_WIDTH),
          height=types.PositiveFloat(const.SLEEVED_HEIGHT),
      ),
      help='card dimensions [length] [width] [height] (mm)',
  )


class SleevedLandscapeArgs(CustomArgs):
  dimension: types.Dimension = tap.arg(
      default=types.Dimension(
          length=types.PositiveFloat(const.SLEEVED_HEIGHT),
          width=types.PositiveFloat(const.SLEEVED_WIDTH),
          height=types.PositiveFloat(const.SLEEVED_LENGTH),
      ),
      help='card dimensions [length] [width] [height] (mm)',
  )
