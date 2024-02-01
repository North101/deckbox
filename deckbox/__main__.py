import typed_argparse as tap

from .args import *
from .shared import *


def main(args: tap.TypedArgs):
  if not isinstance(args, SVGArgs):
    raise ValueError(args)

  svgs = write_all_svg(args)
  data = [
      (str(filename), svg.attrs.width, svg.attrs.height)
      for (filename, svg) in svgs
  ]
  name_len = max(len(name) for (name, _, _) in data)
  length_len = max(len(f'{length:.2f}') for (_, length, _) in data)
  height_len = max(len(f'{height:.2f}') for (_, _, height) in data)
  for (name, length, height) in data:
    print(f'{name:<{name_len}} @ {length:>{length_len}.2f} x {height:>{height_len}.2f}')


if __name__ == '__main__':
  args = tap.Parser(
      tap.SubParserGroup(
          tap.SubParser(
              'sleeved',
              tap.SubParserGroup(
                  tap.SubParser('portrait', SleevedPortaitArgs),
                  tap.SubParser('landscape', SleevedLandscapeArgs),
              ),
          ),
          tap.SubParser(
              'unsleeved',
              tap.SubParserGroup(
                  tap.SubParser('portrait', UnsleevedPortraitArgs),
                  tap.SubParser('landscape', UnsleevedLandscapeArgs),
              ),
          ),
          tap.SubParser(
              'custom',
              CustomArgs,
          ),
      ),
  ).parse_args()
  main(args)
