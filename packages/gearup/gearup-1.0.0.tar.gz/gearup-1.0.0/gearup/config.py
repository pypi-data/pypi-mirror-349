import os
from typing import Union, Any, Mapping

import yaml
from omegaconf import OmegaConf

__all__ = [
  'read_config'
]

ROOT_TOKENS = ['', '.', '*']

def get_root(prefix: list[str], root: Union[None, bytes, str, os.PathLike]):
  if root is None:
    return None

  new_root = os.path.join(root, *prefix)

  if os.path.isdir(new_root):
    return new_root
  else:
    return None

def expand(value: Any, root: Union[None, bytes, str, os.PathLike]) -> Any:
  if root is None:
    return value

  if not os.path.isdir(root):
    return value

  if isinstance(value, Mapping):
    return OmegaConf.create({
      k: expand(v, os.path.join(root, k))
      for k, v in value.items()
    })

  elif isinstance(value, str):
    path = os.path.join(root, f'{value}.yaml')
    return expand(OmegaConf.load(path), root)

  else:
    raise ValueError(f'Value for the hierarchical config ({root}) must be a string, got {value}.')

def assign(config, path, value):
  if len(path) == 0:
    return value

  *rest, last = path

  current = config
  for i, k in enumerate(rest):
    if k not in current:
      current[k] = dict()

    elif not isinstance(current[k], Mapping):
      raise ValueError(
        f'Path {rest[:i + 1]} exists but is not a dictionary ({current[k]})!'
      )

    current = current[k]

  current[last] = value

  return config

def cli_list(base_config, arguments: list[str], root):
  args = list()
  kwargs = list()

  for arg in arguments:
    if '=' in arg:
      path, arg = arg.split('=', maxsplit=1)
      value = yaml.load(arg, Loader=yaml.SafeLoader)

      if path in ROOT_TOKENS:
        kwargs.append(([], value))
      else:
        ks = path.split('.')
        if any(len(k) == 0 or '/' in k for k in ks):
          raise ValueError(f'Path {path} is incorrect!')
        kwargs.append((ks, value))

    else:
      value = yaml.load(arg, Loader=yaml.SafeLoader)
      args.append(value)

  kwargs_sorted = sorted(kwargs, key=lambda e: len(e[0]))

  config = base_config
  for ks, value in kwargs_sorted:
    value = expand(value, get_root(ks, root))
    config = assign(config, ks, value)

  return args, config

def read_config(arguments, config: Union[None, bytes, str, os.PathLike]):
  if config is None:
    root = None
    config = OmegaConf.create()
  else:
    root = os.path.dirname(os.path.abspath(config))
    config = expand(OmegaConf.load(config), root)

  args, config = cli_list(config, arguments, root)
  config = OmegaConf.to_container(config)

  return args, config