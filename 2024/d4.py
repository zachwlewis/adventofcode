# adventofcode.com
# Day 4
# https://adventofcode.com/2024/day/4

import common

def getTestInput() -> list[str]:
    filename = common.getFilePath("input4_test.txt")
    with open(filename, "r") as file:
        return [line.strip() for line in file]

def getInput() -> list[str]:
    filename = common.getFilePath("input4.txt")
    with open(filename, "r") as file:
        return [line.strip() for line in file]

def findXmasCount(puzzle: list[str]) -> int:
    """
    Returns the number of instances of "XMAS" in the puzzle. The target
    can be found in the puzzle in any orientation.

    Instead of checking each orientation, we can check
    - forward
    - down
    - forward-down diagonal
    - back-down diagonal
    
    Then, check if the string is either the target or the reverse of the target.
    """
    width = len(puzzle[0])
    height = len(puzzle)
    target_length = 4
    target = "XMAS"
    target_reversed = "SAMX"

    count = 0
    for i in range(height):
        for j in range(width):
            f, d, fd, bd = "", "", "", ""
            # forward
            if j + target_length - 1 < width:
                f = puzzle[i][j:j + target_length]
            # down
            if i + target_length - 1 < height:
                d = "".join([puzzle[i + k][j] for k in range(4)])
                
            # forward-down diagonal
            if i + target_length - 1 < height and j + target_length - 1 < width:
                fd = "".join([puzzle[i + k][j + k] for k in range(4)])

            # back-down diagonal
            if i + target_length - 1 < height and j - target_length + 1 >= 0:
                bd = "".join([puzzle[i + k][j - k] for k in range(4)])
            
            if f == target or f == target_reversed:
                count += 1
            if d == target or d == target_reversed:
                count += 1
            if fd == target or fd == target_reversed:
                count += 1
            if bd == target or bd == target_reversed:
                count += 1

    return count

def findMasKernel(puzzle: list[str]) -> int:
    """
    Find all instances of the following kernel in the puzzle:

    ```
    M.S
    .A.
    M.S
    ```
    """
    count = 0
    width = len(puzzle[0])
    height = len(puzzle)

    forward_match = ("M","S")
    backward_match = ("S","M")

    for i in range(1,height - 1):
        for j in range(1, width - 1):
            if puzzle[i][j] != "A": continue # Skip if the center is not "A"

            # Check the kernel
            d1 = (puzzle[i-1][j-1],puzzle[i+1][j+1])
            d2 = (puzzle[i-1][j+1],puzzle[i+1][j-1])

            if (d1 == forward_match or d1 == backward_match) and (d2 == forward_match or d2 == backward_match):
                count += 1

    return count

test = getTestInput()
input = getInput()

print("Test cases:")
print(f"S1: {findXmasCount(test)}")
print(f"S2: {findMasKernel(test)}")

print("Solutions:")
print(f"S1: {findXmasCount(input)}")
print(f"S2: {findMasKernel(input)}")