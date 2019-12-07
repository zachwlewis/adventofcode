# adventofcode.com
# Day 7
# https://adventofcode.com/2019/day/7

import common

from itertools import permutations

# OPERATION CODES
OP_ADD  = 1
OP_MUL  = 2
OP_IN   = 3
OP_OUT  = 4
OP_JMP  = 5
OP_NJMP = 6
OP_LESS = 7
OP_EQL  = 8
OP_END  = 99

# ERROR CODES
ERR_NONE = 0
ERR_INPUT = 3
ERR_SUCCESS = 99

PROGRAM_PATH = common.getFilePath('input7.txt')

class Status:
  def __init__(self,addr,err):
    self.addr = addr
    self.err = err

def parseOpcode(opcode):
  s = '%05d' % opcode
  return [int(s[3:]), int(s[2]), int(s[1]), int(s[0])]

def executeInstruction(program, addr, istream = [], ostream = [], verbose = False, interactive = False, thread = -1):
  """
  Reads from an Intcode program at a given address, executes the instruction and returns a status.
  
  ---

  - The verbose flag prints debug output.
  - The interactive flag will prompt the user for input if the input stream is empty.
  - A thread id can be specified for debugging purposes.
  """

  opcode = parseOpcode(program[addr])
  op = opcode[0]
  if op == OP_END:
    if verbose: print("END t_%d" % thread)
    return Status(addr, ERR_SUCCESS)

  aLoc = program[addr+1]
  aVal = aLoc if opcode[1] else program[aLoc]

  if op == OP_IN:
    if len(istream):
      i = int(istream.pop(0))
      if verbose: print("<= %d (from istream) t_%d" % (i, thread))
      program[aLoc] = i
    elif interactive: program[aLoc] = int(input("<= "))
    else: return Status(addr, ERR_INPUT)
    return Status(addr+2, ERR_NONE)

  if op == OP_OUT:
    ostream.append(aVal)
    if verbose: print("=> %d : %s t_%d" % (aVal, ostream, thread))
    return Status(addr+2, ERR_NONE)

  bLoc = program[addr+2]
  bVal = bLoc if opcode[2] else program[bLoc]

  if op == OP_JMP:
    # jump if true
    return Status(bVal if aVal else addr+3, ERR_NONE)

  if op == OP_NJMP:
    # jump if false
    return Status(bVal if not aVal else addr+3, ERR_NONE)

  rLoc = program[addr+3]
  
  if op == OP_ADD:
    program[rLoc] = aVal + bVal
    return Status(addr+4, ERR_NONE)
  
  if op == OP_MUL:
    program[rLoc] = aVal * bVal
    return Status(addr+4, ERR_NONE)

  if op == OP_LESS:
    # less than
    program[rLoc] = 1 if aVal < bVal else 0
    return Status(addr+4, ERR_NONE)

  if op == OP_EQL:
    # equal
    program[rLoc] = 1 if aVal == bVal else 0
    return Status(addr+4, ERR_NONE)
  
  return Status(addr, op)

class Thread:
  MAX_ID = 0
  def __init__(self, program):
    self.program = program
    self.addr = 0
    self.istream = []
    self.ostream = []
    self.status = Status(0, ERR_NONE)
    self.id = Thread.MAX_ID
    Thread.MAX_ID += 1

  def process(self):
    self.status = executeInstruction(self.program, self.status.addr, self.istream, self.ostream, verbose = False, thread = self.id)

def loadProgram(path, separator=','):
  program = []
  for n in open(path, 'r').readline().split(separator):
    program.append(int(n))
    
  return program

def calculateAmplification(sequence):
  output = 0
  for s in sequence:
    thread = Thread(loadProgram(PROGRAM_PATH))
    thread.istream = [s, output]
    while thread.status.err == ERR_NONE:
      thread.process()
    
    output = thread.ostream.pop()

  return output

def calculateAmplificationFeedback(sequence):
  # Create a thread for each amplifier
  threads = list()
  current_thread = 0
  for s in sequence:
    thread = Thread(loadProgram(PROGRAM_PATH))
    thread.istream.append(s)
    threads.append(thread)
    current_thread += 1

  current_thread = 0
  amp = [0]

  while len(threads):
    thread = threads[current_thread]
    # Append our current amp value to the input stream of this thread
    if len(amp):
      thread.istream.append(amp.pop())
    thread.process()
    if thread.status.err == ERR_NONE:
      # The thread is fine. Keep processing it.
      continue
    elif thread.status.err == ERR_SUCCESS:
      # This thread is finished.
      # Get its last output and remove the thread.
      amp.append(thread.ostream.pop())
      threads.pop(current_thread)
    elif thread.status.err == ERR_INPUT:
      # This thread is awaiting input.
      # Get its last output and move to the next thread.
      amp.append(thread.ostream.pop())
      current_thread += 1

    if current_thread >= len(threads): current_thread = 0

  # Once all threads are finished, return the last output.
  return amp.pop()

def basicAmplification():
  sequences = list(permutations(range(0,5)))
  amplifications = []

  for sequence in sequences:
    amplifications.append(calculateAmplification(sequence))

  print(max(amplifications))

def feedbackAmplification():
  feedbackSequences = list(permutations(range(5,10)))
  max_amp = 0
  max_sequence = []
  for sequence in feedbackSequences:
    value = calculateAmplificationFeedback(sequence)
    if value > max_amp:
      max_amp = value
      max_sequence = sequence

  print(max_amp)

basicAmplification()
feedbackAmplification()
