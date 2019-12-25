# adventofcode.com
# Day 23
# https://adventofcode.com/2019/day/23

from common import getFilePath
import intcode as icp
from typing import Dict, Tuple, Set, List

PROGRAM_PATH = getFilePath('input23.txt')

class Network:
  def __init__(self, program: str, size: int):
    self.computers: List[icp.Thread] = []
    self.program: str = program
    self.size: int = size
    self.NAT: Tuple[int, int] = None
    self.idleCycles = 0

  def boot(self) -> None:
    for i in range(self.size):
      _thread = icp.Thread(icp.loadProgram(self.program))
      # Set IP
      _thread.addInput(i)
      _thread.id = i
      self.computers.append(_thread)
      
      #print('Booting %d...' % _thread.id)

  def tick(self) -> bool:
    processing = False
    noPackets = True
    sentPacket = False
    for c in self.computers:
      if c.didSucceed(): continue
      processing = True
      c.process()
      if c.needInput():
        c.addInput(-1)
        c.process()
      
      if len(c.ostream) >= 3:
        # Send a packet if a full one exists.
        sentPacket = True
        self.send(c.readOutput(), c.readOutput(), c.readOutput())

    self.idleCycles += 1
    if self.idleCycles > 1100 and self.NAT:
      self.send(0, self.NAT[0], self.NAT[1])
      print('Sending', self.NAT)
    return processing

  def send(self, ip: int, x: int, y: int) -> None:
    self.idleCycles = 0
    if ip == 255:
      #print('NAT <= (%d, %d)' % (x, y))
      self.NAT = (x, y)
    else:
      #print('%d <= (%d, %d)' % (ip, x, y))
      self.computers[ip].addInput(x)
      self.computers[ip].addInput(y)

n = Network(PROGRAM_PATH, 50)
n.boot()
while n.tick():
  continue
