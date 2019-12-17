# adventofcode.com
# Day 16
# https://adventofcode.com/2019/day/16

import common, math

from typing import List, Tuple, Dict

PROGRAM_PATH = common.getFilePath('input16.txt')

BASE = [0, 1, 0, -1]

def parse(path: str) -> List[int]:
  f = open(path, 'r')
  l = []
  i = f.read(1)
  while i != '':
    l.append(int(i))
    i = f.read(1)

  return l

def index(p: int, s: int) -> int: return BASE[(s+1) // (p+1) % 4]

def phase(sequence: List[int]) -> List[int]:
  output: List[int] = [0] * len(sequence)
  for p in range(0, len(sequence)):
    for s in range(0, len(sequence)):
      output[s] += sequence[p] * BASE[index(s,p)]

  for i in range(0, len(output)):
    output[i] = abs(output[i]) % 10

  return output

def part1():
  inp = parse(PROGRAM_PATH)
  for i in range(100):
    inp = phase(inp)
  print(''.join(map(str, inp[:8])))

def part2():
  inp = parse(PROGRAM_PATH)
  inp *= 10000
  offset = int(''.join(map(str, inp[:7])))
  inp = inp[offset:]
  for i in range(100):
    inp = phase(inp)
  print(''.join(map(str, inp[:8])))


#part1()
part2()
