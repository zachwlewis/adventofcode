## adventofcode.com
# Day 11
# https://adventofcode.com/2020/day/11

import fr
from typing import List, Dict, Tuple

answer1 = 'unknown'
answer2 = 'unknown'

inputs = fr.readAsList('input11')

# The following rules are applied to every seat simultaneously:
# - If a seat is empty (L) and there are no occupied seats adjacent to it, the
#   seat becomes occupied.
# - If a seat is occupied (#) and four or more seats adjacent to it are also
#   occupied, the seat becomes empty.
# - Otherwise, the seat's state does not change.
# Floor (.) never changes; seats don't move, and nobody sits on the floor.

width = len(inputs[0])
height = len(inputs)

print(f'Seat layout: {width}x{height}')

seatsAdjacent: Dict[Tuple[int, int], bool] = {}  # Current seat adjacency.
seatsVisible: Dict[Tuple[int, int], bool] = {}  # Current seat visibility.
offsets = ([
  (-1,-1), (0,-1), (1, -1),
  (-1, 0),         (1,  0),
  (-1, 1), (0, 1), (1,  1),
])

def addOffset(a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[int, int]:
  return (a[0] + b[0], a[1] + b[1])

def adjacentSeats(pos: Tuple[int, int], s: Dict[Tuple[int, int], bool]) -> int:
  '''The number of adjacent filled seats.'''
  count = 0
  for o in offsets:
    adj = addOffset(pos, o) # the adjacent index
    if s.get(adj, False): count += 1

  return count

def inRange(pos: Tuple[int, int]) -> bool:
  return pos[0] >= 0 and pos[0] < height and pos[1] >= 0 and pos[1] < width


def visibleSeats(pos: Tuple[int, int], s: Dict[Tuple[int, int], bool]) -> int:
  '''The number of visible filled seats.'''
  count = 0
  for o in offsets:
    adj = addOffset(pos, o) # the adjacent index
    while inRange(adj) and not adj in s:
      adj = addOffset(adj, o)
    if s.get(adj, False): count += 1

  return count
  
def nextAdjacentSeats(inSeats: Dict[Tuple[int, int], bool]) -> Dict[Tuple[int, int], bool]:
  '''Returns the seats after one step.'''
  nextSeats: Dict[Tuple[int, int], bool] = {}
  for seat in inSeats.keys():
    adj = adjacentSeats(seat, inSeats)
    if inSeats[seat] == False and adj == 0:
      # If a seat is empty (L) and there are no occupied
      # seats adjacent to it, the seat becomes occupied.
      nextSeats[seat] = True
    elif inSeats[seat] == True and adj >= 4:
      # If a seat is occupied (#) and four or more seats
      # adjacent to it are also occupied, the seat becomes empty.
      nextSeats[seat] = False
    else:
      # Otherwise, the seat's state does not change.
      nextSeats[seat] = inSeats[seat]

  return nextSeats

def nextVisibleSeats(inSeats: Dict[Tuple[int, int], bool]) -> Dict[Tuple[int, int], bool]:
  '''Returns the seats after one step.'''
  nextSeats: Dict[Tuple[int, int], bool] = {}
  for seat in inSeats.keys():
    adj = visibleSeats(seat, inSeats)
    if inSeats[seat] == False and adj == 0:
      # If a seat is empty (L) and there are no occupied
      # seats adjacent to it, the seat becomes occupied.
      nextSeats[seat] = True
    elif inSeats[seat] == True and adj >= 5:
      # If a seat is occupied (#) and five or more seats
      # adjacent to it are also occupied, the seat becomes empty.
      nextSeats[seat] = False
    else:
      # Otherwise, the seat's state does not change.
      nextSeats[seat] = inSeats[seat]

  return nextSeats

for iRow in range(0, height):
  for iCol in range(0, width):
    if inputs[iRow][iCol] == 'L':
      seatsAdjacent[(iRow, iCol)] = False
      seatsVisible[(iRow, iCol)] = False

seatsOld = {}
step = -1
while seatsOld != seatsAdjacent:
  seatsOld = seatsAdjacent
  seatsAdjacent = nextAdjacentSeats(seatsOld)
  step += 1

print(f'Adjacent seats stablized after {step} steps.')

answer1 = 0
for s in seatsAdjacent.values():
  if s: answer1 += 1

# --------------

seatsOld = {}
step = -1
while seatsOld != seatsVisible:
  seatsOld = seatsVisible
  seatsVisible = nextVisibleSeats(seatsOld)
  step += 1

print(f'Visible seats stablized after {step} steps.')

answer2 = 0
for s in seatsVisible.values():
  if s: answer2 += 1

print(f'Answer 1: {answer1}')
print(f'Answer 2: {answer2}')