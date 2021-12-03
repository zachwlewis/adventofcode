## adventofcode.com
# Day 17
# https://adventofcode.com/2020/day/17

import fr

answer1 = 'unknown'
answer2 = 'unknown'

inputs: list[str] = fr.readAsList('input17')

def adjacentTo(p: tuple[int, int, int]) -> set[tuple[int, int, int]]:
  """
  Takes a point, p, and returns a set of adjacent points.
  """
  adjacentPoints: set[tuple[int, int, int]] = set()
  for x in [-1, 0, 1]:
    for y in [-1, 0, 1]:
      for z in [-1, 0, 1]:
        if x == 0 and y == 0 and z == 0: continue
        adjacentPoints.add((p[0] + x, p[1] + y, p[2] + z))

  return adjacentPoints



print(f'Answer 1: {answer1}')
print(f'Answer 2: {answer2}')
