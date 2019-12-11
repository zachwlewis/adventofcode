# adventofcode.com
# Day 11
# https://adventofcode.com/2019/day/11

import common, math

import intcode as icp

from typing import Dict, Tuple
Point = Tuple[int, int]
Hull = Dict[Point, int]

def move(location: Point, direction: Point) -> Point:
  return (location[0] + direction[0], location[1] + direction[1])

PROGRAM_PATH = common.getFilePath('input11.txt')
f = open(PROGRAM_PATH, 'r')

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3

BLACK = 0
WHITE = 1
# All panels start off black
# Input 0 if black, 1 if white
DIRECTIONS = { UP:(0,1), LEFT:(-1,0), DOWN:(0,-1), RIGHT:(1,0) }
ROT_LEFT = { UP:LEFT, LEFT:DOWN, DOWN:RIGHT, RIGHT:UP }
ROT_RIGHT = { UP:RIGHT, RIGHT:DOWN, DOWN:LEFT, LEFT:UP }

def startBlack():
  hull = dict()
  robotPosition = (0,0)
  robotFacing = UP

  robotBrain = icp.Thread(icp.loadProgram(PROGRAM_PATH))
  while not robotBrain.didSucceed():
    robotBrain.process()
    if robotBrain.needInput():
      robotBrain.istream.append(hull.get(robotPosition, BLACK))
      continue

    if robotBrain.noError() and len(robotBrain.ostream) == 2:
      paint = robotBrain.ostream.pop(0)
      hull[robotPosition] = paint
      if robotBrain.ostream[0] == 0: robotFacing = ROT_LEFT[robotFacing]
      else: robotFacing = ROT_RIGHT[robotFacing]
      robotBrain.ostream.pop(0)
      robotPosition = move(robotPosition, DIRECTIONS[robotFacing])

  print(len(hull))

def printHull(hull: Hull) -> None:
  locations = hull.keys()
  xmin = 0
  xmax = 0
  ymin = 0
  ymax = 0
  for l in locations:
    xmin = min(xmin, l[0])
    xmax = max(xmax, l[0])
    ymin = min(ymin, l[1])
    ymax = max(ymax, l[1])
  width = xmax - xmin
  height = ymax - ymin

  out = ""
  for y in reversed(range(height+1)):
    for x in range(width+1):
      paint = "█" if hull.get((x+xmin,y+ymin),BLACK) == WHITE else " "
      out += paint
    out += "\n"
  
  print(out)

def startWhite():
  hull = {(0,0): WHITE}
  robotPosition = (0,0)
  robotFacing = UP

  robotBrain = icp.Thread(icp.loadProgram(PROGRAM_PATH))
  while not robotBrain.didSucceed():
    robotBrain.process()
    if robotBrain.needInput():
      robotBrain.istream.append(hull.get(robotPosition, BLACK))
      continue

    if robotBrain.noError() and len(robotBrain.ostream) == 2:
      paint = robotBrain.ostream.pop(0)
      hull[robotPosition] = paint
      if robotBrain.ostream[0] == 0: robotFacing = ROT_LEFT[robotFacing]
      else: robotFacing = ROT_RIGHT[robotFacing]
      robotBrain.ostream.pop(0)
      robotPosition = move(robotPosition, DIRECTIONS[robotFacing])

  printHull(hull)


startBlack()
startWhite()