"""
adventofcode.com
Day 5
https://adventofcode.com/2021/day/5
"""

import fr
from intpoint import IntPoint

inputs: list[str] = fr.read_as_list('input5')

def part1(inputs):
    vents: dict[str, int] = dict()
    for input in inputs:
        points = input.split(' -> ')
        p1 = IntPoint.from_str(points[0])
        p2 = IntPoint.from_str(points[1])

        if p1.x != p2.x and p1.y != p2.y:
            continue

        step = (p2 - p1).unit()
        while p1 != (p2 + step):
            vents[str(p1)] = vents.get(str(p1), 0) + 1
            p1 += step

    overlaps = 0
    for vent in vents.values():
        if vent > 1:
            overlaps += 1

    print(overlaps)

def part2(inputs):
    vents: dict[str, int] = dict()
    for input in inputs:
        points = input.split(' -> ')
        p1 = IntPoint.from_str(points[0])
        p2 = IntPoint.from_str(points[1])

        step = (p2 - p1).unit()
        while p1 != (p2 + step):
            vents[str(p1)] = vents.get(str(p1), 0) + 1
            p1 += step

    overlaps = 0
    for vent in vents.values():
        if vent > 1:
            overlaps += 1

    print(overlaps)

part1(inputs)
part2(inputs)


