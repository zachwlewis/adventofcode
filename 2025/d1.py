# adventofcode.com
# Day 1
# https://adventofcode.com/2025/day/1

import common, re

def getInput() -> list[tuple[str,int]]:
    filename = common.getFilePath("input1.txt")
    input = []
    with open(filename, "r") as file:
        match = re.compile(r"(\w)(\d+)")
        for line in file:
            m = match.match(line)
            input.append((m.group(1), int(m.group(2))))
    return input

print("hello world")
input = getInput()
dial = 50
zeros = 0
zeros2 = 0

for direction, amount in input:
    if direction == 'L': dial -= amount
    else: dial += amount
    while dial < 0:
        dial += 100
    while dial > 99:
        dial -= 100
    
    if dial == 0:
        zeros += 1

print(f"S1: {zeros}")

dial = 50
dir = 0
for direction, amount in input:
    if direction == 'L': dir = -1
    else: dir = 1
    for _ in range(amount):
        dial += dir
        
        if dial < 0:
            dial = 99
        elif dial > 99:
            dial = 0

        if dial == 0: zeros2 += 1

print(f"S2: {zeros2}")