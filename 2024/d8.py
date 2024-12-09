# adventofcode.com
# Day 8
# https://adventofcode.com/2024/day/8

import common
from grid import Grid
from point import IntPoint2

def getInput(s:str) -> Grid[str]:
    filename = common.getFilePath(s)
    data, x, y = [], 0, 0
    with open(filename, "r") as file:
        data = file.read().splitlines()    
    return Grid(data)

def countAntinodes(grid:Grid[str]) -> int:
    # Find all nodes of each frequency.
    nodes: map[str, list[IntPoint2]] = {}
    for y in range(grid.height):
        for x in range(grid.width):
            node = grid[x, y]
            if node != ".":
                if node not in nodes:
                    nodes[node] = []
                nodes[node].append(IntPoint2(x, y))

    antinodes: set[IntPoint2] = set()
    for node in nodes:
        for i in range(len(nodes[node])):
            for j in range(i + 1, len(nodes[node])):
                an1, an2 = findAntinodes(nodes[node][i], nodes[node][j])
                antinodes.add(an1)
                antinodes.add(an2)

    # Only antinodes inside the grid are valid.
    valid_antinodes = [an for an in antinodes if 0 <= an.x < grid.width and 0 <= an.y < grid.height]
    g = grid.copy()
    for an in valid_antinodes:
        g[an.x, an.y] = "#"
    return len(valid_antinodes)

def countHarmonicAntinodes(grid:Grid[str]) -> int:
    # Find all nodes of each frequency.
    nodes: map[str, list[IntPoint2]] = {}
    for y in range(grid.height):
        for x in range(grid.width):
            node = grid[x, y]
            if node != ".":
                if node not in nodes:
                    nodes[node] = []
                nodes[node].append(IntPoint2(x, y))

    antinodes: set[IntPoint2] = set()
    for node in nodes:
        for i in range(len(nodes[node])):
            for j in range(i + 1, len(nodes[node])):
                antinodes.update(harmonicAntinodes(nodes[node][i], nodes[node][j], grid.width, grid.height))

    # Only antinodes inside the grid are valid.
    print(nodes)
    print(antinodes)
    valid_antinodes = [an for an in antinodes if 0 <= an.x < grid.width and 0 <= an.y < grid.height]
    g = grid.copy()
    for an in valid_antinodes:
        g[an.x, an.y] = "#"
    print(g)
    print(valid_antinodes)
    return len(valid_antinodes)

def findAntinodes(a:IntPoint2, b:IntPoint2) -> tuple[IntPoint2, IntPoint2]:
    """ Each pair of nodes has an antinode on either side."""
    d = a - b
    an1 = a + d
    an2 = b - d
    return (an1, an2)

def harmonicAntinodes(a:IntPoint2, b:IntPoint2, width: int, height: int) -> set[IntPoint2]:
    """ Each pair of nodes has an antinode on either side."""
    antinodes: set[IntPoint2] = set()
    d = a - b
    p = a
    while p.x >= 0 and p.x < width and p.y >= 0 and p.y < height:
        antinodes.add(p)
        p += d

    p = b
    while p.x >= 0 and p.x < width and p.y >= 0 and p.y < height:
        antinodes.add(p)
        p -= d
    return antinodes

test= getInput("input8_test.txt")
input = getInput("input8.txt")

print("Test cases:")
print(f"S1: {countAntinodes(test)}")
print(f"S2: {countHarmonicAntinodes(test)}")

print("Solutions:")
print(f"S1: {countAntinodes(input)}")
print(f"S2: {countHarmonicAntinodes(input)}")
