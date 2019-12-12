# adventofcode.com
# Day 12
# https://adventofcode.com/2019/day/12

import common, re

from typing import List, Tuple


PROGRAM_PATH = common.getFilePath('input12.txt')


def compare(a: int, b: int) -> int:
  if a > b: return 1
  if a < b: return -1
  return 0

class Vector3:
  def __init__ (self, x: int = 0, y: int = 0, z: int = 0):
    self.x = x
    self.y = y
    self.z = z

  def add(self, v) -> None:
    self.x += v.x
    self.y += v.y
    self.z += v.z

  def compare(self, v):
    out = Vector3()
    out.x = -compare(self.x, v.x)
    out.y = -compare(self.y, v.y)
    out.z = -compare(self.z, v.z)
    return out

  def absSum(self) -> int: return abs(self.x) + abs(self.y) + abs(self.z)
    
  def __repr__ (self) -> str: return "Vector3"
  def __str__ (self) -> str: return "<x=%s, y=%s, z=%s>" % (str(self.x).rjust(5), str(self.y).rjust(4), str(self.z).rjust(4))

class Moon:
  def __init__(self, position: Vector3):
    self.p = position
    self.v = Vector3()
    self.initial = [(position.x, 0), (position.y, 0), (position.z, 0)]

  def xs(self) -> Tuple[int, int]:
    return (self.p.x, self.v.x)

  def ys(self) -> Tuple[int, int]:
    return (self.p.y, self.v.y)

  def zs(self) -> Tuple[int, int]:
    return (self.p.z, self.v.z)

  def __repr__(self) -> str: return "Moon %s" % self.p
  def __str__(self) -> str: return "pos=%s, vel=%s" % (self.p, self.v)

def readMoonsFrom(path: str) -> list:
  ms = []
  f = open(path, 'r')
  rm = f.readlines()
  for l in rm:
    # For as few inputs as given, this could just be manually entered.
    # RegEx is more fun, though. <3
    values = re.search(r'x=([-\d]+), y=([-\d]+), z=([-\d]+)', l)
    m = Moon(Vector3(int(values.group(1)),int(values.group(2)),int(values.group(3))))
    ms.append(m)
  return ms

def process(m:List[Moon]) -> None:
  for a in m:
    for b in m:
      if a == b: continue
      a.v.add(a.p.compare(b.p))
  
  for a in m: a.p.add(a.v)

# Recursive function to return gcd of a and b 
def gcd(a,b): 
    if a == 0: 
        return b 
    return gcd(b % a, a) 
  
# Function to return LCM of two numbers 
def lcm(a,b): 
    return (a*b) / gcd(a,b) 

def calculateSystemEnergy() -> int:
  moons = readMoonsFrom(PROGRAM_PATH)

  for step in range(0,1000):
    process(moons)

  systemEnergy = 0
  for m in moons:
    systemEnergy += m.v.absSum() * m.p.absSum()

  return systemEnergy

def calculateSystemPeriod() -> int:
  """Each dimension functions independently from the others.

  Find the period of each dimension, then determine the least
  common multiple of the periods to get the minimum period for all
  dimensions to return to their initial positions."""
  
  moons = readMoonsFrom(PROGRAM_PATH)
  universalSteps = 0
  px = 0
  py = 0
  pz = 0

  while not (px and py and pz):
    xr = yr = zr = True
    for m in moons:
      if m.initial[0] != m.xs() : xr = False
      if m.initial[1] != m.ys() : yr = False
      if m.initial[2] != m.zs() : zr = False

    if not px and xr: px = universalSteps
    if not py and yr: py = universalSteps
    if not pz and zr: pz = universalSteps

    process(moons)
    universalSteps += 1

  return int(lcm(px, lcm(py, pz)))

print(calculateSystemEnergy())
print(calculateSystemPeriod())
