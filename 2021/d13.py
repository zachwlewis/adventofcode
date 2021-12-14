"""
adventofcode.com
Day 13
https://adventofcode.com/2021/day/13
"""

import fr
from intpoint import IntPoint

inputs: list[str] = fr.read_as_list('input13')

points: list[IntPoint] = []
folds: list[IntPoint] = []
for input in inputs:
    if input.startswith('fold along '):
        fold = input[11:].split('=')
        if fold[0] == 'y': folds.append(IntPoint(0, int(fold[1])))
        if fold[0] == 'x': folds.append(IntPoint(int(fold[1]), 0))
    elif input != '':
        points.append(IntPoint.from_str(input))

def fold_page(initial: list[IntPoint], fold: IntPoint) -> list[IntPoint]:
    print(f'Folding along {fold}.')
    folded: list[IntPoint] = []
    for p in initial:
        if fold.y == 0:
            if p.x < fold.x: folded.append(p)
            if p.x > fold.x: folded.append(IntPoint(fold.x + fold.x - p.x, p.y))
        if fold.x == 0:
            if p.y < fold.y:
                folded.append(p)
            if p.y > fold.y:
                folded.append(IntPoint(p.x, fold.y + fold.y - p.y))

    
    return folded

step = fold_page(points, folds[0])

print(len(set(step)))

step = points
for fold in folds:
    step = fold_page(step, fold)

def print_page(page: list[IntPoint]):
    mx: int = 0
    my: int = 0
    for p in page:
        if p.x > mx: mx = p.x
        if p.y > my: my = p.y

    for y in range(my+1):
        for x in range(mx+1):
            if IntPoint(x,y) in page: print('# ', end='')
            else: print('. ', end='')
        print('')

print_page(step)