## adventofcode.com
# Day 5
# https://adventofcode.com/2020/day/5

import fr

from typing import List

boardingPasses = fr.readAsList('input5')

def parseSeatCode(code:str) -> int:
  row = int(code[:-3].replace('F', '0').replace('B','1'), 2)
  col = int(code[-3:].replace('L', '0').replace('R','1'), 2)

  return row * 8 + col

seats = list(map(parseSeatCode, boardingPasses))

print(f'Answer 1: {max(seats)}')

seats.sort()
seatId = seats[0]

for seat in seats:
  if seat != seatId: break
  seatId += 1

print(f'Answer 2: {seatId}')



