# adventofcode.com
# Day 11
# https://adventofcode.com/2024/day/11

import common
from grid import Grid
from point import IntPoint2

def getInput(s:str) -> Grid[int]:
    filename = common.getFilePath(s)
    data = []
    with open(filename, "r") as file:
        data = file.read().splitlines()
        
    grid = Grid(data)

    for j in range(grid.height):
        for i in range(grid.width):
            grid[i,j] = int(grid[i,j])

    return grid

def blink(stones: list[int]) -> list[int]:
    """
    Every time you blink, the stones each simultaneously change according to the
    first applicable rule in this list:

    1. If the stone is engraved with the number 0, it is replaced by a stone
       engraved with the number 1.
    2. If the stone is engraved with a number that has an even number of digits,
       it is replaced by two stones. The left half of the digits are engraved on
       the new left stone, and the right half of the digits are engraved on the
       new right stone. (The new numbers don't keep extra leading zeroes: 1000
       would become stones 10 and 0.)
    3. If none of the other rules apply, the stone is replaced by a new stone;
       the old stone's number multiplied by 2024 is engraved on the new stone.
    """

    s: list[int] = []

    for stone in stones:
        if stone == 0:
            s.append(1)
        elif len(str(stone)) % 2 == 0:
            half = len(str(stone)) // 2
            s.append(int(str(stone)[:half]))
            s.append(int(str(stone)[half:]))
        else:
            s.append(stone * 2024)
    
    return s

def solution1(stones: list[int]) -> int:
    """
    Return the number of stones with the number 1 after 2024 blinks.
    """
    original = stones.copy()
    for _ in range(25):
        stones = blink(stones)
        #print(f"Blink {_ + 1}: {stones}")

    return len(stones)

def solution2(stones: list[int]) -> int:
    """
    Need another approach, since the array grows too quickly.
    """

    return 0

test = [125,17]
input = [9759, 0, 256219, 60, 1175776, 113, 6, 92833]

print("Test cases:")
print(f"S1: {solution1(test)}")
print(f"S2: {solution2(test)}")

print("Solutions:")
print(f"S1: {solution1(input)}")
print(f"S2: {solution2(input)}")
