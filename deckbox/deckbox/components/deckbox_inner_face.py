import pysvg
import pysvg_util as util
from pysvg import Element, path, svg

from ..args import CustomArgs


@util.register_svg()
class DeckboxInnerFace(util.SVGFile[CustomArgs]):
  def write(self, args: CustomArgs):
    length = args.dimension.length
    height = args.tray_height
    base_height = args.base_height

    top_path = util.h_pad(path.d([
        path.d.h(round(length / 3, 3) - 6),
        util.corner_radius_br(3, False),
        path.d.v(height - base_height - 6),
        util.corner_radius_br(3, True),
        path.placeholder(lambda w, h: path.d.h(length - w)),
        util.corner_radius_tl(3, True),
        -path.d.v(height - base_height - 6),
        util.corner_radius_tl(3, False),
        path.d.h(round(length / 3, 3) - 6),
    ]), args.inner_thickness)

    right_path = util.v_tabs(
        out=False,
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
        max_width=length,
        kerf=args.kerf,
        padding=args.inner_thickness,
    )

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

    return svg(
        attrs=svg.attrs(
            width=pysvg.length(d.width, 'mm'),
            height=pysvg.length(d.height, 'mm'),
            viewBox=(0, 0, d.width, d.height),
        ),
        children=children,
    )
