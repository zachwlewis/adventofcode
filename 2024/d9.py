# adventofcode.com
# Day 9
# https://adventofcode.com/2024/day/9

import common
from grid import Grid
from point import IntPoint2

def get_input(s:str) -> list[int]:
    filename = common.getFilePath(s)
    data: list[int] = []
    with open(filename, "r") as file:
        data = [int(x) for x in file.read().strip()]

    return data

def uncompress_data(data: list[int]) -> list[int]:
    id = 0
    ud: list[int] = []
    add: bool = True
    for d in data:
        if add:
            # add d instances of id to ud
            for i in range(d):
                ud.append(id)
            id += 1
        else:
            for i in range(d):
                ud.append(-1)
        add = not add
    return ud

def compact_data(data: list[int]) -> list[int]:
    start, end = 0, len(data) - 1
    while start < end:
        if data[start] >= 0:
            start += 1
        elif data[end] < 0:
            end -= 1
        else:
            data[start], data[end] = data[end], data[start]
            start += 1
            end -= 1
    return data

def calculate_checksum(data: list[int]) -> int:
    checksum = 0
    for i in range(len(data)):
        if data[i] < 0:
            break
        checksum += i * data[i]
    return checksum

def solution1(data: list[int]) -> int:
    ud = uncompress_data(data)
    cd = compact_data(ud)
    return calculate_checksum(cd)

test1 = [1,2,3,4,5]
test2 = [2,3,3,3,1,3,3,1,2,1,4,1,4,1,3,1,4,0,2]
input = get_input("input9.txt")
print("Test cases:")
print(f"S1: {solution1(test2)}")
#print(f"S2: {countHarmonicAntinodes(test)}")

print("Solutions:")
print(f"S1: {solution1(input)}")
#print(f"S2: {countHarmonicAntinodes(input)}")
