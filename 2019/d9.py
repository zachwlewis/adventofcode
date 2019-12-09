# adventofcode.com
# Day 9
# https://adventofcode.com/2019/day/9

import common

from itertools import permutations
from typing import Dict, List
Program = Dict[int, int]
Vector = List[int]

# OPERATION CODES
OP_ADD  = 1
OP_MUL  = 2
OP_IN   = 3
OP_OUT  = 4
OP_JNZ  = 5
OP_JZ   = 6
OP_LT   = 7
OP_EQ   = 8
OP_ARB  = 9
OP_END  = 99

NUM_ARGS = {OP_ADD:3, OP_MUL:3, OP_IN: 1, OP_OUT: 1, OP_JNZ: 2, OP_JZ: 2, OP_LT: 3, OP_EQ: 3, OP_ARB: 1, OP_END: 0}

# ERROR CODES
ERR_NONE = 0
ERR_INPUT = 3
ERR_SUCCESS = 99

# PARAMETER MODES
PM_ADR = 0
PM_VAL = 1
PM_REL = 2

PROGRAM_PATH = common.getFilePath('input9.txt')

class Status:
  def __init__(self,addr,err):
    self.addr = addr
    self.err = err

class Operation:
  def __init__(self, value: int):
    self.s = '%05d' % value
    self.code = int(self.s[3:])
    self.mode = [int(self.s[2]), int(self.s[1]), int(self.s[0])]

class Thread:
  MAX_ID = 0
  def __init__(self, program: Program):
    self.program = program
    self.addr = 0
    self.istream = []
    self.ostream = []
    self.status = Status(0, ERR_NONE)
    self.id = Thread.MAX_ID
    self.relativeBase = 0
    self.interactive = False
    self.verbose = False
    Thread.MAX_ID += 1

  def process(self):
    self.status = executeThread(self)
    self.addr = self.status.addr

def getValueAtAddress(program: Program, addr: int, mode: int, relativeBase: int) -> int:
  if mode == PM_ADR: return program.get(addr, 0)
  elif mode == PM_REL: return program.get(relativeBase + addr, 0)
  
  return addr

def outputValue(addr: int, value: int, relativeBase: int, mode: int) -> str:
  if mode == PM_ADR: return "[%d] %d" % (addr, value)
  if mode == PM_REL: return "<%d> %d" % (relativeBase+addr, value)
  
  return "%d" % (value)
  

def executeThread(thread: Thread):
  opcode = Operation(thread.program[thread.addr])
  op = opcode.code
  addrs = []
  vals = []

  for i in range(NUM_ARGS[op]):
    addr = thread.program[thread.addr+i+1]
    addrs.append(addr)
    vals.append(getValueAtAddress(thread.program,addr,opcode.mode[i],thread.relativeBase))

  if op == OP_END:
    if thread.verbose: print("%d\t%s\tEND" % (thread.addr, opcode.s))
    return Status(thread.addr, ERR_SUCCESS)

  write_address =  addrs[0] if opcode.mode[0] != PM_REL else addrs[0] + thread.relativeBase
  aOut = outputValue(addrs[0], vals[0], thread.relativeBase, opcode.mode[0])

  if op == OP_IN:
    if thread.verbose: print("%d\t%s\tIN\t%s" % (thread.addr, opcode.s, write_address))
    if len(thread.istream):
      i = int(thread.istream.pop(0))
      if thread.verbose: print("<= %d *istream" % i)
      thread.program[write_address] = i
    elif thread.interactive: thread.program[write_address] = int(input("<= "))
    else: return Status(thread.addr, ERR_INPUT)
    return Status(thread.addr+2, ERR_NONE)

  if op == OP_OUT:
    thread.ostream.append(vals[0])
    if thread.verbose: print("%d\t%s\tOUT\t%s" % (thread.addr, opcode.s, aOut))
    if thread.verbose or thread.interactive: print("=> %d" % vals[0])
    return Status(thread.addr+2, ERR_NONE)

  if op == OP_ARB:
    if thread.verbose: print("%d\t%s\tARB\t%s" % (thread.addr, opcode.s, aOut))
    thread.relativeBase += vals[0]
    return Status(thread.addr+2, ERR_NONE)

  bOut = outputValue(addrs[1], vals[1], thread.relativeBase, opcode.mode[1])

  if op == OP_JNZ:
    # jump if value is not zero
    if thread.verbose: print("%d\t%s\tJNZ\t%s\t%s" % (thread.addr, opcode.s, aOut, bOut))
    
    return Status(vals[1] if vals[0] else thread.addr+3, ERR_NONE)

  if op == OP_JZ:
    # jump if value is zero
    if thread.verbose: print("%d\t%s\tJZ\t%s\t%s" % (thread.addr, opcode.s, aOut, bOut))
    return Status(vals[1] if not vals[0] else thread.addr+3, ERR_NONE)

  write_address =  addrs[2] if opcode.mode[2] != PM_REL else addrs[2] + thread.relativeBase
  rOut = write_address
  
  if op == OP_ADD:
    if thread.verbose: print("%d\t%s\tADD\t%s\t%s\t%s" % (thread.addr, opcode.s, aOut, bOut, rOut))
    thread.program[write_address] = vals[0] + vals[1]
    return Status(thread.addr+4, ERR_NONE)
  
  if op == OP_MUL:
    if thread.verbose: print("%d\t%s\tMUL\t%s\t%s\t%s" % (thread.addr, opcode.s, aOut, bOut, rOut))
    thread.program[write_address] = vals[0] * vals[1]
    return Status(thread.addr+4, ERR_NONE)

  if op == OP_LT:
    # less than
    if thread.verbose: print("%d\t%s\tLT\t%s\t%s\t%s" % (thread.addr, opcode.s, aOut, bOut, rOut))
    thread.program[write_address] = 1 if vals[0] < vals[1] else 0
    return Status(thread.addr+4, ERR_NONE)

  if op == OP_EQ:
    # equal
    if thread.verbose: print("%d\t%s\tEQ\t%s\t%s\t%s" % (thread.addr, opcode.s, aOut, bOut, rOut))
    thread.program[write_address] = 1 if vals[0] == vals[1] else 0
    return Status(thread.addr+4, ERR_NONE)
  
  return Status(thread.addr, op)

def loadProgram(path: str, separator: str = ',') -> Program:
  program = dict()
  addr = 0
  for n in open(path, 'r').readline().split(separator):
    program[addr] = int(n)
    addr += 1
    
  return program

def runTest() -> Vector:
  thread = Thread(loadProgram(PROGRAM_PATH))
  thread.interactive = False
  thread.verbose = False
  thread.istream.append(1)
  while thread.status.err == ERR_NONE:
      thread.process()

  return thread.ostream

def sensorBoost() -> Vector:
  thread = Thread(loadProgram(PROGRAM_PATH))
  thread.istream.append(2)
  while thread.status.err == ERR_NONE:
      thread.process()

  return thread.ostream


print(runTest())
print(sensorBoost())
