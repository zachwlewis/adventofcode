## adventofcode.com
# Day 10
# https://adventofcode.com/2020/day/10

import fr
from typing import List, Dict

answer1 = 'unknown'
answer2 = 'unknown'

inputs = list(map(int,fr.readAsList('input10')))
inputs.append(0)
inputs.sort()
diffs = [0,0,0,1]

for i in range(1,len(inputs)):
  diffs[inputs[i] - inputs[i-1]] += 1

answer1 = diffs[1] * diffs[3]

# Build a map containing the possible paths
# any node is part of
paths: Dict[int, int] = {0: 1}

for i in range(1,len(inputs)):
  n = inputs[i] # value of current node
  p = 0 # number of paths the node is part of
  p = (
    paths.get(n - 1, 0)
  + paths.get(n - 2, 0)
  + paths.get(n - 3, 0)
  )

  paths[n] = p

answer2 = paths[max(inputs)]

print(f'Answer 1: {answer1}')
print(f'Answer 2: {answer2}')