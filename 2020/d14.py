## adventofcode.com
# Day 14
# https://adventofcode.com/2020/day/14

import fr

answer1 = 'unknown'
answer2 = 'unknown'

inputs: list[str] = fr.readAsList('input14')

def itob36(value: int) -> str:
  """Converts an int to a 36-character binary string"""
  return f'{str(bin(value))[2:]:0>36}'

def mask36(bstr: str, _mask: str) -> str:
  """Masks a 36-character binary string with the provided mask."""
  if len(bstr) != len(_mask):
    print("Error: Binary/Mask Length Mismatch")
    return "err"

  blist = list(bstr)
  for i in range(len(_mask)):
    blist[i] = _mask[i] if _mask[i] != 'X' else bstr[i]

  return ''.join(blist)

def b36toi(bstr: str) -> int:
  """Converts a 36-character binary string to an integer."""
  return int(f'0b{bstr}',2)

mask = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
mem: dict[int, int] = {}

for line in inputs:
  _line = line.split(' ')
  if _line[0] == 'mask':
    mask = _line[2]
    continue

  # Non-mask lines in the format:
  # |     0     |1|   2   |
  #  mem[<addr>] = <value>

  addr = int(_line[0][4:-1])
  value = int(_line[2])

  mem[addr] = b36toi(mask36(itob36(value), mask))

answer1 = 0
for value in mem.values():
  answer1 += value


print(f'Answer 1: {answer1}')
print(f'Answer 2: {answer2}')