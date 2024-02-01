import enum
import functools
import pathlib

import pysvg
from pysvg import Element, path, svg

from .shared import *


class Face(enum.Enum):
  FRONT = enum.auto()
  BACK = enum.auto()


def write_svg(args: SVGArgs, face: Face):
  length = args.outer_length(True)
  lid_height = args.lid_height
  base_height = args.base_height

  top_path = path.d([
      path.d.h(args.outer_thickness),
      args.h_tab_half(args.tab),
      path.placeholder(lambda w, h: args.h_center(
          segment=lambda length: args.h_tabs(args.tab, length, True),
          h_length=length - w,
      )),
      args.h_tab_half(args.tab),
      path.d.h(args.outer_thickness),
  ])

  right_path = path.d([
      path.d([
          args.v_tab_half(args.tab),
          path.placeholder(lambda w, h: args.v_center(
              segment=lambda height: args.v_tabs(args.tab, height, False),
              v_length=lid_height - h,
          )),
          args.v_tab_half(args.tab),
      ]),
      path.d([
          args.v_tab_half(args.tab),
          path.placeholder(lambda w, h: args.v_center(
              segment=lambda height: args.v_tabs(args.tab, height, False),
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
              segment=lambda height: args.v_tabs(args.tab, height, False),
              v_length=base_height - h,
          )),
          args.v_tab_half(args.tab),
      ]),
      path.d([
          args.v_tab_half(args.tab),
          path.placeholder(lambda w, h: args.v_center(
              segment=lambda height: args.v_tabs(args.tab, height, False),
              v_length=lid_height - h,
          )),
          args.v_tab_half(args.tab),
      ]),
  ])

  d = path.d([
      path.d.m(0, args.outer_thickness),
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
              path.d.m(0, args.outer_thickness + lid_height),
              path.d.h(length),
          ]),
      ) | args.cut),
      args.face_magnets(True),
  ]
  if face is Face.FRONT and args.front_icon:
    children.append(args.icon(
        d=d,
        icon=args.front_icon,
    ))
  elif face is Face.BACK and args.back_icon:
    children.append(args.icon(
        d=d,
        icon=args.back_icon,
    ))
  elif args.face_icon:
    children.append(args.icon(
        d=d,
        icon=args.face_icon,
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
  filename = pathlib.Path(f'{stem}_{face.name.lower()}').with_suffix('.svg').name
  return args.output / filename, s


for face in Face:
  register_svg(functools.partial(write_svg, face=face))
