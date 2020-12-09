## adventofcode.com
# Day 9
# https://adventofcode.com/2020/day/

import fr
from typing import List

answer1 = 'unknown'
answer2 = 'unknown'

inputs = list(map(int,fr.readAsList('input9')))

def sumExists(data: List[int], value: int) -> bool:
  for i in range(1,len(data) - 1):
    target = value - data[i - 1]
    if target in data[i:]: return True

  return False

for i in range(25, len(inputs)):
  if not sumExists(inputs[i-25:i], inputs[i]):
    answer1 = inputs[i]
    break

for i in range(0, len(inputs)):
  acc = 0
  j = i
  while acc < answer1 and j < len(inputs):
    acc += inputs[j]
    j += 1

  if acc == answer1:
    contiguous = inputs[i:j]
    answer2 = min(contiguous) + max(contiguous)
    break


print(f'Answer 1: {answer1}')
print(f'Answer 2: {answer2}')