import math
import pathlib
from typing import Callable, NamedTuple, Protocol

from pysvg import PresentationAttributes, circle, g, path, svg, transforms
from pysvg.attributes.presentation import DrawSegment


class Dimension(NamedTuple):
  length: float
  width: float
  height: float


class Icon(NamedTuple):
  path: pathlib.Path
  width: float
  height: float
  scale: float


class SVGArgs:
  output: pathlib.Path
  dimension: Dimension
  outer_thickness: float
  inner_thickness: float
  kerf: float
  base_percent: float
  tray_percent: float
  tab: float
  magnet_r: float
  divider: bool

  end_icon: Icon
  top_icon: Icon
  bottom_icon: Icon

  side_icon: Icon
  left_icon: Icon
  right_icon: Icon

  face_icon: Icon
  front_icon: Icon
  back_icon: Icon

  def h_tab_half(self, tab):
    return path.d.h(tab / 2)

  def h_tab(self, tab: float, out: bool):
    kerf = -self.kerf if out else self.kerf
    thickness = -path.d.v(self.outer_thickness) if out else path.d.v(self.outer_thickness)
    return path.d([
        path.d.h((tab / 2) + kerf),
        thickness,
        path.d.h(tab + -kerf + -kerf),
        -thickness,
        path.d.h(kerf + (tab / 2)),
    ])

  def h_tabs(self, tab: float, length: float, out: bool):
    h_tab = self.h_tab(tab, out)
    count = math.floor(length / h_tab.width)
    return path.d([
        h_tab
        for _ in range(count)
    ])

  def v_tab_half(self, tab):
    return path.d.v(tab / 2)

  def v_tab(self, tab: float, out: bool):
    kerf = -self.kerf if out else self.kerf
    thickness = -path.d.h(self.outer_thickness) if out else path.d.h(self.outer_thickness)
    return path.d([
        path.d.v((tab / 2) + kerf),
        -thickness,
        path.d.v(tab + -kerf + -kerf),
        thickness,
        path.d.v(kerf + (tab / 2)),
    ])

  def v_tabs(self, tab: float, height: float, out: bool):
    v_tab = self.v_tab(tab, out)
    count = math.floor(height / v_tab.height)
    return path.d([
        v_tab
        for _ in range(count)
    ])

  def h_slot(self, tab: float):
    kerf = self.kerf
    thickness = path.d.v(self.outer_thickness)
    return path.d([
        path.d.m((tab / 2) + kerf, 0),
        thickness,
        path.d.h(tab + -kerf + -kerf),
        -thickness,
        -path.d.h(tab + -kerf + -kerf),
        path.d.m(tab + -kerf + -kerf, 0),
        path.d.m(kerf + (tab / 2), 0),
    ])

  def h_slots(self, tab: float, width: float):
    h_slot = self.h_slot(tab)
    count = math.floor(width / h_slot.width)
    return path.d([
        h_slot
        for _ in range(count)
    ])

  def v_slot(self, tab: float):
    kerf = self.kerf
    thickness = path.d.h(self.outer_thickness)
    return path.d([
        path.d.m(0, (tab / 2) + kerf),
        thickness,
        path.d.v(tab + -kerf + -kerf),
        -thickness,
        -path.d.v(tab + -kerf + -kerf),
        path.d.m(0, tab + -kerf + -kerf),
        path.d.m(0, kerf + (tab / 2)),
    ])

  def v_slots(self, tab: float, height: float):
    v_slot = self.v_slot(tab)
    count = math.floor(height / v_slot.height)
    return path.d([
        v_slot
        for _ in range(count)
    ])

  def h_center(self, segment: Callable[[float], DrawSegment], h_length: float):
    return path.d([
        path.placeholder(lambda w, h: path.d.h((h_length - w) / 2)),
        segment(h_length),
        path.placeholder(lambda w, h: path.d.h((h_length - w) / 2)),
    ])

  def v_center(self, segment: Callable[[float], DrawSegment], v_length: float):
    return path.d([
        path.placeholder(lambda w, h: path.d.v((v_length - h) / 2)),
        segment(v_length),
        path.placeholder(lambda w, h: path.d.v((v_length - h) / 2)),
    ])

  def icon(self, d: path.d, icon: Icon):
    contain_scale = min(d.width / icon.width, d.height / icon.height)
    width = icon.width * contain_scale * icon.scale
    height = icon.height * contain_scale * icon.scale
    return g(
        attrs=g.attrs(transform=[
            transforms.translate(
                x=(d.width - width) / 2,
                y=(d.height - height) / 2,
            ),
            transforms.scale(contain_scale),
            transforms.scale(icon.scale),
        ]) | self.engrave,
        children=[
            icon.path.read_text().strip(),
        ],
    )

  @property
  def base_height(self):
    return round(self.dimension.height * self.base_percent, 3)

  @property
  def lid_height(self):
    return self.dimension.height - self.base_height

  @property
  def tray_height(self):
    return round(self.dimension.height * self.tray_percent, 3)

  def inner_length(self, with_tabs: bool):
    if with_tabs:
      return self.dimension.length + (self.inner_thickness * 2)
    else:
      return self.dimension.length

  def inner_width(self, with_tabs: bool):
    if with_tabs:
      return self.dimension.width + (self.inner_thickness * 2)
    else:
      return self.dimension.width

  def outer_length(self, with_tabs: bool):
    if with_tabs:
      return self.inner_length(True) + (self.outer_thickness * 2)
    else:
      return self.inner_length(True)

  def outer_width(self, with_tabs: bool):
    if with_tabs:
      return self.inner_width(True) + (self.outer_thickness * 2)
    else:
      return self.inner_width(True)

  def magnet_cx(self, outer: bool):
    if outer:
      x = self.outer_thickness
    else:
      x = 0
    return x + self.inner_thickness + (self.magnet_r * 2)

  def magnet_cy(self, outer: bool):
    if outer:
      y = 0
    else:
      y = 0
    return y + (self.magnet_r * 2)

  def magnets(self, cx: float, cy: float, width: float, height: float):
    r = self.magnet_r - self.kerf - self.kerf
    return g(attrs=g.attrs() | self.cut, children=[
        circle(attrs=circle.attrs(
            cx=cx,
            cy=cy,
            r=r,
        )),
        circle(attrs=circle.attrs(
            cx=width - cx,
            cy=cy,
            r=r,
        )),
        circle(attrs=circle.attrs(
            cx=cx,
            cy=height - cy,
            r=r,
        )),
        circle(attrs=circle.attrs(
            cx=width - cx,
            cy=height - cy,
            r=r,
        )),
    ])

  def face_magnets(self, outer: bool):
    width = self.outer_length(True) if outer else self.inner_length(True)
    height = self.tray_height - self.base_height
    return g(attrs=g.attrs(transform=transforms.translate(
        x=0,
        y=self.base_height + self.outer_thickness if outer else 0,
    )), children=[
        self.magnets(
            cx=self.magnet_cx(outer),
            cy=self.magnet_cy(outer),
            width=width,
            height=height,
        ),
        self.magnets(
            cx=self.magnet_cx(outer) + (self.magnet_r * 3),
            cy=self.magnet_cy(outer),
            width=width,
            height=height,
        ),
    ])

  def side_magnets(self, outer: bool):
    width = self.outer_length(True) if outer else self.inner_length(True)
    height = self.tray_height - self.base_height
    return g(attrs=g.attrs(transform=transforms.translate(
        x=0,
        y=self.base_height + self.outer_thickness if outer else 0,
    )), children=[
        self.magnets(
            cx=self.magnet_cx(outer),
            cy=self.magnet_cy(outer),
            width=width,
            height=height,
        ),
    ])

  def corner_radius_right(self, r: float, invert: bool):
    return path.d.a(r, r, 0, False, invert, r, r)

  def corner_radius_left(self, r: float, invert: bool):
    return path.d.a(r, r, 0, False, invert, r, -r)

  cut = PresentationAttributes(
      fill='none',
      stroke='black',
      stroke_width=0.001,
  )

  engrave = PresentationAttributes(
      fill='black',
      stroke='none',
      stroke_width=0.001,
  )


class RegisterSVGCallable(Protocol):
  def __call__(self, args: SVGArgs) -> tuple[pathlib.Path, svg]:
    ...


svg_list: list[RegisterSVGCallable] = []


def register_svg(f: RegisterSVGCallable):
  svg_list.append(f)
  return f


def write_all_svg(args: SVGArgs):
  args.output.mkdir(parents=True, exist_ok=True)
  data = [
      write_svg(args)
      for write_svg in svg_list
  ]
  for (filename, svg_data) in data:
    filename.write_text(format(svg_data, '.3f'))

  return data
