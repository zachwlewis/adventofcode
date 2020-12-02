# adventofcode.com
# Integer Point
# Utility class for dealing with integer points.

class IntPoint:
  """An Integer Point"""
  def __init__(self, x: int, y: int):
    self.x = x
    self.y = y

  def __add__(self, o): return IntPoint(self.x + o.x, self.y + o.y)
  def __sub__(self, o): return IntPoint(self.x - o.x, self.y - o.y) 
  def __mul__(self, o):
    if type(o) == IntPoint: return IntPoint(self.x * o.x, self.y * o.y)
    elif type(o) == int: return IntPoint(self.x * o, self.y * o)
    else: raise TypeError("Expected int or IntPoint. Got %s instead." % type(o))
  def __eq__(self, o): return self.x == o.x and self.y == o.y
  def __ne__(self, o): return not self == o

  def __str__(self) -> str: return '(%d, %d)' % (self.x, self.y)
  def __repr__(self) -> str: return 'IntPoint %s' % str(self)
  def __hash__(self): return hash((self.x, self.y))

class GridArrayConverter:
  def __init__(self, width: int, height: int):
    self.width = width
    self.height = height

  def pti(self, point: IntPoint) -> int:
    """Converts an IntPoint to an array index."""
    return point.x + point.y * self.width

  def itp(self, index: int) -> IntPoint:
    """Converts an array index to an IntPoint."""
    return IntPoint(index % self.width, index // self.height)

