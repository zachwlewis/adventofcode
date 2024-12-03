# adventofcode.com
# Day 3
# https://adventofcode.com/2024/day/3

import common, re

def getInput() -> list[str]:
    filename = common.getFilePath("input3.txt")
    with open(filename, "r") as file:
        return [line.strip() for line in file]

def sumValidMultiplications(strings:list[str]) -> int:
    """Returns the sum of the valid multiplications in the string."""
    # Find all the valid multiplications in the string.
    for s in strings:
        matches = re.findall(r"mul\((\d+),(\d+)\)", s)
        # Sum the valid multiplications.
        total = 0
        for match in matches:
            total += int(match[0]) * int(match[1])
    return total

def correctedLineSum(strings:list[str]) -> int:
    commands = re.compile(r"(do\(\)|mul\(\d+,\d+\)|don't\(\))")
    should_add = True
    total = 0
    for s in strings:
        matches = re.findall(commands, s)
        
        for match in matches:
            if match == "do()":
                should_add = True
            elif match == "don't()":
                should_add = False
            elif should_add:
                digits = re.compile(r"(\d+),(\d+)")
                nums = digits.findall(match)
                total += int(nums[0][0]) * int(nums[0][1])

    return total

test1 = ["xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"]
test2 = ["xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"]
input = getInput()

print("Test cases:")
print(f"S1: {sumValidMultiplications(test1)}")
print(f"S2: {correctedLineSum(test2)}")

print("Solutions:")
print(f"S1: {sumValidMultiplications(input)}")
print(f"S2: {correctedLineSum(input)}")