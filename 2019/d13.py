# adventofcode.com
# Day 13
# https://adventofcode.com/2019/day/13

import common, math

import intcode as icp

from typing import List

PROGRAM_PATH = common.getFilePath('input13.txt')
f = open(PROGRAM_PATH, 'r')

SCREEN_WIDTH = 37
SCREEN_HEIGHT = 24

TILESET = [' ','X','B','=','o']
screen = dict()
score = [0]
ai = [0,0]
ball = (0,0)
paddle = (0,0)

def countBlocks():
  tiles = {0:0, 1:0, 2:0, 3:0, 4:0}

  arcade = icp.Thread(icp.loadProgram(PROGRAM_PATH))
  while not arcade.didSucceed():
    arcade.process()
    if len(arcade.ostream) == 3:
      arcade.ostream.pop(0)
      arcade.ostream.pop(0)
      tiles[arcade.ostream.pop(0)] += 1

  print(tiles[2])

def playGame():
  arcade = icp.Thread(icp.loadProgram(PROGRAM_PATH))
  arcade.program[0] = 2
  while not arcade.didSucceed():
    arcade.process()
    if arcade.status.err == icp.ERR_INPUT:
      render(arcade.ostream, ai)
      t = 0
      if ai[0] < ai[1]: t = -1
      elif ai[0] > ai[1]: t = 1
      arcade.istream.append(t)

  render(arcade.ostream, ai)
  print(score[0])

def render(o: List[int], inAI: List[int], draw=False) -> None:
  #if len(o) == 0: return
  while len(o):
    x = o.pop(0)
    y = o.pop(0)
    v = o.pop(0)

    if x == -1:
      score[0] = v
    else:
      if v == 4: inAI[0] = x
      elif v == 3: inAI[1] = x

      screen[(x,y)] = TILESET[v]

  if draw:
    for y in range(0,SCREEN_HEIGHT):
      for x in range(0,SCREEN_WIDTH):
        print(screen[(x,y)], end='')
      print()
    print("SCORE: %d" % score[0])



countBlocks()
playGame()