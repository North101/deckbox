import enum

import pysvg
import pysvg_util as util
from pysvg import Element, path, svg

from ..args import CustomArgs


class Face(enum.Enum):
  FRONT = enum.auto()
  BACK = enum.auto()


@util.register_svg_variants(Face)
class DeckboxOuterFace(util.VariantSVGFile[CustomArgs, Face]):
  def write(self, args: CustomArgs):
    length = args.dimension.length
    lid_height = args.lid_height
    base_height = args.base_height

    top_path = util.h_tabs(
        out=True,
        thickness=args.outer_thickness,
        tab=args.tab,
        gap=args.tab,
        max_width=length,
        kerf=args.kerf,
        padding=args.inner_thickness + args.outer_thickness,
    )

    b_height = ((base_height - args.tab) // (args.tab * 2) * (args.tab * 2)) + args.tab
    l_height = ((lid_height - args.tab) // (args.tab * 2) * (args.tab * 2)) + args.tab
    right_path = path.d([
        path.d.v(lid_height - l_height),
        util.v_tabs(
            out=False,
            thickness=args.outer_thickness,
            tab=args.tab,
            gap=args.tab,
            max_height=l_height,
            kerf=args.kerf,
        ),
        util.v_tabs(
            out=False,
            thickness=args.outer_thickness,
            tab=args.tab,
            gap=args.tab,
            max_height=b_height,
            kerf=args.kerf,
        ),
        path.d.v(base_height - b_height),
    ])

    bottom_path = -top_path

    left_path = -path.d([
        path.d.v(base_height - b_height),
        util.v_tabs(
            out=False,
            thickness=args.outer_thickness,
            tab=args.tab,
            gap=args.tab,
            max_height=b_height,
            kerf=args.kerf,
        ),
        util.v_tabs(
            out=False,
            thickness=args.outer_thickness,
            tab=args.tab,
            gap=args.tab,
            max_height=l_height,
            kerf=args.kerf,
        ),
        path.d.v(lid_height - l_height),
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
                path.d.h(args.outer_length(True)),
            ]),
        ) | args.cut),
        args.face_magnets(True),
    ]

    if self.variant is Face.FRONT and args.front_image:
      image = args.front_image
    elif self.variant is Face.BACK and args.back_image:
      image = args.back_image
    else:
      image = args.face_image or args.image

    if image:
      children.append(util.engrave_image(
          parent=d,
          image=image,
          engrave=args.engrave,
      ))

    return svg(
        attrs=svg.attrs(
            width=pysvg.length(d.width, 'mm'),
            height=pysvg.length(d.height, 'mm'),
            viewBox=(0, 0, d.width, d.height),
        ),
        children=children,
    )
