import pathlib

import pysvg
from pysvg import Element, path, svg

from .shared import *


@register_svg
def write_svg(args: SVGArgs):
  length = args.inner_length(False)
  height = args.tray_height
  base_height = args.base_height

  top_path = path.d([
      path.d.h(round(length / 3, 3) - 6),
      args.corner_radius_right(3, True),
      path.d.v(height - base_height - 3),
      args.corner_radius_right(3, False),
      path.placeholder(lambda w, h: path.d.h(length - w)),
      args.corner_radius_left(3, False),
      -path.d.v(height - base_height - 3),
      args.corner_radius_left(3, True),
      path.d.h(round(length / 3, 3) - 6),
  ])

  right_path = path.d([
      path.d.h(args.inner_thickness),
      path.d.v(round(height / 2, 3)),
      -path.d.h(args.inner_thickness),
      path.placeholder(lambda w, h: path.d.v(height - h)),
  ])

  bottom_path = -path.d.h(length)

  left_path = -path.d([
      path.placeholder(lambda w, h: path.d.v(height - h)),
      path.d.h(args.inner_thickness),
      path.d.v(round(height / 2, 3)),
      -path.d.h(args.inner_thickness),
  ])

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
