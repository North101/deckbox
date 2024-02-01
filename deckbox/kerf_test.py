import pathlib

from pysvg import length, path, svg

from .shared import *


@register_svg
def write_svg(args: SVGArgs):
  tab = 5

  tab_out = path.d([
      path.d.m(0, 0),
      path.d.h(10),
      args.v_tab_half(tab),
      args.v_tab(tab, True),
      args.v_tab(tab, True),
      args.v_tab_half(tab),
      -path.d.h(10),
      -path.placeholder(lambda w, h: path.d.v(h)),
  ])

  tab_in = path.d([
      path.d.m(10 + args.tab + 2, 0),
      path.d.h(10),
      args.v_tab_half(tab),
      args.v_tab(tab, False),
      args.v_tab(tab, False),
      args.v_tab_half(tab),
      -path.d.h(10),
      -path.placeholder(lambda w, h: path.d.v(h)),
  ])

  d = path.d([
      tab_out,
      tab_in,
  ])

  s = svg(
      attrs=svg.attrs(
          width=length(d.width, 'mm'),
          height=length(d.height, 'mm'),
          viewBox=(0, 0, d.width, d.height),
      ),
      children=[
          path(attrs=path.attrs(
              d=d,
          ) | args.cut),
          args.magnets(
              cx=5,
              cy=d.height / 2,
              width=d.width,
              height=0,
          ),
      ]
  )

  filename = args.output / pathlib.Path(__file__).with_suffix('.svg').name
  return filename, s
