"""
adventofcode.com
Day 15
https://adventofcode.com/2021/day/15

Could be better optimized. Part 2 takes about a minute. :/
"""

import fr

inputs: list[str] = fr.read_as_list('input15')

def idx(x:int, y:int, side_length:int) -> int:
    return x + y * side_length

def valid(x:int, y:int, side_length:int) -> bool:
    return x >= 0 and y >= 0 and x < side_length and y < side_length

def valid_risk_sum(s: int) -> bool:
    return s > -1

def find_risk(x:int, y:int, risks: list[int], sums: list[int], side_length:int) -> int:
    # The total risk at a location is the value of the tile plus the minimum
    # neighboring risk sum.
    TILE_RISK = risks[idx(x,y, side_length)]
    adjacent_risks: list[int] = []
    if valid(x - 1, y + 0, side_length): adjacent_risks.append(sums[idx(x - 1, y + 0, side_length)])
    if valid(x + 1, y + 0, side_length): adjacent_risks.append(sums[idx(x + 1, y + 0, side_length)])
    if valid(x + 0, y - 1, side_length): adjacent_risks.append(sums[idx(x + 0, y - 1, side_length)])
    if valid(x + 0, y + 1, side_length): adjacent_risks.append(sums[idx(x + 0, y + 1, side_length)])

    R = list(filter(valid_risk_sum, adjacent_risks))
    M_SUM = 0 if len(R) == 0 else min(R)
    R_VALUE = TILE_RISK + M_SUM

    return R_VALUE

def print_grid(grid: list[int], side_length:int, header: str = '----------------'):
    print(header)
    for i, v in enumerate(grid):
        print(f'{v}', end='')
        if (i + 1) % side_length == 0: print()
    print('----------------')

def process_risk(risks: list[int], sums: list[int], side_length: int) -> bool:
    changed:bool = False
    for y in range(side_length):
        for x in range(side_length):
            if x != 0 or y != 0:
                R = find_risk(x, y, risks, sums, side_length)
                if R != sums[idx(x, y, side_length)]:
                    changed = True
                    sums[idx(x, y, side_length)] = R
    return changed

def rep(value:int, x:int, y:int) -> int:
    out = value + x + y
    while out > 9:
        out -= 9

    return out

def part1():
    tile_risks: list[int] = []
    SIDE_LENGTH = len(inputs[0])

    for input in inputs:
        tile_risks.extend(map(int,list(input)))

    total_risk: list[int] = [-1]*len(tile_risks)
    total_risk[0] = 0

# print_grid(total_risk, 'Initial')
    step:int = 0
    while process_risk(tile_risks, total_risk, SIDE_LENGTH):
        step += 1
    # print_grid(total_risk, f'Step {step}')

    print(total_risk[-1])

def part2():
    tile_risks: list[int] = []
    SIDE_LENGTH = len(inputs[0]) * 5

    for repeat_y in range(5):
        for input in inputs:
            IL = list(map(int, list(input)))
            for repeat_x in range(5):
                for value in IL:
                    tile_risks.append(rep(value, repeat_x, repeat_y))

    total_risk: list[int] = [-1]*len(tile_risks)
    total_risk[0] = 0

    # print_grid(total_risk, 'Initial')
    step:int = 0
    while process_risk(tile_risks, total_risk, SIDE_LENGTH):
        step += 1
    # print_grid(total_risk, f'Step {step}')

    print(total_risk[-1])

part1()
part2()
