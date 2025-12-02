# adventofcode.com
# Day 2
# https://adventofcode.com/2025/day/2

import common, re

def parseLine(line: str) -> list[tuple[int,int]]:
    parts:list[str] = line.split(",")
    parsed: list[tuple[int,int]] = []
    for part in parts:
        parsed.append(tuple(map(int, part.split("-"))))
    return parsed

def parseId1(id: int) -> bool:
    # returns true if the id is number repeated once, like 11, 6969, 420420
    strId = str(id)
    size = len(strId)
    if size % 2 != 0: return False

    halfSize = size // 2
    first = strId[:halfSize]
    second = strId[halfSize:]

    return first == second

def parseId2(id: int) -> bool:
    # returns true if the id is number repeated multiple times, like 11, 696969, 420420420420
    strId = str(id)
    size = len(strId)

    maxWindow = size // 2
    currentWindow = 1

    while currentWindow <= maxWindow:
        if size % currentWindow != 0:
            currentWindow += 1
            continue
        
        isRepeated = True
        window = strId[:currentWindow]
        slices = size // currentWindow

        for i in range(1, slices):
            start = i * currentWindow
            end = start + currentWindow
            if strId[start:end] != window:
                # not repeated
                isRepeated = False
                break
        if isRepeated:
            # found a repeated pattern
            return True
        
        # try next window size
        currentWindow += 1

    # no repeated pattern found
    return False

filename = common.getFilePath("input2.txt")
input:list[tuple[int,int]] = []
with open(filename, "r") as file:
    for line in file:
        input.extend(parseLine(line.strip()))

s1, s2 = 0, 0
for elem in input:
    for id in range(elem[0], elem[1]+1):
        if parseId1(id): s1 += id
        if parseId2(id): s2 += id

print(f"S1: {s1}")
print(f"S2: {s2}")
