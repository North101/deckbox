import pysvg
import pysvg_util as util
from pysvg import Element, path, svg

from ..args import CustomArgs


@util.register_svg()
class DeckboxInnerSide(util.SVGFile[CustomArgs]):
  def write(self, args: CustomArgs):
    width = args.dimension.width
    height = args.tray_height

    divider_height = round(height / 4, 3)
    divider_thickness = args.inner_thickness - (args.kerf * 2)

    top_path = path.d([
        path.d.h((args.magnet.width + 1) * 2),
        path.placeholder(lambda w, h: util.h_center(
            segment=lambda width: path.d([
                util.h_tabs(
                    out=False,
                    thickness=divider_height,
                    tab=divider_thickness,
                    gap=divider_thickness,
                    max_width=width,
                    padding=args.tab / 2,
                    kerf=args.kerf,
                ),
            ]),
            width=(width - w),
        )),
        path.d.h((args.magnet.width + 1) * 2),
    ]) if args.divider else path.d.h(width)
    right_path = util.v_tabs(
        out=True,
        thickness=args.inner_thickness,
        tab=args.tab,
        gap=args.tab,
        max_height=height,
        kerf=args.kerf,
    )
    bottom_path = -util.h_tabs(
        out=True,
        thickness=args.outer_thickness,
        tab=args.tab,
        gap=args.tab,
        max_width=width,
        kerf=args.kerf,
    )

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
        args.side_magnets(False),
    ]

    return svg(
        attrs=svg.attrs(
            width=pysvg.length(d.width, 'mm'),
            height=pysvg.length(d.height, 'mm'),
            viewBox=(0, 0, d.width, d.height),
        ),
        children=children,
    )
