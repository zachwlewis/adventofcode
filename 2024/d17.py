# adventofcode.com
# Day 17
# https://adventofcode.com/2024/day/17

from dataclasses import dataclass
from point import IntPoint2
from grid import Grid

@dataclass
class Computer:
    A: int
    B: int
    C: int
    ptr: int
    program: list[int]
    output: list[int]

def tick(computer:Computer) -> bool:
    if computer.ptr + 1 >= len(computer.program): return False # not running
    
    opcode = computer.program[computer.ptr]
    operand = computer.program[computer.ptr + 1]
    value = 0
    if operand < 4: value = operand
    elif operand == 4: value = computer.A
    elif operand == 5: value = computer.B
    elif operand == 6: value = computer.C
    else: 
        raise ValueError(f"Invalid operand: {operand}")
    
    if opcode == 0: # adv (division)
        computer.A //= 2 ** value
    elif opcode == 1: # bxl (bitwise XOR)
        # bitwise xor of B and value
        computer.B ^= operand
    elif opcode == 2: # bst
        computer.B = value % 8
    elif opcode == 3: # jnz
        if computer.A != 0:
            computer.ptr = value
            return True # still running
    elif opcode == 4: # bxc
        computer.B ^= computer.C
    elif opcode == 5: # out
        computer.output.append(value % 8)
    elif opcode == 6: # bdv
        computer.B = computer.A // (2 ** value)
    elif opcode == 7: # cdv
        computer.C = computer.A // (2 ** value)
    else:
        raise ValueError(f"Invalid opcode: {opcode}")
    
    computer.ptr += 2
    return True # still running

def solution1(computer:Computer) -> str:
    while tick(computer): pass
    return ",".join([str(x) for x in computer.output])

def printComputer(computer:Computer) -> None:
    print(f"A: {computer.A}\nB: {computer.B}\nC: {computer.C}")
    print(f"{2*computer.ptr*"-"}v")
    print(",".join([str(x) for x in computer.program]))
    print(">" + ",".join([str(x) for x in computer.output]))
    print()


test = Computer(729,0,0,0,[0,1,5,4,3,0],[])
test2 = Computer(2024,0,0,0,[0,3,5,4,3,0],[])
inpt = Computer(33940147,0,0,0,[2,4,1,5,7,5,1,6,4,2,5,5,0,3,3,0],[])

aval = 0
while inpt.program != inpt.output:
    inpt.output.clear()
    inpt.A = aval
    inpt.B = 0
    inpt.C = 0
    inpt.ptr = 0
    while tick(inpt): pass
    #print(f"A: {aval}", end="\r")
    aval += 1
print(f"A: {aval}")
print("Test cases:")
print(f"S1: {solution1(test)}")
# print(f"S2: {solution2(w1,m1)}")

print("Solutions:")
print(f"S1: {solution1(inpt)}")
# print(f"S2: {solution2(wi,wm)}")

