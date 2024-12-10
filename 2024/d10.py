# adventofcode.com
# Day 10
# https://adventofcode.com/2024/day/10

import common
from grid import Grid
from point import IntPoint2

UP = IntPoint2(0, -1)
DOWN = IntPoint2(0, 1)
LEFT = IntPoint2(-1, 0)
RIGHT = IntPoint2(1, 0)
DIRECTONS = [UP, DOWN, LEFT, RIGHT]

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

def countPeaks(grid:Grid[int], p:IntPoint2) -> set[IntPoint2]:
    elevation = grid[p.t]
    peaks:set[IntPoint2] = set()
    if elevation == 9:
        peaks.add(p)
        return peaks
    for d in DIRECTONS:
        n = p + d
        if n.x < 0 or n.x >= grid.width or n.y < 0 or n.y >= grid.height:
            continue
        if grid[n.t] == elevation + 1:
            peaks.update(countPeaks(grid, n))
    
    return peaks

def scoreTrailhead(grid:Grid[int], p:IntPoint2) -> int:
    elevation = grid[p.t]
    score = 0
    if elevation == 9: return 1
    for d in DIRECTONS:
        n = p + d
        if n.x < 0 or n.x >= grid.width or n.y < 0 or n.y >= grid.height:
            continue
        if grid[n.t] == elevation + 1:
            score += scoreTrailhead(grid, n)
    
    return score

def solution1(grid:Grid[int]) -> int:
    score = 0
    trailheads = grid.findAll(0)
    for trailhead in trailheads:
        i = IntPoint2(trailhead[0], trailhead[1])
        p = countPeaks(grid, i)
        s = len(p)
        score += s

    return score

def solution2(grid:Grid[int]) -> int:
    score = 0
    trailheads = grid.findAll(0)
    for trailhead in trailheads:
        i = IntPoint2(trailhead[0], trailhead[1])
        s = scoreTrailhead(grid, i)
        score += s

    return score

test= getInput("input10_test.txt")
input = getInput("input10.txt")

print("Test cases:")
print(f"S1: {solution1(test)}")
print(f"S2: {solution2(test)}")

print("Solutions:")
print(f"S1: {solution1(input)}")
print(f"S2: {solution2(input)}")