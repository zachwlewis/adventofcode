'''
adventofcode.com
Day 18
https://adventofcode.com/2021/day/18
'''

from __future__ import annotations
import re
import fr


INPUTS: list[str] = fr.read_as_list('input18')
SPLITTER = re.compile(r'\d+|\[|\]|,')

def explode(sn: str) -> tuple[str, bool]:
    '''Takes a Snailnumber and explodes it if needed.'''
    e = re.findall(SPLITTER, sn)
    depth: int = 0
    left_idx: int = -1
    right_value: int = -1
    idx: int = 0
    LENGTH = len(e)
    start: int = -1
    end: int = -1
    output = sn
    did_explode: bool = False
    while idx < LENGTH:
        symbol = e[idx]
        if   symbol == '[': depth += 1
        elif symbol == ']': depth -= 1
        elif symbol == ',': pass
        else:
            if right_value >= 0 or depth <= 4:
                if right_value >= 0:
                    e[idx] = str(right_value + int(symbol))
                    break
                else: left_idx = idx
            else:
                start = idx - 1
                end = idx + 4
                if left_idx >= 0:
                    e[left_idx] = str(int(e[left_idx]) + int(symbol))
                right_value = int(e[idx+2])
                idx = end - 1
                continue
        idx += 1

    if start >= 0 and end >= 0:
        output = ''.join(e[:start] + ['0'] + e[end:])
        did_explode = True

    return output, did_explode

def split(sn: str) -> tuple[str, bool]:
    e = re.findall(SPLITTER, sn)
    LENGTH = len(e)
    idx = 0
    target: int = -1
    while idx < LENGTH:
        symbol = e[idx]
        if symbol not in ['[', ']', ',']:
            # It's a digit!
            if int(symbol) >= 10:
                target = idx
                break
        idx += 1
    
    if target >= 0:
        value = int(e[target])
        left = value // 2
        right = int(value / 2 + 0.5)
        output = ''.join(e[:target] + ['[', str(left), ',', str(right), ']'] + e[target+1:])
        return output, True

    return sn, False

def reduce(sn: str, print_operations: bool = False) -> str:
    did_reduce: bool = True
    e = sn
    if print_operations: print(f'>  {e}')
    while did_reduce:
        did_reduce = False
        e, did_explode = explode(e)
        if did_explode:
            did_reduce = True
            if print_operations: print(f'X: {e}')
            continue
        e, did_split = split(e)
        if did_split:
            did_reduce = True
            if print_operations: print(f'S: {e}')
            continue

    if print_operations: print(f'O: {e}')
    return e

def add(a: str, b: str, print_operations: bool = False) -> str:
    sn = f'[{a},{b}]'
    reduced = reduce(sn, print_operations)
    if print_operations:
        print(f'   {a}\n  +{b}\n ={sn}\n=>{reduced}')
    return reduced

def sn_sum(it: list[str]) -> str:
    running_sum = it[0]
    remaining = it[1:]
    while len(remaining) > 0:
        next = remaining.pop(0)
        running_sum = reduce(add(running_sum, next))

    return running_sum

def magnitude(sn: str) -> int:
    '''
    Calculates the magnitude of the Snailfish Number.
    
    `M = 3*left + 2*right`
    '''
    # 1. Strip the exterior braces.
    e = re.findall(SPLITTER, sn)
    if len(e) == 1:
        return int(e[0])

    e = e[1:-1]
    LENGTH = len(e)
    # 2. Split into two pairs.
    depth: int = 0
    idx: int = -1
    for i, v in enumerate(e):
        if v == '[': depth += 1
        elif v == ']': depth -= 1
        elif v == ',' and depth == 0:
            idx = i
            break

    left = ''.join(e[:idx])
    right = ''.join(e[idx+1:])
    return 3 * magnitude(left) + 2 * magnitude(right)

# Part 1
print(magnitude(sn_sum(INPUTS)))

# Part 2
max_magnitude: int = -1
for a in range(len(INPUTS)):
    for b in range(len(INPUTS)):
        if a != b:
            mag = magnitude(add(INPUTS[a], INPUTS[b]))
            max_magnitude = max(max_magnitude, mag)

print(max_magnitude)
