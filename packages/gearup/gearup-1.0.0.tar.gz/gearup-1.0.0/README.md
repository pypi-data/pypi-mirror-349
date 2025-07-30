# GearUp

Have you ever had a moment, when the code is ready, you are eager to launch it,
you want to know if your new and shiny method works or not, just to realize you need to write
100+ lines of `argparse` or `click`?

Gear up and get ready to go! 

## Quick intro

Assume your project contains `main.py` script with the following functions: 

```python
### main.py

def train(method: str, dataset: str, alpha: float):
  <do stuff>

def test_accuracy(method: str, dataset: str):
  <do testing>

def test_robustness(method: str):
  <do testing>
```

Just add:

```python
if __name__ == '__main__':
  from gearup import gearup
  gearup(train, test=dict(accuracy=test_accuracy, robustness=test_robustness))()
```

and you are ready to go!

```bash
> python main.py train method=resnet dataset=mnist alpha=0.01
> python main.py test accuracy method=resnet dataset=mnist
> python main.py test robustness method=resnet
```

## Installation

As usual:
```bash
pip install gearup
```
or
```bash
pip install git+https://gitlab.com/craynn/gearup.git
```

## How it works

`gearup`, applied to a function, reads the signature of the function
and infers which arguments should be passed to it:

```python
def f(x: int, y: int):
  return x + y
```

When gear-uped function is called without arguments it reads `sys.argv`,
alternatively, it can be called with a list of strings:

```python
gearup(f)(['1', '2']) ### result = 3
gearup(f)() ### read from console arguments
```

`gearup` relies on [`omegaconf`](https://pypi.org/project/omegaconf/) and [`PyYAML`](https://pypi.org/project/PyYAML/):
- arguments are converted according to YAML rules, e.g., `1` is parsed as an integer,
    `1.0` --- as a float, `'1'` --- as a string;
- keyword arguments, like `classifier.alpha=1.0`, are parsed as a
    [`dot-list`](https://omegaconf.readthedocs.io/en/latest/usage.html#from-a-dot-list);
- positional arguments (ones that do not contain `=` sign) are always passed to the function.

After that the underlying function is called: `f(*args, **kwargs)`, **passing only the arguments required by the function**...

Yes, no flags, no aliases, just launch script like
a python function (Haskell style)...

```bash
> python main.py 1 y=2
```

*Notes:*
- **spaces should not appear between argument name, `=` and argument value**:
  - `a=x` sets value of argument `a` to `x`;
  - `a = x` is interpreted as three separate arguments: two positional: `a` and `x`, and a keyword one
  (with empty name and value);
- if you need to supply a value with a space character in it, use quotes:
  `python main.py x='a b c'`;
- if you need to supply a value with `=` character in it, just specify argument name:
  `python main.py x=a=b` or, better, `python main.py x='a=b'`;
- it is impossible to set one of variational positional arguments (`*args`) to a value,
  that contains `=` character;
- lists are valid values: `python main.py x=[1,2,3,4]` or
  (in case you want to add spaces) `python main.py 'x=[1, 2, 3, 4]'`. 

As a bonus, `gearup.apply(f)(*args, **kwargs)` provides a Python-friendly way to pass down a subconfig.

```python
import gearup

def method1(x: int, y: int): return x + y
def method2(x: int, z: float): return x / z

def main(method, x: int, **kwargs):
  if method == 'method1':
    method = method1
  elif method == 'method2':
    method = method2
  else:
    raise ValueError()

  gearup.apply(method, x, **kwargs)

if __name__ == '__main__':
  gearup.gearup(main)()
``` 
 

### Commands

Sometimes you need to pack several functions into one script:

```python
gearup(train, test)()
### or
gearup(train=train, test=test)()
### or
gearup(train, test=test)()
```

```bash
> python main.py train <arguments for train>
> python main.py test <arguments for test>
```

More precisely, if supplied with more than one argument or at least one keyword argument,
`gearup` consumes the first CLI argument and
switches between provided functions.

Bonus: it is recursive!

```python
def train(...): pass
def test_fast(...): pass
def test_slow(...): pass

gearup(
  train,
  test=dict(
    fast=test_fast,
    slow=test_slow
  )
)()
```

```bash
> python main.py train method=resnet alpha=0.1
> python main.py test slow method=resnet
```

Note: when a non-keyword argument is passed to `gearup`,
it reads `__name__` attribute of this argument. For example, `gearup(f1, f2)` is equivalent to
`gearup(f1=f1, f2=f2)`.

### Help

Just add `help`:

```
> python examples/main.py help
Available commands:
train -> (method, power, alpha: float = 0.001, flag: bool = False)
         Trains method with alpha.
test -> a -> (method)
             Tests method...
        b -> (method)
             Undocumented test function.
```

The helper keyword can be overriden (or turned off) with:
```python
gearup(...).without_helper()
gearup(...).with_helper(helper=None)
gearup(...).with_helper(helper='helpme')
```

### Configuration file

`gearup()` can be supplied with a configuration file.
```python
gearup(...).with_config('/path/to/config.yaml')
```

The config will be merged with CLI arguments, with the latter having priority:

```yaml
### config.yaml

point:
  x: 1
  y: 4
```

```python
### main.py

def norm(point):
  import math
  return math.sqrt(point['x'] ** 2 + point['y'] ** 2)

if __name__ == '__main__':
  import gearup
  result = gearup(norm).with_config('config.yaml')()
  print(result)
```

```shell
> python main.py
4.123105625617661
> python main.py point.x=3
5.0
```