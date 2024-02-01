import pathlib

import pysvg
from pysvg import Element, path, svg

from .shared import *


@register_svg
def write_svg(args: SVGArgs):
  length = args.inner_length(True)
  height = args.tray_height
  base_height = args.base_height

  top_path = path.d([
      path.d.h(round(length / 3, 3) - 6),
      args.corner_radius_right(3, True),
      path.d.v(height - base_height - 6),
      args.corner_radius_right(3, False),
      path.placeholder(lambda w, h: path.d.h(length - w)),
      args.corner_radius_left(3, False),
      -path.d.v(height - base_height - 6),
      args.corner_radius_left(3, True),
      path.d.h(round(length / 3, 3) - 6),
  ])

  right_path = path.d([
      args.v_tab_half(args.tab),
      path.placeholder(lambda w, h: args.v_center(
          segment=lambda height: args.v_tabs(args.tab, height, False),
          v_length=(height - h),
      )),
      args.v_tab_half(args.tab),
  ])

  bottom_path = -path.d.h(length)

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
      args.face_magnets(False),
  ]

  s = svg(
      attrs=svg.attrs(
          width=pysvg.length(d.width, 'mm'),
          height=pysvg.length(d.height, 'mm'),
          viewBox=(0, 0, d.width, d.height),
      ),
      children=children,
  )

  filename = pathlib.Path(__file__).with_suffix('.svg').name
  return args.output / filename, s
