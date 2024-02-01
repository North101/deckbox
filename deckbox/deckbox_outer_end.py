import enum
import functools
import pathlib

import pysvg
from pysvg import Element, path, svg

from .shared import *


class End(enum.Enum):
  TOP = enum.auto()
  BOTTOM = enum.auto()


def write_svg(args: SVGArgs, end: End):
  length = args.outer_length(True)
  width = args.outer_width(True)

  top_path = path.d([
      path.d.h(args.outer_thickness),
      args.h_tab_half(args.tab),
      path.placeholder(lambda w, h: args.h_center(
          segment=lambda length: args.h_tabs(args.tab, length, False),
          h_length=length - w,
      )),
      args.h_tab_half(args.tab),
      path.d.h(args.outer_thickness),
  ])

  right_path = path.d([
      path.d.v(args.outer_thickness),
      args.v_tab_half(args.tab),
      path.placeholder(lambda w, h: args.v_center(
          segment=lambda width: args.v_tabs(args.tab, width, False),
          v_length=width - h,
      )),
      args.v_tab_half(args.tab),
      path.d.v(args.outer_thickness),
  ])

  bottom_path = -top_path

  left_path = -right_path

  d = path.d([
      path.d.m(0, 0),
      top_path,
      right_path,
      bottom_path,
      left_path,
  ])

  children: list[Element | str] = [
      path(attrs=path.attrs(
          d=d,
      ) | args.cut),
  ]

  if end is end.TOP and args.top_icon:
    children.append(args.icon(
        d=d,
        icon=args.top_icon,
    ))
  elif end is end.BOTTOM and args.bottom_icon:
    children.append(args.icon(
        d=d,
        icon=args.bottom_icon,
    ))
  elif args.end_icon:
    children.append(args.icon(
        d=d,
        icon=args.end_icon,
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
  filename = pathlib.Path(f'{stem}_{end.name.lower()}').with_suffix('.svg').name
  return args.output / filename, s


for end in End:
  register_svg(functools.partial(write_svg, end=end))
