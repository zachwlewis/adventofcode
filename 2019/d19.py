# adventofcode.com
# Day 19
# https://adventofcode.com/2019/day/19

from common import getFilePath
import intcode as icp
from typing import Dict, Tuple, Set, List

core = icp.Thread(icp.loadProgram(getFilePath('input19.txt')))

def scan(x: int, y: int) -> int:
  t = core.clone()
  t.istream.append(x)
  t.istream.append(y)
  while not t.didSucceed():
        t.process()

  return t.readOutput()

def checkPoint(left:int, bottom:int) -> Tuple[int, int, int]:
  top = bottom - 99
  right = left + 99

  return (scan(right,top),left,top)


def part1():
  strength = 0

  for y in range(50):
    for x in range(50):
      value = scan(x, y)
      if value: strength += 1
          
  print('\n%d' % strength)

def part2():
  xstart, xend = 80, 80
  # Dodge edge cases of rows with no signal by starting higher
  y = 1000

  searching = True

  while searching:
    # Find end
    xend = max(xstart,xend)
    value = scan(xend, y)
    while value == 1:
      xend += 1
      value = scan(xend, y)

    # Find start
    value = scan(xstart, y)
    while value == 0:
      xstart += 1
      value = scan(xstart, y)

    check = checkPoint(xstart,y)
    # print('[%d] %d: [%d..%d] %s' % (y, xend-xstart+1, xstart, xend,check))
    

    
    if check[0]:
      searching = False
      print(check[1] * 10000 + check[2])
      
      continue
    y += 1
    

part1()
part2()