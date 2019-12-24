# adventofcode.com
# Day 17
# https://adventofcode.com/2019/day/17

import common, math

import intcode as icp
from intpoint import IntPoint

from typing import Dict, Tuple, Set, List

PROGRAM_PATH = common.getFilePath('input17.txt')

DIRECTIONS = {'n': IntPoint(0,-1), 'e': IntPoint(1,0), 's': IntPoint(0,1), 'w': IntPoint(-1,0) }
DIRECTIONS_S = {IntPoint(0,-1): 'n', IntPoint(1,0): 'e', IntPoint(0,1): 's', IntPoint(-1,0): 'w' }
TURN_RIGHT = {'n': DIRECTIONS['e'], 'e': DIRECTIONS['s'], 's': DIRECTIONS['w'], 'w': DIRECTIONS['n']}
TURN_LEFT  = {'n': DIRECTIONS['w'], 'e': DIRECTIONS['n'], 's': DIRECTIONS['e'], 'w': DIRECTIONS['s']}

def part1() -> Tuple[Set[IntPoint], IntPoint]:
  ip = icp.Thread(icp.loadProgram(PROGRAM_PATH))
  output: List[str] = []
  x, y = 0, 0
  scaffolds: Set[IntPoint] = set()
  position: IntPoint = IntPoint(0,0)
  while not ip.didSucceed():
    ip.process()
    if ip.hasOutput():
      value = chr(ip.readOutput())
      currentLocation = IntPoint(x,y)
      if value == '#':
        # A scaffold exists at this location.
        scaffolds.add(currentLocation)
      elif value == '^':
        # The robot exists at this location.
        # It is on a scaffold.
        scaffolds.add(currentLocation)
        position = currentLocation
      
      if value == '\n':
        x = 0
        y += 1
      else: x += 1

      output.append(value)

  alignment_sum = 0

  #print(''.join(map(str,output)))
  
  for s in scaffolds:
    checks = {s + DIRECTIONS['n'],
              s + DIRECTIONS['e'],
              s + DIRECTIONS['s'],
              s + DIRECTIONS['w']}

    if len(scaffolds.intersection(checks)) == 4:
      alignment_sum += s.x * s.y

  print(alignment_sum)

  return scaffolds, position

def part2():
  """
  Via inspection, it is seen that the sequences that work match:

  A,B,A,C,A,B,C,B,C,B
  A=L,10,R,8,L,6,R,6
  B=L,8,L,8,R,8
  C=R,8,L,6,L,10,L,10
  """
  
  ip = icp.Thread(icp.loadProgram(PROGRAM_PATH))
  ip.program[0] = 2
  ip.addInputAscii('A,B,A,C,A,B,C,B,C,B\nL,10,R,8,L,6,R,6\nL,8,L,8,R,8\nR,8,L,6,L,10,L,10\nn\n')

  while not ip.didSucceed(): ip.process()
  # Clear the output buffer of the map.
  ip.readOutputAscii()
  print(ip.readOutput())

def find_path(m: Set[IntPoint], p: IntPoint) -> str:
  current_position = p
  current_direction = 'n'
  output = ''
  moves = 0
  available_move = can_move(m, current_position, current_direction)
  while available_move[0] != 'none':
    if available_move[0] == 'F':
      current_position += DIRECTIONS[current_direction]
      moves += 1
    else:
      current_direction = available_move[1]
      if moves: output += '%d,' % moves
      output += '%s,' % available_move[0]
      moves = 0

    available_move = can_move(m, current_position, current_direction)

  if moves: output += '%d,' % moves
  return output.rstrip(',')

def can_move(m: Set[IntPoint], p: IntPoint, d: str) -> Tuple[str, str]:
  # Can move forward?
  if p + DIRECTIONS[d] in m: return 'F', d
  
  # Can move right?
  if p + TURN_RIGHT[d] in m: return 'R', DIRECTIONS_S[TURN_RIGHT[d]]

  # Can move left?
  if p + TURN_LEFT[d] in m: return 'L', DIRECTIONS_S[TURN_LEFT[d]]

  # Can't move.
  return 'none', d

scaffold_map, starting_position = part1()

part2()