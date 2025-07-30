from typing import Union, Callable, Any, TypeVar

import inspect
import os

import yaml
from omegaconf import OmegaConf

from .utils import indent_second

__all__ = [
  'gearup',
  'apply',
]

T = TypeVar('T')

def apply(f: Callable[..., T]) -> Callable[..., T]:
  """
  Applies function `f` to the provided arguments and keyword arguments,
  ignoring keyword arguments that are not accepted by the function.

  Note: positional arguments `args` are always passed to the function.
  """
  def call(*args, **kwargs) -> T:
    signature = inspect.signature(f)

    passed_kwargs = dict()

    for name, p in signature.parameters.items():
      if p.kind == inspect.Parameter.POSITIONAL_ONLY:
        pass

      elif p.kind == inspect.Parameter.VAR_POSITIONAL:
        pass

      elif p.kind == inspect.Parameter.VAR_KEYWORD:
        ### function accepts everything
        return f(*args, **kwargs)

      elif name in kwargs:
        passed_kwargs[name] = kwargs[name]

    return f(*args, **passed_kwargs)

  return call

class cli_function(object):
  def __init__(self, f, helper: Union[None, str]=None, config: Union[None, bytes, str, os.PathLike]=None):
    self.f = f
    self.helper = helper
    self.config = config

  def help(self):
    doc: Union[None, str] = getattr(self.f, '__doc__', None)
    signature = str(inspect.signature(self.f))

    if doc is None:
      return f'{signature}'
    else:
      return f'{signature}\n{inspect.cleandoc(doc)}'

  def short_help(self):
    doc = getattr(self.f, '__doc__', None)
    signature = str(inspect.signature(self.f))

    if doc is None:
      return str(inspect.signature(self.f))
    else:
      header, *_ = inspect.cleandoc(doc).split('\n\n', maxsplit=1)

      return f'{signature}\n{header.strip()}'

  def __call__(self, arguments=None):
    from .config import read_config

    if arguments is None:
      import sys
      arguments = sys.argv[1:]

    if len(arguments) == 1:
      if self.helper is not None and arguments[0] == self.helper:
        print(self.help())
        return

    args, kwargs = read_config(arguments, self.config)

    return apply(self.f)(*args, **kwargs)

class cli_commands(object):
  def __init__(self, commands, helper: Union[None, str], config: Union[None, bytes, str, os.PathLike]):
    self.commands = commands
    self.helper = helper
    self.config = config

  def signature(self):
    return '\n'.join(
      '%s -> %s' % (k, indent_second(v.short_help(), len(k) + 4))
      for k, v in self.commands.items()
    )

  def help(self):
    return (f'Available commands:\n'
            f'{self.signature()}')

  def short_help(self):
    return self.signature()

  def __call__(self, arguments=None):
    if arguments is None:
      import sys
      arguments = sys.argv[1:]

    if len(arguments) == 0:
      raise ValueError(
        f'please, specify command.\n'
        f'{self.help()}'
      )

    if len(arguments) == 1:
      if self.helper is not None and arguments[0] == self.helper:
        print(self.help())
        return

    command = arguments[0]
    if command not in self.commands:
      raise ValueError(
        f'invalid command {command}.\n'
        f'{self.help()}'
      )

    return self.commands[command](arguments[1:])

def compose(
  functions,
  named_functions,
  helper: Union[None, str]='help',
  config: Union[None, bytes, str, os.PathLike]=None
):
  if len(named_functions) == 0 and len(functions) == 0:
    raise ValueError('A function or dictionary of functions must be supplied!')

  if len(named_functions) == 0 and len(functions) == 1:
    return cli_function(functions[0], helper=helper, config=config)

  commands = dict()

  for function in functions:
    if hasattr(function, '__name__') and callable(function):
      name = function.__name__
      if name in commands:
        raise ValueError('duplicated command names (%s)' % (name,))
      else:
        commands[name] = cli_function(function, helper=helper, config=config)

    else:
      raise ValueError(
        f'non-keyword arguments must be callables and have `__name__` attribute (like all functions). '
        f'Got {function}'
      )

  for name, function in named_functions.items():
    if name in commands:
      raise ValueError('duplicated command names (%s)' % (name,))

    if isinstance(function, (list, tuple)):
      commands[name] = compose(function, dict(), helper=helper, config=config)
    elif isinstance(function, (dict,)):
      commands[name] = compose((), function, helper=helper, config=config)
    elif callable(function):
      commands[name] = cli_function(function, helper=helper, config=config)
    else:
      raise ValueError(
        f'command {name}={function} is not understood, must be either a callable, a tuple/list or a dict.'
      )

  return cli_commands(commands, helper=helper, config=config)

class GearUp(object):
  def __init__(
    self,
    functions, named_functions,
    helper: Union[None, str]='help',
    config: Union[None, bytes, str, os.PathLike]=None
  ):
    self.functions = functions
    self.named_functions = named_functions

    self.helper = helper
    self.config = config

  def with_config(self, config: Union[None, bytes, str, os.PathLike]) -> 'GearUp':
    return GearUp(self.functions, self.named_functions, helper=self.helper, config=config)

  def with_helper(self, helper: Union[None, str]) -> 'GearUp':
    return GearUp(self.functions, self.named_functions, helper=helper, config=self.config)

  def without_helper(self) -> 'GearUp':
    return self.with_helper(helper=None)

  def __call__(self, args=None):
    return compose(self.functions, self.named_functions, helper=self.helper, config=self.config)(args)

def gearup(*args, **kwargs) -> GearUp:
  return GearUp(args, kwargs)