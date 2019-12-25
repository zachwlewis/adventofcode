# adventofcode.com
# Day 21
# https://adventofcode.com/2019/day/21

import common, math

import intcode as icp
from intpoint import IntPoint

from typing import Dict, Tuple, Set, List

PROGRAM_PATH = common.getFilePath('input21.txt')

def part1() -> None:
  ip = icp.Thread(icp.loadProgram(PROGRAM_PATH))
  ip.addInputAscii('NOT A T\nNOT B J\nOR T J\nNOT C T\nOR T J\nAND D J\nWALK\n')

  while not ip.didSucceed():
    ip.process()
    
  ip.readOutputAscii()
  print(ip.readOutput())

def part2() -> None:
  ip = icp.Thread(icp.loadProgram(PROGRAM_PATH))
  ip.addInputAscii('NOT A T\nNOT B J\nOR T J\nNOT C T\nOR T J\nAND D J\nNOT E T\nNOT T T\nOR H T\nAND T J\nRUN\n')

  while not ip.didSucceed():
    ip.process()
    
  ip.readOutputAscii()
  print(ip.readOutput())

part1()
part2()