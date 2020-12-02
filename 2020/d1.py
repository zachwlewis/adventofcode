## adventofcode.com
# Day 1
# https://adventofcode.com/2020/day/1

import fr

from typing import List

lines = fr.readAsList('input1')
values = [int(line) for line in lines]

def findSum2(l: List[int], sum: int):
  start = 0
  for value in l:
    
    target = sum - value
    
    if target in values[start:]:
      return target, value

    start += 1

  return -1, -1

def findSum3(l: List[int], sum: int):
  start = 0
  for value in l:
    
    target = sum - value
    s = start
    for v in l[s:]:
      a, b = findSum2(l[s:], target)
      if a != -1: return value, a, b
      s += 1

    start += 1

  return -1, -1, -1

a, b = findSum2(values, 2020)
print(f'{a} * {b} = {a*b}')

a, b, c = findSum3(values, 2020)
print(f'{a} * {b} * {c} = {a*b*c}')




