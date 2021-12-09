"""
adventofcode.com
Day 9
https://adventofcode.com/2021/day/9
"""

import fr

inputs: list[str] = fr.read_as_list('input9')

WIDTH = len(inputs[0])
HEIGHT = len(inputs)
X_MAX = WIDTH - 1
Y_MAX = HEIGHT - 1


T=0
L=1
B=2
R=3

grid = []
for input in inputs:
    grid.append(list(map(int,list(input))))

def print_grid():
    for row in grid:
        for col in row:
            print(col,end='')

        print('')

gradient = [[[0]*4]*WIDTH]*HEIGHT
low_points = []
BORDER_HEIGHT = 100

# Populate the gradient map.
risk_level: int = 0
for y in range(HEIGHT):
    for x in range(WIDTH):
        UP = BORDER_HEIGHT if y == 0 else grid[y-1][x]
        LEFT = BORDER_HEIGHT if x == 0 else grid[y][x-1]
        DOWN = BORDER_HEIGHT if y == Y_MAX else grid[y+1][x]
        
        RIGHT = BORDER_HEIGHT if x == X_MAX else grid[y][x+1]
        H = grid[y][x]
        gr = [0]*4
        gr[T] = H - UP
        gr[L] = H - LEFT
        gr[B] = H - DOWN
        gr[R] = H - RIGHT

        if max(gr) < 0:
            low_points.append([x,y])
            risk_level += 1 + H

print(risk_level)

def neighbors(x:int,y:int, s:set[str]=set()) -> set[str]:
    if x < 0 or x > X_MAX or y < 0 or y > Y_MAX: return set()
    if grid[y][x] == 9: return set()

    p = f'({x},{y})'
    if p in s: return set()
    
    s.add(p)
    s.update(neighbors(x+1, y, s))
    s.update(neighbors(x-1, y, s))
    s.update(neighbors(x, y+1, s))
    s.update(neighbors(x, y-1, s))
    

    return s

basins: list[int] = []
for lp in low_points:
    b_set = neighbors(lp[0],lp[1],set())
    basins.append(len(b_set))

basins.sort(reverse=True)

print(basins[0] * basins[1] * basins[2])
