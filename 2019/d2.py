# adventofcode.com
# Day 2
# https://adventofcode.com/2019/day/2

import array, common

OP_ADD = 1
OP_MUL = 2
OP_END = 99

def processIntcode(program, addr):
  op = program[addr]
  if op == OP_END: return (False, "SUCCESS")
  aLoc = program[addr+1]
  bLoc = program[addr+2]
  rLoc = program[addr+3]
  aVal = program[aLoc]
  bVal = program[bLoc]

  if op == OP_ADD:
    program[rLoc] = aVal + bVal
    return (True, "ADD")
  
  if op == OP_MUL:
    program[rLoc] = aVal * bVal
    return (True, "MUL")
  
  return (False, "INVALID OP: %d" % op)

def loadProgram(path, noun, verb, separator=','):
  program = []
  for n in open(path, 'r').readline().split(separator):
    program.append(int(n))
  
  program[1] = noun
  program[2] = verb
  return program

def runProgram(program):
  addr = 0
  while processIntcode(program, addr)[0]:
    addr += 4
  return program[0]

PROGRAM_PATH = common.getFilePath('input2.txt')

program = loadProgram(PROGRAM_PATH, 12, 2)
print(runProgram(program))

TARGET_VALUE = 19690720

for noun in range(0,99):
  for verb in range(0,99):
    program = loadProgram(PROGRAM_PATH, noun, verb)
    if runProgram(program) == TARGET_VALUE:
      print(100*noun+verb)
      break
