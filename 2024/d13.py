# adventofcode.com
# Day 13
# https://adventofcode.com/2024/day/13

import common
from dataclasses import dataclass
from point import IntPoint2

@dataclass
class ClawMachine:
    a: IntPoint2
    b: IntPoint2
    prize: IntPoint2

def getInput(s:str) -> list[ClawMachine]:
    filename = common.getFilePath(s)
    with open(filename, "r") as file:
        machines: list[ClawMachine] = []
        while line := file.readline():
            line = line.strip()
            if line == "": break
            ints:list[int] = [int(x) for x in line.split(" ")]
            a = IntPoint2(ints[0], ints[1])
            b = IntPoint2(ints[2], ints[3])
            prize = IntPoint2(ints[4], ints[5])
            machines.append(ClawMachine(a, b, prize))
        
    return machines

def bestValue(machine: ClawMachine) -> int:
    """
    Find all values of a0, b0 that satisfy the equations:

    ```
    prize.x = a.x * a0 + b.x * b0
    prize.y = a.y * a0 + b.y * b0
    ```
    """

    a = machine.a
    b = machine.b
    prize = machine.prize
    price = float('inf')
    for a0 in range(100):
        for b0 in range(100):
            if prize.x == a.x * a0 + b.x * b0 and prize.y == a.y * a0 + b.y * b0:
                price = min(price, 3 * a0 + b0)
            
    return price

def solution1(machines: list[ClawMachine]) -> int:
    totalCost = 0
    for m in machines:
        cost = bestValue(m)
        if cost != float('inf'):
            totalCost += cost

    return totalCost

def bestValue2(machine: ClawMachine) -> int:
    """
    Find all values of a0, b0 that satisfy the equations:

    ```
    10000000000000 + prize.x = a.x * a0 + b.x * b0
    10000000000000 + prize.y = a.y * a0 + b.y * b0
    ```
    """

    a = machine.a
    b = machine.b
    prize = machine.prize + IntPoint2(10000000000000, 10000000000000)

    # Use linear algebra to solve the equations
    det = a.x * b.y - a.y * b.x
    if det == 0:
        raise ValueError("No unique solution (determinant is zero)")
    
    x = (prize.x * b.y - prize.y * b.x) / det
    y = (a.x * prize.y - a.y * prize.x) / det

    if x == int(x) and y == int(y):
        return 3 * int(x) + int(y)
            
    return 0

def solution2(machines: list[ClawMachine]) -> int:
    totalCost = 0
    for m in machines:
        totalCost += bestValue2(m)

    return totalCost

test = getInput("input13_test.txt")
input = getInput("input13.txt")

print("Test cases:")
print(f"S1: {solution1(test)}")
print(f"S2: {solution2(test)}")

print("Solutions:")
print(f"S1: {solution1(input)}")
print(f"S2: {solution2(input)}")