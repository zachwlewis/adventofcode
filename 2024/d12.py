# adventofcode.com
# Day 12
# https://adventofcode.com/2024/day/12

import common
from dataclasses import dataclass
from grid import Grid
from point import IntPoint2

UP = IntPoint2(0, -1)
DOWN = IntPoint2(0, 1)
LEFT = IntPoint2(-1, 0)
RIGHT = IntPoint2(1, 0)
DIRECTONS = [UP, DOWN, LEFT, RIGHT]

CROPS = [chr(c+65) for c in range(26)]

@dataclass
class Region:
    crop: str
    area: int
    perimeter: int
    locations: set[IntPoint2]


def getInput(s:str) -> Grid[str]:
    filename = common.getFilePath(s)
    with open(filename, "r") as file:
        data = file.read().splitlines()
        
    return Grid(data)

def floodRegion(grid:Grid[str], start:IntPoint2) -> Region:
    crop: str = grid[start.t]
    area: int = 0
    perimeter: int = 0
    locations: set[IntPoint2] = set()
    stack: set[IntPoint2] = set()
    stack.add(start)

    replace = crop * 2

    while len(stack) > 0:
        current = stack.pop()
        grid[current.t] = replace
        locations.add(current)
        area += 1
        for direction in DIRECTONS:
            neighbor = current + direction
            if not grid.inBounds(neighbor.t):
                perimeter += 1
                continue
            if grid[neighbor.t] == replace:
                # not an edge
                continue

            if grid[neighbor.t] != crop:
                # The crop is different, so this is a perimeter.
                perimeter += 1
            else:
                stack.add(neighbor)
        
    return Region(crop, area, perimeter, locations)

def solution1(grid:Grid[str]) -> int:
    regions: list[Region] = []
    for y in range(grid.height):
        for x in range(grid.width):
            if grid[x, y] in CROPS:
                    regions.append(floodRegion(grid, IntPoint2(x, y)))
    price = 0
    for region in regions:
        price += region.area * region.perimeter
    return price

# For Part 2, we need to find the number of edges, not just
# the perimeter.


test= getInput("input12_test.txt")
input = getInput("input12.txt")

print("Test cases:")
print(f"S1: {solution1(test)}")
#print(f"S2: {solution2(test)}")

print("Solutions:")
print(f"S1: {solution1(input)}")
#print(f"S2: {solution2(input)}")