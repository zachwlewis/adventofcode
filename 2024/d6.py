# adventofcode.com
# Day 6
# https://adventofcode.com/2024/day/6

import common
from grid import Grid

def getInput(s:str) -> Grid[str]:
    filename = common.getFilePath(s)
    data, x, y = [], 0, 0
    with open(filename, "r") as file:
        data = file.read().splitlines()    
    return Grid(data)

def walkGrid(grid:Grid[str]) -> int:
    x, y = grid.find('^')
    dx, dy = 0, -1

    # Walk the grid until we leave it.
    while x >= 0 and x < grid.width and y >= 0 and y < grid.height:
        # Mark our current location as visited.
        grid[x, y] = 'X'
        nx, ny = x + dx, y + dy
        if nx < 0 or nx >= grid.width or ny < 0 or ny >= grid.height:
            break
        # Check if we can move forward.
        if grid[x + dx, y + dy] == '#':
            # There is a wall in front of us.
            # Turn right.
            dx, dy = -dy, dx
            continue
        else:
            # There is no wall in front of us.
            # Move forward.
            x += dx
            y += dy

    return grid.count('X')

def drawPath(grid:Grid[str]) -> int:
    g = grid.copy()
    x, y = g.find('^')
    sx, sy = x, y
    dx, dy = 0, -1
    g[x, y] = '|'
    _loops = 0
    visited = set()
    loops = set()
    # Walk the grid until we leave it.
    while x >= 0 and x < g.width and y >= 0 and y < g.height:
        # Mark our current location as visited, with direction.
        visited.add((x, y, dx, dy))
        nx, ny = x + dx, y + dy
        if dx == 0: # up or down
            g[x, y] = '|' if g[x,y] != '-' else '+'
        if dy == 0: # left or right
            g[x, y] = '-' if g[x,y] != '|' else '+'
        if nx < 0 or nx >= g.width or ny < 0 or ny >= g.height:
            break
        # Check if we can move forward.
        if g[nx,ny] == '#':
            # There is a wall in front of us.
            # Turn right.
            dx, dy = -dy, dx
            continue
        else:
            # There is no wall in front of us.
            # Check for a loop opportunity.
            if g[nx,ny] == '.':
                if wouldCauseLoop(g, visited, x, y, dx, dy):
                        loops.add((nx,ny))
                        _loops += 1
            
            # Move forward.      
            x = nx
            y = ny

    if (sx,sy) in loops:
        loops.remove((sx,sy))

    return len(loops)

def wouldCauseLoop(grid:Grid[str], visited:set[tuple[int,int,int,int]], x:int, y:int, dx:int, dy:int) -> bool:
    # Check if we would hit a wall or a visited location by putting a wall here.
    # We are moving in direction dx, dy, so putting a wall here would cause
    # us to turn right.
    if grid[x + dx, y + dy] == "#":
        return False
    
    g = grid.copy()
    g[x + dx, y + dy] = '#'

    v = visited.copy()
    v.remove((x, y, dx, dy))

    # Walk the grid until we leave it or reach the start.
    while x >= 0 and x < g.width and y >= 0 and y < g.height:
        # If we've already visited this location and direction, we have a loop.
        if (x, y, dx, dy) in v:
            return True
        
        # Mark our current location as visited.
        v.add((x, y, dx, dy))
        nx, ny = x + dx, y + dy

        if nx < 0 or nx >= g.width or ny < 0 or ny >= g.height:
            # We have left the grid. No loop.
            return False
        # Check if we can move forward.
        if g[nx, ny] == '#':
            # There is a wall in front of us.
            # Turn right.
            dx, dy = -dy, dx
            continue
        else:
            # There is no wall in front of us.
            # Move forward.
            x = nx
            y = ny

    return False

test= getInput("input6_test.txt")
input = getInput("input6.txt")
t_loops = drawPath(test)
loops = drawPath(input)

print("Test cases:")
print(f"S1: {walkGrid(test)}")
print(f"S2: {t_loops}")
#
print("Solutions:")
print(f"S1: {walkGrid(input)}")
print(f"S2: {loops}")