import pathlib

import pysvg
from pysvg import Element, path, svg

from .shared import *


@register_svg
def write_svg(args: SVGArgs):
  width = args.inner_width(False)
  height = args.tray_height
  base_height = args.base_height

  top_path = path.d([
      path.placeholder(lambda w, h: path.d.h((width - w) / 2)),
      path.d.v(round(height / 2, 3)),
      path.d.h(args.inner_thickness - (args.kerf * 6)),
      -path.d.v(round(height / 2, 3)),
      path.placeholder(lambda w, h: path.d.h((width - w) / 2)),
  ]) if args.divider else path.d.h(width)

  right_path = path.d([
      args.v_tab_half(args.tab),
      path.placeholder(lambda w, h: args.v_center(
          segment=lambda height: args.v_tabs(args.tab, height, True),
          v_length=(height - h),
      )),
      args.v_tab_half(args.tab),
  ])

  bottom_path = -path.d.h(width)

  left_path = -right_path

  d = path.d([
      path.d.m(args.inner_thickness, 0),
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
