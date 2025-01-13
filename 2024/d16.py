# adventofcode.com
# Day 16
# https://adventofcode.com/2024/day/16

import common
from dataclasses import dataclass
from point import IntPoint2
from grid import Grid

N = IntPoint2(0, -1)
S = IntPoint2(0, 1)
W = IntPoint2(-1, 0)
E = IntPoint2(1, 0)



def getInput(s:str) -> Grid[str]:
    filename = common.getFilePath(s)
    with open(filename, "r") as file:
        return Grid(file.read().strip().split("\n"))

test = getInput("input16_test.txt")
inpt = getInput("input16.txt")



def solution1(track:Grid[str]) -> int:
    facing = E
    facing = N
    print(E)

print("Test cases:")
solution1(test)
# print(f"S1: {solution1(w1.copy(),m1.copy())}")
# print(f"S2: {solution2(w1,m1)}")

print("Solutions:")
# print(f"S1: {solution1(wi.copy(),wm.copy())}")
# print(f"S2: {solution2(wi,wm)}")

