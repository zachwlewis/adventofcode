# adventofcode.com
# Day 14
# https://adventofcode.com/2024/day/14

import common
from dataclasses import dataclass
from point import IntPoint2
from grid import Grid
from PIL import Image

@dataclass
class Robot:
    p: IntPoint2
    v: IntPoint2

def getInput(s:str) -> list[Robot]:
    filename = common.getFilePath(s)
    with open(filename, "r") as file:
        robots: list[Robot] = []
        while line := file.readline():
            line = line.strip()
            if line == "": break
            ints:list[int] = [int(x) for x in line.split(" ")]
            p = IntPoint2(ints[0], ints[1])
            v = IntPoint2(ints[2], ints[3])
            robots.append(Robot(p, v))
        
    return robots

def evaluatePosition(robot:Robot, time:int, bounds:IntPoint2) -> IntPoint2:
    p = robot.p + robot.v * time
    p.x = p.x % bounds.x
    p.y = p.y % bounds.y
    return p

def solution1(robots:list[Robot], bounds:IntPoint2) -> int:
    midpoint = bounds // 2
    q1, q2, q3, q4 = 0, 0, 0, 0
    for robot in robots:
        p = evaluatePosition(robot, 100, bounds)
        if p.x < midpoint.x:
            if p.y < midpoint.y:
                q1 += 1
            elif p.y > midpoint.y:
                q2 += 1
        elif p.x > midpoint.x:
            if p.y < midpoint.y:
                q3 += 1
            elif p.y > midpoint.y:
                q4 += 1
    return q1 * q2 * q3 * q4

def isBalanced(robots:list[Robot], time:int, bounds:IntPoint2) -> bool:
    midpoint = bounds // 2
    left,right = 0, 0
    for robot in robots:
        p = evaluatePosition(robot, time, bounds)
        if p.x < midpoint.x:
            left += 1
        elif p.x > midpoint.x:
            right += 1
    return left == right

def printTime(robots:list[Robot], time:int, bounds:IntPoint2) -> None:
    g = Grid(bounds.x, bounds.y, ".")
    for robot in robots:
        p = evaluatePosition(robot, time, bounds)
        g[p.t] = 'X'

    print(g)

def saveImage(robots:list[Robot], time:int, bounds:IntPoint2, filename:str) -> None:
    img = Image.new("L", (bounds.x, bounds.y))
    pixels = img.load()
    for robot in robots:
        p = evaluatePosition(robot, time, bounds)
        pixels[p.t] = 255
    img.save(filename)

test = getInput("input14_test.txt")
inpt = getInput("input14.txt")

print("Test cases:")
print(f"S1: {solution1(test, IntPoint2(11, 7))}")
#print(f"S2: {solution2(test)}")

print("Solutions:")
print(f"S1: {solution1(inpt, IntPoint2(101,103))}")
print(f"S2: 7286")


#for t in range (103 * 101 + 1):
#    saveImage(inpt, t, IntPoint2(101, 103), f"2024/output14/{t}.png")
