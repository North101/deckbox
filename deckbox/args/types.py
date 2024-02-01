import argparse
import pathlib
from gettext import gettext
from typing import Any, Sequence


def svg_file_exists(value: str):
  path = pathlib.Path(value)
  if not path.is_file() or path.suffix != '.svg':
    raise ValueError()

  return path


def positive_float(value: str):
  float_value = float(value)
  if float_value < 0.0:
    raise ValueError()

  return float_value


def percentage(value: str, min=0.0, max=1.0):
  percent_value = float(value)
  if not (min <= percent_value <= max):
    raise ValueError()

  return percent_value


def is_NamedTuple(obj) -> bool:
  return (
      tuple in obj.__bases__ and
      hasattr(obj, '_fields') and
      hasattr(obj, '__annotations__')
  )


class NamedTupleAction(argparse.Action):
  def __init__(self, option_strings: list[str], dest: str, type: Any, nargs=None, metavar=None, **kwargs):
    assert is_NamedTuple(type), f'{type} is not a NamedTuple'
    assert nargs is None, 'nargs is not None'
    assert metavar is None, 'metavar is not None'

    metavar = tuple((
        field.upper()
        for field in type._fields
    ))
    super().__init__(option_strings, dest, type=None, nargs=len(metavar), metavar=metavar, **kwargs)

    self._type = type

  def field_type_at_index(self, index: int):
    field = self._type._fields[index]
    return self._type.__annotations__[field]

  def parse_value(self, index: int, value: str):
    subtype = self.field_type_at_index(index)
    try:
      return subtype(value)
    except (TypeError, ValueError):
      name = getattr(subtype, '__name__', repr(subtype))
      args = {'type': name, 'value': value}
      msg = gettext('invalid %(type)s value: %(value)r')
      raise argparse.ArgumentError(self, msg % args)

  def parse_values(self, values: Sequence[str]):
    return self._type(*(
        self.parse_value(i, value)
        for i, value in enumerate(values)
    ))

  def __call__(self, parser, namespace, values, option_string=None):
    if not isinstance(values, list):
      raise ValueError(values)

    setattr(namespace, self.dest, self.parse_values(values))
