from gearup import apply

def test_apply():
  def f(a: int, x: int, y: int):
    return a + x + y

  assert apply(f)(1, 2, 3) == 6
  assert apply(f)(1, x=2, y=3) == 6
  assert apply(f)(a=1, x=2, y=3) == 6
  assert apply(f)(a=1, x=2, y=3, z=5) == 6

  try:
    apply(f)(1, 2, x=3, z=5)
  except TypeError:
    pass