import typed_argparse as tap

from . import deckbox


def main():
  tap.Parser(
      tap.SubParserGroup(
          tap.SubParser(
              'sleeved',
              tap.SubParserGroup(
                  tap.SubParser('portrait', deckbox.SleevedPortaitArgs),
                  tap.SubParser('landscape', deckbox.SleevedLandscapeArgs),
              ),
          ),
          tap.SubParser(
              'unsleeved',
              tap.SubParserGroup(
                  tap.SubParser('portrait', deckbox.UnsleevedPortraitArgs),
                  tap.SubParser('landscape', deckbox.UnsleevedLandscapeArgs),
              ),
          ),
          tap.SubParser(
              'custom',
              deckbox.CustomArgs,
          ),
      ),
  ).bind(
      deckbox.custom,
      deckbox.sleeved_landscape,
      deckbox.sleeved_portrait,
      deckbox.unsleeved_landscape,
      deckbox.unsleeved_portrait,
  ).run()
