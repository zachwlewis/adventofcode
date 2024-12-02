# adventofcode.com
# Day 2
# https://adventofcode.com/2024/day/2

import common, math, re

def getInput() -> list[int]:
    filename = common.getFilePath("input2.txt")
    reports = []
    with open(filename, "r") as file:
        for line in file:
            report = [int(x) for x in line.split()]
            reports.append(report)
    return reports

def isSafe(report:list[int]) -> bool:
    """Returns True if the report is safe, False otherwise.
    A report only counts as safe if both of the following are true:
    - The levels are either all increasing or all decreasing.
    - Any two adjacent levels differ by at least one and at most three.
    """

    # Check if the levels are either all increasing or all decreasing.
    increasing = True
    decreasing = True
    for i in range(1, len(report)):
        alpha = report[i] - report[i - 1]
        if alpha == 0 or abs(alpha) > 3:
            return False
        if alpha > 0:
            decreasing = False
        else:
            increasing = False

    return increasing or decreasing

def safeReportCount(reports: list[list[int]]) -> int:
    """Returns the number of safe reports in the list of reports."""
    count = 0
    for report in reports:
        if isSafe(report):
            count += 1
    return count

def safeReportCountWithDampener(reports: list[list[int]]) -> int:
    """Returns the number of safe reports in the list of reports with the safety
    dampener applied."""
    count = 0
    for report in reports:
        if isSafe(report):
            count += 1
        else:
            for i in range(0, len(report)):
                # Remove the item at index i and check if the report is safe.
                if isSafe(report[:i] + report[i + 1:]):
                    count += 1
                    break
    return count
    
test = [[7, 6, 4, 2, 1],
[1, 2, 7, 8, 9],
[9, 7, 6, 2, 1],
[1, 3, 2, 4, 5],
[8, 6, 4, 4, 1],
[1, 3, 6, 7, 9]]

reports = getInput()

print("Test cases:")
print(f"S1: {safeReportCount(test)}")
print(f"S2: {safeReportCountWithDampener(test)}")

print("Solutions:")
print(f"S1: {safeReportCount(reports)}")
print(f"S2: {safeReportCountWithDampener(reports)}")