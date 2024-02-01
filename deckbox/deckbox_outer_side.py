import enum
import functools
import pathlib

import pysvg
from pysvg import Element, path, svg

from .shared import *


class Side(enum.Enum):
  RIGHT = enum.auto()
  LEFT = enum.auto()


def write_svg(args: SVGArgs, side: Side):
  width = args.outer_width(False)
  lid_height = args.lid_height
  base_height = args.base_height

  top_path = path.d([
      args.h_tab_half(args.tab),
      path.placeholder(lambda w, h: args.h_center(
          segment=lambda width: args.h_tabs(args.tab, width, True),
          h_length=width - w,
      )),
      args.h_tab_half(args.tab),
  ])

  right_path = path.d([
      path.d([
          args.v_tab_half(args.tab),
          path.placeholder(lambda w, h: args.v_center(
              segment=lambda height: args.v_tabs(args.tab, height, True),
              v_length=lid_height - h,
          )),
          args.v_tab_half(args.tab),
      ]),
      path.d([
          args.v_tab_half(args.tab),
          path.placeholder(lambda w, h: args.v_center(
              segment=lambda height: args.v_tabs(args.tab, height, True),
              v_length=base_height - h,
          )),
          args.v_tab_half(args.tab),
      ]),
  ])

  bottom_path = -top_path

  left_path = -path.d([
      path.d([
          args.v_tab_half(args.tab),
          path.placeholder(lambda w, h: args.v_center(
              segment=lambda height: args.v_tabs(args.tab, height, True),
              v_length=base_height - h,
          )),
          args.v_tab_half(args.tab),
      ]),
      path.d([
          args.v_tab_half(args.tab),
          path.placeholder(lambda w, h: args.v_center(
              segment=lambda height: args.v_tabs(args.tab, height, True),
              v_length=lid_height - h,
          )),
          args.v_tab_half(args.tab),
      ]),
  ])

  d = path.d([
      path.d.m(args.outer_thickness, args.outer_thickness),
      top_path,
      right_path,
      bottom_path,
      left_path,
  ])

  children: list[Element | str] = [
      path(attrs=path.attrs(
          d=d,
      ) | args.cut),
      path(attrs=path.attrs(
          d=path.d([
              path.d.m(args.outer_thickness, args.outer_thickness + lid_height),
              path.d.h(width),
          ]),
      ) | args.cut),
  ]

  if side is Side.RIGHT and args.right_icon:
    children.append(args.icon(
        d=d,
        icon=args.right_icon,
    ))
  elif side is Side.LEFT and args.left_icon:
    children.append(args.icon(
        d=d,
        icon=args.left_icon,
    ))
  elif args.side_icon:
    children.append(args.icon(
        d=d,
        icon=args.side_icon,
    ))

  s = svg(
      attrs=svg.attrs(
          width=pysvg.length(d.width, 'mm'),
          height=pysvg.length(d.height, 'mm'),
          viewBox=(0, 0, d.width, d.height),
      ),
      children=children,
  )

  stem = pathlib.Path(__file__).stem
  filename = pathlib.Path(f'{stem}_{side.name.lower()}').with_suffix('.svg').name
  return args.output / filename, s


for side in Side:
  register_svg(functools.partial(write_svg, side=side))
