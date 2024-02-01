import pysvg
import pysvg_util as util
from pysvg import Element, path, svg

from ..args import CustomArgs


@util.register_svg()
class DeckboxInnerDivider(util.SVGFile[CustomArgs]):
  def write(self, args: CustomArgs):
    length = args.dimension.length
    height = args.tray_height
    base_height = args.base_height

    top_path = path.d([
        path.d.h(round(length / 3, 3) - 6),
        util.corner_radius_br(3, False),
        path.d.v(height - base_height - 3),
        util.corner_radius_br(3, True),
        path.placeholder(lambda w, h: path.d.h(length - w)),
        util.corner_radius_tl(3, True),
        -path.d.v(height - base_height - 3),
        util.corner_radius_tl(3, False),
        path.d.h(round(length / 3, 3) - 6),
    ])

    right_path = path.d([
        path.d.h(args.inner_thickness),
        path.d.v(round(height / 4, 3)),
        -path.d.h(args.inner_thickness),
        path.placeholder(lambda w, h: path.d.v(height - h)),
    ])

    bottom_path = -path.d.h(length)

    left_path = -path.d([
        path.placeholder(lambda w, h: path.d.v(height - h)),
        path.d.h(args.inner_thickness),
        path.d.v(round(height / 4, 3)),
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

    return svg(
        attrs=svg.attrs(
            width=pysvg.length(d.width, 'mm'),
            height=pysvg.length(d.height, 'mm'),
            viewBox=(0, 0, d.width, d.height),
        ),
        children=children,
    )
