import os

def test_kwargs():
  from gearup import gearup, apply

  def f(**kwargs):
    assert 'clf' in kwargs
    assert 'method' in kwargs
    assert 'foo' in kwargs['clf']
    assert 'bar' in kwargs['clf']
    assert 'bar' in kwargs['method']
    assert len(kwargs) == 2
    assert len(kwargs['clf']) == 2
    assert len(kwargs['method']) == 1

  print()
  gearup(f)(['clf={}', 'clf.foo=1', 'clf.bar=2', 'method.bar=3'])

  def f1(alpha: float): return alpha
  def f2(beta: float, gamma: float): return beta + gamma

  def main(f, **kwargs):
    if f == 'f1':
      return apply(f1)(**kwargs['func'])
    elif f == 'f2':
      return apply(f2)(**kwargs['func'])
    else:
      raise NotImplementedError()

  gearup(main)(['f=f1', 'func.alpha=3'])
  gearup(main)(['f=f2', 'func.beta=5', 'func.gamma=6'])

def test_conf():
  from gearup import gearup

  def f(*args, **kwargs):
    print(args)
    return kwargs

  root = os.path.dirname(__file__)
  conf_path = os.path.join(root, 'config', 'config.yaml')

  # conf = gearup(f).with_config(conf_path)([])
  # print(conf)
  # assert conf['fee']['number'] == 1
  # assert conf['fee']['smth']['fee-smth'] == 'a'
  # assert conf['fee']['smth']['must-not-be-here-when-b'] == True
  # assert conf['foo']['bar']['order'] == 'first'
  # assert 'additional' not in conf['foo']['bar']['order']

  conf = gearup(f).with_config(conf_path)(['fee=two'])
  print(conf)
  assert 'must-not-be-here-when-b' not in conf['fee']['smth']
  assert conf['fee']['number'] == 'two'
  assert conf['fee']['smth']['fee-smth'] == 'b'
  assert conf['foo']['bar']['order'] == 'first'
  assert 'additional' not in conf['foo']['bar']['order']

  conf = gearup(f).with_config(conf_path)(['foo.bar=second'])
  print(conf)
  assert conf['fee']['number'] == 1
  assert conf['fee']['smth']['fee-smth'] == 'a'
  assert conf['foo']['bar']['order'] == 'reversed'
  assert conf['foo']['bar']['additional'] == 'stuff'

  conf = gearup(f).with_config(conf_path)(['fee=two', 'foo.bar=second', 'fee.smth=a'])
  print(conf)
  assert conf['fee']['number'] == 'two'
  assert conf['fee']['smth']['fee-smth'] == 'a'
  assert conf['foo']['bar']['order'] == 'reversed'
  assert conf['foo']['bar']['additional'] == 'stuff'

  conf = gearup(f).with_config(conf_path)(['fee=two', 'fee.smth=a', 'foo.bar=second', 'fee.smth.fee-smth=999'])
  print(conf)
  assert conf['fee']['number'] == 'two'
  assert conf['fee']['smth']['fee-smth'] == 999
  assert conf['foo']['bar']['order'] == 'reversed'
  assert conf['foo']['bar']['additional'] == 'stuff'

def test_alternative():
  from gearup import gearup

  def f(*args, **kwargs):
    print(args)
    return kwargs

  root = os.path.dirname(__file__)
  conf_path = os.path.join(root, 'config', 'config.yaml')

  conf = gearup(f).with_config(conf_path)(['=alternative'])
  print(conf)
  assert conf['fee']['number'] == 'two'
  assert 'must-not-be-here-when-b' not in conf['fee']['smth']
  assert conf['fee']['smth']['fee-smth'] == 'b'
  assert conf['foo']['bar']['order'] == 'reversed'
  assert conf['foo']['bar']['additional'] == 'stuff'

  try:
    conf = gearup(f).with_config(conf_path)(['=empty'])
  except FileNotFoundError:
    pass