## adventofcode.com
# Day 12
# https://adventofcode.com/2020/day/12

import fr
from typing import List, Dict, Tuple

answer1 = 'unknown'
answer2 = 'unknown'

inputs = fr.readAsList('input12')

# BOW --------------

class Ship:
  x: int = 0
  y: int = 0
  facing: str = 'E'
  
  _directions = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}
  _left = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}
  _right = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}

  def turnLeft(self, angle: int):
    turns = int(angle / 90)
    for i in range(turns):
      del i
      self.facing = self._left[self.facing]

  def turnRight(self, angle: int):
    turns = int(angle / 90)
    for i in range(turns):
      del i
      self.facing = self._right[self.facing]

  def move(self, direction: str, distance: int):
    self.x += distance * self._directions[direction][0]
    self.y += distance * self._directions[direction][1]
  
  def act(self, action: str):
    direction = action[0]
    count = int(action[1:])

    if direction == 'L': self.turnLeft(count)
    elif direction == 'R': self.turnRight(count)
    elif direction == 'F': self.move(self.facing, count)
    else: self.move(direction, count)

  def manhattan(self) -> int:
    return abs(self.x) + abs(self.y)

  def __str__(self):
    xs = f'E.{self.x}' if self.x > 0 else f'W.{abs(self.x)}'
    ys = f'N.{self.y}' if self.y > 0 else f'S.{abs(self.y)}'
    return f'{xs} {ys}'

# STERN ------------

# BOW --------------

class NavShip(Ship):
  wx: int = 10
  wy: int = 1

  def turnLeft(self, angle: int):
    turns = int(angle / 90)
    for i in range(turns):
      del i
      x = -self.wy
      self.wy = self.wx
      self.wx = x

  def turnRight(self, angle: int):
    turns = int(angle / 90)
    for i in range(turns):
      del i
      x = self.wy
      self.wy = -self.wx
      self.wx = x

  def move(self, direction: str, distance: int):
    self.wx += distance * self._directions[direction][0]
    self.wy += distance * self._directions[direction][1]

  def approach(self, distance: int):
    self.x += distance * self.wx
    self.y += distance * self.wy
  
  def act(self, action: str):
    direction = action[0]
    count = int(action[1:])

    if direction == 'L': self.turnLeft(count)
    elif direction == 'R': self.turnRight(count)
    elif direction == 'F': self.approach(count)
    else: self.move(direction, count)

  def manhattan(self) -> int:
    return abs(self.x) + abs(self.y)

  def __str__(self):
    xs = f'E.{self.x}' if self.x > 0 else f'W.{abs(self.x)}'
    ys = f'N.{self.y}' if self.y > 0 else f'S.{abs(self.y)}'

    wxs = f'E.{self.wx}' if self.wx > 0 else f'W.{abs(self.wx)}'
    wys = f'N.{self.wy}' if self.wy > 0 else f'S.{abs(self.wy)}'
    return f'{xs} {ys} > W {wxs} {wys}'

# STERN ------------

ferry = Ship()

for action in inputs:
  ferry.act(action)

print(ferry)

answer1 = ferry.manhattan()

wFerry = NavShip()

for action in inputs:
  wFerry.act(action)

answer2 = wFerry.manhattan()

print(f'Answer 1: {answer1}')
print(f'Answer 2: {answer2}')