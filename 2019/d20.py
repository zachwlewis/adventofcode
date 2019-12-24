# adventofcode.com
# Day 20
# https://adventofcode.com/2019/day/20

from common import getFilePath
from intpoint import IntPoint
import array
import time
from typing import Dict, Tuple, Set, List
import re

t_start = time.time()

named = re.compile('\w\w')

U, D, L, R = IntPoint(0, -1), IntPoint(0, 1), IntPoint(-1, 0), IntPoint(1, 0)

FILE_PATH = getFilePath('input20_sample.txt')

def idx(inP: IntPoint, inW: int, inH: int) -> int:
  return inP.x + inP.y * inW

a: array = array.array('u')
f = open(FILE_PATH, 'r')
input = list(f.read())
w, h = 0, 0
x, y = 0, 0
for c in input:
  #print(c, end='', flush=True)
  w = max(x, w)
  h = max(y, h)
  if c == '\n':
    x = 0
    y += 1
  else:
    x += 1
    a.append(c)

#print('\n%dx%d' % (w, h))
xs = 2
xe = w - 2
ys = 2
ye = h - 1
#print('x:[%d..%d] y:[%d..%d]' % (xs, xe, ys, ye))

# Build path map

pm: Dict[IntPoint, List[IntPoint]] = dict()
portalToPoint: Dict[str,IntPoint] = dict()
pointToPortal: Dict[IntPoint,str] = dict()

for _y in range(ys, ye):
  for _x in range(xs, xe):
    _p = IntPoint(_x, _y)
    v = a[idx(_p, w, h)]
    if v == '.':
      # Valid path, add to list
      pm[_p] = []

      # Check for named point
      names = [a[idx(_p+U+U, w, h)] + a[idx(_p+U, w, h)],
               a[idx(_p+D, w, h)] + a[idx(_p+D+D, w, h)],
               a[idx(_p+L+L, w, h)] + a[idx(_p+L, w, h)],
               a[idx(_p+R, w, h)] + a[idx(_p+R+R, w, h)]]

      for _name in names:
        if named.match(_name):
          _from = _name
          _to = _name + '_'
          if _from == 'AA' or _from == 'ZZ': _to = _name
          if portalToPoint.get(_from, None):
            _from = _name + '_'
            _to = _name
          portalToPoint[_from] = _p
          pointToPortal[_p] = _to

#print('portalToPoint =', portalToPoint)
#print('pointToPortal =', pointToPortal)

# Now, fill out pm with their neighbors, including portals.
for _p in pm:
  # Link Portals
  if _p in pointToPortal:
    _destination = portalToPoint[pointToPortal[_p]]
    if _destination != _p:
      pm[_p].append(_destination)
      #print('%s => %s' % (_p, _destination))
  # Link adjacent tiles
  _adj = [_p+U, _p+D, _p+L, _p+R]
  for _a in _adj:
    if _a in pm: pm[_p].append(_a)

# pm now contains a proper adjacency map of the maze.
t_map = time.time()
print('mapped in %s sec.' % (t_map - t_start))

visited: Set[IntPoint] = {portalToPoint['AA']}

edge: List[IntPoint] = [portalToPoint['AA']]
steps = 0
searching = True

while searching:
  steps += 1
  _edge: List[IntPoint] = []
  for _p in edge:
    # Iterate over the leading edge.
    for _a in pm[_p]:
      if not _a in visited:
        # _a hasn't been visited. Add it.
        _edge.append(_a)
        visited.add(_a)
        if _a == portalToPoint['ZZ']: searching = False

  edge = _edge

print('%d steps in %s sec.' % (steps, (time.time()-t_map)))
