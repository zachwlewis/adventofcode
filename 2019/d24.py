# adventofcode.com
# Day 24
# https://adventofcode.com/2019/day/24

from common import getFilePath
from intpoint import IntPoint, GridArrayConverter
from typing import Dict, Tuple, Set, List

"""
Input
-----
#.#..
.#.#.
#...#
.#..#
##.#.
"""

adj: Set[IntPoint] = {IntPoint(1,0), IntPoint(0,1), IntPoint(-1,0), IntPoint(0,-1)}

def adjacentBugs(p: IntPoint, g: Dict[IntPoint, int]) -> int:
  bugs = 0
  for _p in adj:
    _v = g.get(p + _p, None)
    if _v != None and _v == 1:
      bugs += 1

  return bugs

def printGrid(g: Dict[IntPoint, int]) -> None:
  s = '  0 1 2 3 4\n'
  lut = {0:'.',1:'#'}
  count = 0
  for k, v in g.items():
    if count % 5 == 0: s += '%d ' % (count//5)
    s += lut[v]+' '
    if count % 5 == 4: s += '\n'
    count += 1

  print(s)
    
def tick(g: Dict[IntPoint, int]) -> Dict[IntPoint, int]:
  _g: Dict[IntPoint, int] = dict()
  for k, v in g.items():
    a = adjacentBugs(k, g)
    if v == 0:
      if a == 1 or a == 2: _g[k] = 1
      else: _g[k] = 0
    else:
      if a != 1: _g[k] = 0
      else: _g[k] = 1
    
  return _g

def bdr(g: Dict[IntPoint, int]) -> int:
  """Calculates the biodiversity rating."""
  _values = list(g.values())
  _value = 0
  for i in range(len(_values)):
    if _values[i] == 1: _value += 2 ** i

  return _value


initial: Dict[IntPoint, int] = {
  IntPoint(0,0):1,IntPoint(1,0):0,IntPoint(2,0):1,IntPoint(3,0):0,IntPoint(4,0):0,
  IntPoint(0,1):0,IntPoint(1,1):1,IntPoint(2,1):0,IntPoint(3,1):1,IntPoint(4,1):0,
  IntPoint(0,2):1,IntPoint(1,2):0,IntPoint(2,2):0,IntPoint(3,2):0,IntPoint(4,2):1,
  IntPoint(0,3):0,IntPoint(1,3):1,IntPoint(2,3):0,IntPoint(3,3):0,IntPoint(4,3):1,
  IntPoint(0,4):1,IntPoint(1,4):1,IntPoint(2,4):0,IntPoint(3,4):1,IntPoint(4,4):0,
}

seen: Set[str] = set()
searching = True
seen.add(''.join(str(e) for e in initial.values()))
print(seen)
steps = 0
while searching:
  initial = tick(initial)
  steps += 1
  s = ''.join(str(e) for e in initial.values())
  
  if s in seen:
    print(steps, s)
    printGrid(initial)
    searching = False
  else: seen.add(s)

  if steps % 50 == 0:
    print(steps, s, len(seen))
    printGrid(initial)

print(bdr(initial))