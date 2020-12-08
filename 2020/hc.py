## adventofcode.com
# Handheld Console
# https://adventofcode.com/2020/day/8

import fr

from typing import List, Dict

class HCI:
  '''HanCon Instruction'''
  ins = 'nop'
  val = 0

  def __init__(self, instruction: str):
    split = instruction.split(' ')
    self.ins = split[0]
    self.val = int(split[1]) if len(split) > 1 else 0

  def __str__(self):
    return f'{self.ins}: {self.val}'

class HanCon:
  '''Handheld Console'''

  rom: List[HCI] = []
  op: int = 0
  acc: int = 0

  status: str = 'off'

  def loadROM(self, romPath: str):
    raw = fr.readAsList(romPath)
    self.rom = list(map(HCI, raw))
    self.op = 0
    self.acc = 0
    self.status = 'on'

  def __init__(self, romPath: str):
    self.loadROM(romPath)

  def tick(self) -> (int, int):
    '''
    Tick the current rom.
    Returns next op and current accumulator.
    '''

    # Handle reaching the end of the file.
    if self.op >= len(self.rom):
      self.status = 'end'
      return self.op, self.acc

    inst = self.rom[self.op]

    if inst.ins == 'acc':
      self.acc += inst.val
      self.op += 1
    elif inst.ins == 'jmp': self.op += inst.val
    elif inst.ins == 'nop': self.op += 1
    else:
      print(f'Invalid Instruction: {inst.ins}')
      self.status = 'error'

    return self.op, self.acc

  def reset(self):
    '''Reset the console without reloading the current rom.'''
    self.acc = 0
    self.op = 0

  def currentInstruction(self) -> HCI:
    return self.rom[self.op]

  def __len__(self):
    return len(self.rom)

