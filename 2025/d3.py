# adventofcode.com
# Day 3
# https://adventofcode.com/2025/day/3

import common

def parseInput(value: list[str]) -> list[list[int]]:
    parsed: list[list[int]] = []
    for line in value:
        parsed.append([int(x) for x in line.strip()])
    return parsed

def calcBankJoltage(bank: list[int]) -> int:
    a, b = 0, 0
    size = len(bank)
    for i in range(size-1):
        if bank[i] > a:
            a = bank[i]
            b = bank[i+1]
        elif bank[i+1] > b:
            b = bank[i+1]

    return 10 * a + b

def calcLargeBankJoltage(bank: list[int]) -> int:
    windowSize = 12
    b = bank[:windowSize]
    size = len(bank)
    for i in range(size - windowSize):
        print(i, bank[i:i+windowSize])
        start = i - size - windowSize
        print(start)
        for j in range(0, windowSize):
            if bank[i+j] > b[j]:
                b = bank[i+j:i+j+windowSize]

    print(b)
    return 10

sampleData = [
    "987654321111111",
    "811111111111119",
    "234234234234278",
    "818181911112111"
]

sampleInput = parseInput(sampleData)

filename = common.getFilePath("input3.txt")
input = []
with open(filename, "r") as file:
    input = parseInput(file.readlines())

s1, s2 = 0, 0

calcLargeBankJoltage(sampleInput[2])

# for line in sampleInput:
#     s1 += calcBankJoltage(line)
#     s2 += calcLargeBankJoltage(line)

print(f"S1: {s1}")
print(f"S2: {s2}")
