# adventofcode.com
# Day 15
# https://adventofcode.com/2024/day/15

import common
from dataclasses import dataclass
from point import IntPoint2
from grid import Grid

UP = IntPoint2(0, -1)
DOWN = IntPoint2(0, 1)
LEFT = IntPoint2(-1, 0)
RIGHT = IntPoint2(1, 0)

@dataclass
class Box:
    left:IntPoint2
    right:IntPoint2
    def __hash__(self):
        return hash((self.left, self.right))
    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

@dataclass
class State:
    walls: set[IntPoint2]
    boxes: set[Box]
    robot: IntPoint2
    size: IntPoint2

def getInput(s:str) -> tuple[Grid[str], list[IntPoint2]]:
    filename = common.getFilePath(s)
    with open(filename, "r") as file:
        warehouse_data = []
        while line := file.readline():
            line = line.strip()
            if line == "": break
            warehouse_data.append(line)

        move_data:str = ""
        while line:= file.readline():
            move_data += line.strip()

        warehouse = Grid(warehouse_data)

        moves:list[IntPoint2] = []
        for s in move_data:
            if s == "^": moves.append(UP)
            if s == "v": moves.append(DOWN)
            if s == "<": moves.append(LEFT)
            if s == ">": moves.append(RIGHT)

    return warehouse, moves

def move(warehouse:Grid[str], pos:IntPoint2, m:IntPoint2) -> bool:
    target = warehouse[pos.t]
    if target == "#": return False # can't move
    next_space = pos + m

    if warehouse[next_space.t] == "#": return False # can't move
    if warehouse[next_space.t] == ".":
        # empty space. perform the move.
        warehouse[pos.t] = "."
        warehouse[next_space.t] = target
        return True
    
    if warehouse[next_space.t] == "O":
        # move to open space
        if move(warehouse, next_space, m):
            warehouse[pos.t] = "."
            warehouse[next_space.t] = target
            return True
        return False
    
def move2(warehouse:Grid[str], pos:IntPoint2, m:IntPoint2) -> bool:
    target = warehouse[pos.t]
    if target == "#": return False # can't move
    next_space = pos + m

    if warehouse[next_space.t] == "#": return False # can't move
    if warehouse[next_space.t] == ".":
        # empty space. perform the move.
        warehouse[pos.t] = "."
        warehouse[next_space.t] = target
        return True
    
    if warehouse[next_space.t] == "O":
        # move to open space
        if move(warehouse, next_space, m):
            warehouse[pos.t] = "."
            warehouse[next_space.t] = target
            return True
        return False
    
    if warehouse[next_space.t] == "[": # large crate left
        # handle large crate
        pass

    if warehouse[next_space.t] == "]": # large crate right
        # handle large crate
        pass
    
def sumGPS(w:Grid[str]) -> int:
    smallCrates = w.findAll("O")
    largeCrate = w.findAll("[")
    crates = smallCrates + largeCrate
    score = 0
    for c in crates:
        score += 100 * c[1] + c[0]
    return score

def solution1(w:Grid[str], m:list[IntPoint2]) -> int:
    while len(m) > 0:
        r = IntPoint2()
        r.t = w.find("@")
        move(w, r, m.pop(0))

    return sumGPS(w)

def expandWarehouse(w:Grid[str]) -> Grid[str]:
    new_width = w.width * 2
    new_data = []
    for d in w._grid:
        if d == "#": new_data += ["#", "#"]
        if d == ".": new_data += [".", "."]
        if d == "O": new_data += ["[", "]"]
        if d == "@": new_data += ["@", "."]
    
    g = Grid(new_width,w.height,0)
    g._grid = new_data

    return g

def getState(w:Grid[str]) -> State:
    walls:set[IntPoint2] = set()
    boxes:set[IntPoint2] = set()
    rt = w.find("@")
    robot:IntPoint2 = IntPoint2(rt[0] * 2, rt[1])
    size = IntPoint2(w.width * 2, w.height)
    boxes = [Box(IntPoint2(x*2,y),IntPoint2(x*2+1,y)) for x,y in w.findAll("O")]
    for wall in w.findAll("#"):
        walls.add(IntPoint2(wall[0] * 2, wall[1]))
        walls.add(IntPoint2(wall[0] * 2 + 1, wall[1]))
           
    return State(walls, boxes, robot, size)

def printState(s:State) -> None:
    grid = gridState(s)
    print(grid)

def gridState(s:State) -> Grid[str]:
    grid: Grid[str] = Grid(s.size.x, s.size.y, ".")
    for wall in s.walls:
        grid[wall.t] = "#"
    for box in s.boxes:
        grid[box.left.t] = "["
        grid[box.right.t] = "]"
    grid[s.robot.t] = "@"
    return grid

def moveState(s:State, m:IntPoint2) -> None:
    next_position = s.robot + m
    if next_position in s.walls: return # ran into a wall
    moved_boxes = set()
        
    for box in s.boxes:
        if box.left == next_position or box.right == next_position:
            # ran into a box
            # check if the box can move
            can_move, mb = canMoveBox(s, box, m)
            moved_boxes.update(mb)
            if not can_move:
                #print(f"Ran into box: {box}. Can't move.")
                #print(f"Bumped boxes: {moved_boxes}")
                return # can't move all boxes
            else:
                #print(f"Ran into box: {box}. Can move.")
                #print(f"Moved boxes: {moved_boxes}")
                break
    
    for box in moved_boxes:
        box.left += m
        box.right += m

    s.robot = next_position

def canMoveBox(s:State, b:Box, m:IntPoint2) -> tuple[bool,set[Box]]:
    nl, nr = b.left + m, b.right + m
    moved_boxes = set([b])
    if nl in s.walls or nr in s.walls: return False, set() # ran into a wall
    can_move_right, can_move_left = True, True
    for box in s.boxes:
        if box == b: continue
        if box.left == nl or box.left == nr:
            # collision with left side of box
            #print(f"--Collision with left side of box: {box}")
            can_move_left, bs = canMoveBox(s, box, m)
            moved_boxes.update(bs)
        if box.right == nl or box.right == nr:
            # collision with right side of box
            #print(f"--Collision with right side of box: {box}")
            can_move_right, bs = canMoveBox(s, box, m)
            moved_boxes.update(bs)

    return (can_move_left and can_move_right, moved_boxes)

def solution2(w:Grid[str], m:list[IntPoint2]) -> int:
    state = getState(w)
    while len(m) > 0:
        moveState(state, m.pop(0))

    printState(state)
    return sumGPS(gridState(state))

w1:Grid[str]
m1:list[IntPoint2]

w2:Grid[str]
m2:list[IntPoint2]

wi:Grid[str]
wm:list[IntPoint2]
w1, m1 = getInput("input15_test1.txt")
w2, m2 = getInput("input15_test2.txt")
wi, wm = getInput("input15.txt")

print("Test cases:")
print(f"S1: {solution1(w1.copy(),m1.copy())}")
print(f"S2: {solution2(w1,m1)}")

print("Solutions:")
print(f"S1: {solution1(wi.copy(),wm.copy())}")
print(f"S2: {solution2(wi,wm)}")

# interative solution
# warehouse, moves = w1, m1
# state = getState(warehouse)
# while len(moves) > 0 and input("") != "q":
#         moveState(state, moves.pop(0))
#         printState(state)
#         if len(moves) > 0:
#             if moves[0] == UP: print("Next: ^")
#             if moves[0] == DOWN: print("Next: v")
#             if moves[0] == LEFT: print("Next: <")
#             if moves[0] == RIGHT: print("Next: >")

# print(sumGPS(gridState(state)))