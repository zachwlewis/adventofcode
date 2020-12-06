## adventofcode.com
# Day 6
# https://adventofcode.com/2020/day/6

import fr

from typing import List

customs = fr.readAsList('input6-clean')

answers = list(map(chr, range(97,123)))

def totalUnions() -> int:
  unions = 0
  for group in customs:
    for answer in answers:
      if answer in group: unions += 1

  return unions

def totalIntersections() -> int:
  intersections = 0
  for group in customs:
    g = group.split(',')
    sets: List[set] = list(map(lambda s: set(s), g))
    intr = set(answers)
    for answer in sets:
      intr = intr.intersection(answer)

    intersections += len(intr)
  
  return intersections

print(f'Answer 1: {totalUnions()}')
print(f'Answer 2: {totalIntersections()}')
