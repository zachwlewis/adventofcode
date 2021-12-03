"""
adventofcode.com
Day 2
https://adventofcode.com/2021/day/2
"""

import fr

inputs: list[str] = fr.read_as_list('input2')
input_size = len(inputs)

def part1(data):
    """Solves part 1."""
    horizontal: int = 0
    depth: int = 0

    for command in data:
        _ = command.split()
        direction: str = _[0]
        value: int = int(_[1])

        if direction == "forward":
            horizontal += value
        elif direction == "down":
            depth += value
        elif direction == "up":
            depth -= value

    print(horizontal * depth)

def part2(data):
    """Solves part 2."""
    horizontal: int = 0
    depth: int = 0
    aim: int = 0

    for command in data:
        _ = command.split()
        direction: str = _[0]
        value: int = int(_[1])

        if direction == "forward":
            horizontal += value
            depth += value * aim
        elif direction == "down":
            aim += value
        elif direction == "up":
            aim -= value

    print(horizontal * depth)

part1(inputs)
part2(inputs)
