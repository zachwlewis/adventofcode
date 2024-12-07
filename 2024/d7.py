# adventofcode.com
# Day 7
# https://adventofcode.com/2024/day/7

import common
from dataclasses import dataclass

@dataclass
class Calibration:
    target: int
    values: list[int]

def getInput(s:str) -> list[Calibration]:
    filename = common.getFilePath(s)
    data = []
    with open(filename, "r") as file:
        for line in file:
            target, values = line.split(": ")
            data.append(Calibration(int(target), [int(x) for x in values.split()]))

    return data

def evaluate_basic(target:int, current: int, values: list[int]) -> int:
    if len(values) == 0:
        raise ValueError("No values to evaluate.")
    if len(values) == 1:
        sum = 1 if current + values[0] == target else 0
        mul = 1 if current * values[0] == target else 0
        return sum + mul
    elif current >= target:
        return 0
        
    sum = current + values[0]
    mul = current * values[0]
    return evaluate_basic(target, sum, values[1:]) + evaluate_basic(target, mul, values[1:])

def evaluate_advanced(target:int, current: int, values: list[int]) -> int:
    if len(values) == 0:
        raise ValueError("No values to evaluate.")
    if len(values) == 1:
        sum = 1 if current + values[0] == target else 0
        mul = 1 if current * values[0] == target else 0
        cat = 1 if int(str(current) + str(values[0])) == target else 0
        return sum + mul + cat
    elif current >= target:
        return 0
        
    sum = current + values[0]
    mul = current * values[0]
    cat = int(str(current) + str(values[0]))
    return evaluate_advanced(target, sum, values[1:]) + evaluate_advanced(target, mul, values[1:]) + evaluate_advanced(target, cat, values[1:])

def solution1(report:list[Calibration]) -> int:
    value = 0
    for r in report:
        result = evaluate_basic(r.target, r.values[0], r.values[1:])
        if result > 0:
            value += r.target
    return value

def solution2(report:list[Calibration]) -> int:
    value = 0
    for r in report:
        result = evaluate_advanced(r.target, r.values[0], r.values[1:])
        if result > 0:
            value += r.target
    return value

test = getInput("input7_test.txt")
input = getInput("input7.txt")
print(len(input))
print("Test cases:")
print(f"S1: {solution1(test)}")
print(f"S2: {solution2(test)}")

print("Solutions:")
print(f"S1: {solution1(input)}")
print(f"S2: {solution2(input)}")