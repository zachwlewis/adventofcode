# adventofcode.com
# Day 17
# https://adventofcode.com/2019/day/17

import common, math

import intcode as icp
from intpoint import IntPoint

from typing import Dict, Tuple, Set, List

PROGRAM_PATH = common.getFilePath('input17.txt')

DIRECTIONS = [IntPoint(1,0), IntPoint(-1,0), IntPoint(0,1), IntPoint(0,-1)]

def part1():
  ip = icp.Thread(icp.loadProgram(PROGRAM_PATH))
  output: List[str] = []
  x, y = 0, 0
  scaffolds: Set[IntPoint] = set()
  while not ip.didSucceed():
    ip.process()
    if ip.hasOutput():
      value = chr(ip.readOutput())
      
      if value == '#':
        # A scaffold exists at this location.
        scaffolds.add(IntPoint(x,y))
      
      if value == '\n':
        x = 0
        y += 1
      else: x += 1

      output.append(value)

  alignment_sum = 0
  
  for s in scaffolds:
    checks = {s + DIRECTIONS[0],
              s + DIRECTIONS[1],
              s + DIRECTIONS[2],
              s + DIRECTIONS[3]}

    if len(scaffolds.intersection(checks)) == 4:
      alignment_sum += s.x * s.y

  print(alignment_sum)

def part2():
  ip = icp.Thread(icp.loadProgram(PROGRAM_PATH))
  output: List[str] = []
  x, y = 0, 0
  scaffolds: Set[IntPoint] = set()
  while not ip.didSucceed():
    ip.process()
    if ip.hasOutput():
      value = chr(ip.readOutput())
      
      if value == '#':
        # A scaffold exists at this location.
        scaffolds.add(IntPoint(x,y))
      
      if value == '\n':
        x = 0
        y += 1
      else: x += 1

      output.append(value)

  alignment_sum = 0
  
  for s in scaffolds:
    checks = {s + DIRECTIONS[0],
              s + DIRECTIONS[1],
              s + DIRECTIONS[2],
              s + DIRECTIONS[3]}

    if len(scaffolds.intersection(checks)) == 4:
      alignment_sum += s.x * s.y

  print(alignment_sum)


part1()