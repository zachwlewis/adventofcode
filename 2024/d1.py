# adventofcode.com
# Day 1
# https://adventofcode.com/2024/day/1

import common, math, re

def getInput() -> tuple[list[int], list[int]]:
    filename = common.getFilePath("input1.txt")
    list1 = []
    list2 = []
    with open(filename, "r") as file:
        match = re.compile(r"(\d+)\s+(\d+)")
        for line in file:
            m = match.match(line)
            list1.append(int(m.group(1)))
            list2.append(int(m.group(2)))
    return list1, list2

def sortedDifference(lhs:list[int], rhs:list[int]) -> int:
    lhs.sort()
    rhs.sort()
    sum = 0
    for i in range(len(lhs)):
        sum += abs(lhs[i] - rhs[i])
    return sum

def similarity(lhs:list[int], rhs:list[int]) -> int:
    """Calculate a total similarity score by adding up each number in the left
    list after multiplying it by the number of times that number appears in the
    right list."""
    rmap = {}
    for n in rhs:
        if n in rmap:
            rmap[n] += 1
        else:
            rmap[n] = 1

    sum = 0
    for n in lhs:
        if n in rmap:
            sum += n * rmap[n]
    return sum

test1 = [3,4,2,1,3,3]
test2 = [4,3,5,3,9,3]
print("Test cases:")
print(f"S1: {sortedDifference(test1, test2)}")
print(f"S2: {similarity(test1, test2)}")

list1, list2 = getInput()

print("Solutions:")
print(f"S1: {sortedDifference(list1, list2)}")
print(f"S2: {similarity(list1, list2)}")