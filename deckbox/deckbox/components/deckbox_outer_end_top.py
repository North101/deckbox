import pysvg
import pysvg_util as util
from pysvg import Element, path, svg

from ..args import CustomArgs


@util.register_svg()
class DeckboxOuterEndTop(util.SVGFile[CustomArgs]):
  def write(self, args: CustomArgs):
    length = args.outer_length(False)
    width = args.inner_width(False)

    top_path = util.h_tabs(
        out=False,
        thickness=args.outer_thickness,
        tab=args.tab,
        gap=args.tab,
        max_width=length,
        kerf=args.kerf,
        padding=args.outer_thickness,
    )
    right_path = util.v_center(lambda x: util.v_tabs(
        out=False,
        thickness=args.outer_thickness,
        tab=args.tab,
        gap=args.tab,
        max_height=width,
        kerf=args.kerf,
        padding=args.outer_thickness,
    ), height=args.outer_width(True))
    bottom_path = -top_path
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
    ]

    if args.top_image:
      image = args.top_image
    else:
      image = args.end_image or args.image

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
