# adventofcode.com
# Day 5
# https://adventofcode.com/2019/day/5

import common

OP_ADD  = 1
OP_MUL  = 2
OP_IN   = 3
OP_OUT  = 4
OP_JMP  = 5
OP_NJMP = 6
OP_LESS = 7
OP_EQL  = 8
OP_END  = 99

def processOpcode(opcode):
  s = '%05d' % opcode
  return [int(s[3:]), int(s[2]), int(s[1]), int(s[0])]

def executeInstruction(program, addr):
  opcode = processOpcode(program[addr])
  op = opcode[0]
  if op == OP_END: return -1

  aLoc = program[addr+1]
  aVal = aLoc if opcode[1] else program[aLoc]

  if op == OP_IN:
    program[aLoc] = int(input("<= "))
    return addr+2

  if op == OP_OUT:
    print("=> %d" % aVal)
    return addr+2

  bLoc = program[addr+2]
  bVal = bLoc if opcode[2] else program[bLoc]

  if op == OP_JMP:
    # jump if true
    return bVal if aVal else addr+3

  if op == OP_NJMP:
    # jump if false
    return bVal if not aVal else addr+3

  rLoc = program[addr+3]
  
  if op == OP_ADD:
    program[rLoc] = aVal + bVal
    return addr+4
  
  if op == OP_MUL:
    program[rLoc] = aVal * bVal
    return addr+4

  if op == OP_LESS:
    # less than
    program[rLoc] = 1 if aVal < bVal else 0
    return addr+4

  if op == OP_EQL:
    # equal
    program[rLoc] = 1 if aVal == bVal else 0
    return addr+4
  
  return -1

def loadProgram(path, separator=','):
  program = []
  for n in open(path, 'r').readline().split(separator):
    program.append(int(n))
    
  return program

def runProgram(program):
  addr = executeInstruction(program, 0)
  while addr > 0: addr = executeInstruction(program, addr)
  return program[0]

PROGRAM_PATH = common.getFilePath('input5.txt')

runProgram(loadProgram(PROGRAM_PATH))
