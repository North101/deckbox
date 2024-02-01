import pysvg_util as util
from pysvg import length, path, svg

from ..args import CustomArgs


@util.register_svg()
class KerfTest(util.SVGFile[CustomArgs]):
  def write(self, args: CustomArgs):
    tab = 5

    tab_out = path.d([
        path.d.m(0, 0),
        path.d.h(10),
        util.v_tabs(
            out=True,
            thickness=args.outer_thickness,
            tab=tab,
            gap=tab,
            max_height=tab * 3,
            kerf=args.kerf,
        ),
        -path.d.h(10),
        -path.placeholder(lambda w, h: path.d.v(h)),
    ])

    tab_in = path.d([
        path.d.m(10 + args.tab + 2, 0),
        path.d.h(10),
        util.v_tabs(
            out=False,
            thickness=args.outer_thickness,
            tab=tab,
            gap=tab,
            max_height=tab * 3,
            kerf=args.kerf,
        ),
        -path.d.h(10),
        -path.placeholder(lambda w, h: path.d.v(h)),
    ])

    d = path.d([
        tab_out,
        tab_in,
    ])

    return svg(
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
                cy=5,
                width=args.magnet.width,
            ),
        ]
    )
