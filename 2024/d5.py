# adventofcode.com
# Day 5
# https://adventofcode.com/2024/day/5

import common

def getInput(s:str) -> tuple[list[tuple[int,int]],list[list[int]]]:
    filename = common.getFilePath(s)
    rules = []
    changes = []
    with open(filename, "r") as file:
        # read rules until the first empty line
        line = file.readline()
        while line != "\n":
            rule = tuple([int(x) for x in line.split("|")])
            rules.append(rule)
            line = file.readline()
        # read changes until the end of the file
        for line in file:
            change = [int(x) for x in line.split(',')]
            changes.append(change)

    return (rules,changes)

def scoreOrderList(data: tuple[list[tuple[int,int]],list[list[int]]]) -> int:
    good, bad = validateChanges(data[0], data[1])
    score = 0
    for change in good:
        score += change[len(change)//2]

    return score

def validateChanges(rules: list[tuple[int,int]], changes: list[list[int]]) -> tuple[list[list[int]], list[list[int]]]:
    good, bad = [], []
    for change in changes:
        valid = True
        for rule in rules:
            try:
                a = change.index(rule[0])
                b = change.index(rule[1])
            except ValueError:
                # rule not applicable
                continue
            if a > b:
                # rule failed
                valid = False
                break
        
        if valid: good.append(change)
        else: bad.append(change)
    return good, bad

def fixOrderList(data: tuple[list[tuple[int,int]],list[list[int]]]) -> int:
    good, bad = validateChanges(data[0], data[1])
    rules = data[0]
    score = 0
    for change in bad:
        fixed = False
        while not fixed: # brute force until fixed
            fixed = True
            for rule in rules:
                try:
                    a = change.index(rule[0])
                    b = change.index(rule[1])
                except ValueError:
                    # rule not applicable
                    continue
                if a > b:
                    # rule failed
                    change[a], change[b] = change[b], change[a]
                    fixed = False
                    break
            
        score += change[len(change)//2]

    return score

test = getInput("input5_test.txt")
input = getInput("input5.txt")

print("Test cases:")
print(f"S1: {scoreOrderList(test)}")
print(f"S2: {fixOrderList(test)}")

print("Solutions:")
print(f"S1: {scoreOrderList(input)}")
print(f"S2: {fixOrderList(input)}")