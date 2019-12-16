# adventofcode.com
# Day 15
# https://adventofcode.com/2019/day/15

import common, math

import intcode as icp
from intpoint import IntPoint

from typing import Dict, Tuple
DroneMap = Dict[int, Dict[int, int]]

PROGRAM_PATH = common.getFilePath('input15.txt')
f = open(PROGRAM_PATH, 'r')

# Droid Status Codes
DS_WALL = 0 # Droid hit wall. Did not move.
DS_MOVE = 1 # Droid moved successfully.
DS_ONO2 = 2 # Droid moved successfully and is on the O2 System.

DS_P = {-1:'start', DS_WALL: 'wall', DS_MOVE: 'move', DS_ONO2: 'success'}
MAP_P = {DS_WALL: "█", DS_MOVE:".", DS_ONO2:"O"}

# Droid Movement Codes
DM_N = 1 # Move North
DM_S = 2 # Move South
DM_W = 3 # Move West
DM_E = 4 # Move East

DM_P = {DM_N: 'north', DM_E: 'east', DM_S: 'south', DM_W: 'west'}

S_D = {'n': DM_N, 'e': DM_E, 's':DM_S, 'w':DM_W}

# Movement Cycle
MC = {DM_N: DM_E,
      DM_E: DM_S,
      DM_S: DM_W,
      DM_W: DM_N}

# Movement Deltas
MD = {DM_N: IntPoint(0,1),
      DM_E: IntPoint(1, 0),
      DM_S: IntPoint(0,-1),
      DM_W: IntPoint(-1,0)}

class Scanner:
  def __init__(self,
               program: icp.Thread,
               direction: int,
               steps: int,
               position: IntPoint):
    self.program = program
    self.direction = direction
    self.steps = steps
    self.position = position

droneMap: DroneMap = {0:{0:1}} # Saved as y, x.

def addPosition(m: DroneMap, p: IntPoint, value: int) -> bool:
  """Adds a position to the map.

  Returns if new entry.
  """
  x = p.x
  y = p.y
  if m.get(y, None) == None:
    # No dictionary exists for this y position.
    # Create one and add our value.
    m[y] = {x:value}
    return True
  
  if m[y].get(x, None) == None:
    m[y][x] = value
    return True

  return False

def getMapExtents(m: DroneMap) -> Tuple[int, int, int, int]:
  y_min = 0
  y_max = 0
  x_min = 0
  x_max = 0
  for y in m:
    y_min = min(y, y_min)
    y_max = max(y, y_max)
    for x in m[y]:
      x_min = min(x, x_min)
      x_max = max(x, x_max)

  return x_min-1, y_min-1, x_max+2, y_max+2

def printMap(m: DroneMap, p: IntPoint = None, file: str = "") -> None:
  """Prints a map to an optional file."""
  x_min, y_min, x_max, y_max = getMapExtents(m)
  ys = range(y_max, y_min, -1)
  for y in ys:
    if m.get(y, None) == None:
      print("")
      continue
    for x in range(x_min,x_max):
      if m[y].get(x, None) == None:
        print("░", end="")
        continue
      if p != None and IntPoint(x, y) == p:
        print("D", end="")
        continue
      print(MAP_P[m[y][x]], end="")
    print("")

def hasBeenVisited(m: DroneMap, p: IntPoint) -> bool:
  if m.get(p.y, None) == None: return False
  if m[p.y].get(p.x, None) == None: return False
  return True

def findO2System() -> Scanner:
  init = icp.Thread(icp.loadProgram(PROGRAM_PATH))
  drones = [Scanner(init.clone(), DM_N, 0, IntPoint(0,0)),
            Scanner(init.clone(), DM_E, 0, IntPoint(0,0)),
            Scanner(init.clone(), DM_S, 0, IntPoint(0,0)),
            Scanner(init.clone(), DM_W, 0, IntPoint(0,0))]
  status = -1
  drone = drones.pop(0)
  while not status == DS_ONO2:
    drone.program.process()
    if drone.program.needInput():
      # Drone waiting for input.
      #print("----------s%d %s" % (drone.program.id, drone.position))
      #printMap(droneMap, drone.position)
      direction = drone.direction
      """Bulletproof Input
      print(drone.position, DS_P[status], end=" ")
      newDirection = -1
      while newDirection == -1:
        try:
          newDirection = S_D[input("<=")]
        except:
          newDirection = -1
      
      direction = newDirection
      #"""
      drone.program.istream.append(direction)
      continue
    if drone.program.hasOutput():
      status = drone.program.readOutput()
      if status == DS_MOVE or status == DS_ONO2:
        drone.steps += 1
        drone.position += MD[direction]
        addPosition(droneMap, drone.position, status)

        for d in MC:
          if d == drone.direction: continue
          if not hasBeenVisited(droneMap, drone.position + MD[d]):
            #print("Making scanner facing %s" % DM_P[d])
            drones.append(Scanner(drone.program.clone(), d, drone.steps, drone.position))

      elif status == DS_WALL:
        wallPosition = drone.position + MD[direction]
        addPosition(droneMap, wallPosition, status)
        if len(drones): drone = drones.pop(0)
        else:
          #print("-------")
          #printMap(droneMap,drone.position)
          return drone
      continue

  return drone

def calculateO2Fill(d: Scanner):
  drones = [Scanner(d.program.clone(), DM_N, 0, d.position),
            Scanner(d.program.clone(), DM_E, 0, d.position),
            Scanner(d.program.clone(), DM_S, 0, d.position),
            Scanner(d.program.clone(), DM_W, 0, d.position)]
  status = -1
  steps = 0
  drone = drones.pop(0)
  while drone != None:
    steps = max(steps, drone.steps)
    drone.program.process()
    if drone.program.needInput():
      # Drone waiting for input.
      #print("----------s%d %s" % (drone.program.id, drone.position))
      #printMap(droneMap, drone.position)
      direction = drone.direction
      """Bulletproof Input
      print(drone.position, DS_P[status], end=" ")
      newDirection = -1
      while newDirection == -1:
        try:
          newDirection = S_D[input("<=")]
        except:
          newDirection = -1
      
      direction = newDirection
      #"""
      drone.program.istream.append(direction)
      continue
    if drone.program.hasOutput():
      status = drone.program.readOutput()
      if status == DS_MOVE or status == DS_ONO2:
        drone.steps += 1
        drone.position += MD[direction]
        addPosition(droneMap, drone.position, status)

        for d in MC:
          if d == drone.direction: continue
          if not hasBeenVisited(droneMap, drone.position + MD[d]):
            #print("Making scanner facing %s" % DM_P[d])
            drones.append(Scanner(drone.program.clone(), d, drone.steps, drone.position))

      elif status == DS_WALL:
        wallPosition = drone.position + MD[direction]
        addPosition(droneMap, wallPosition, status)
        if len(drones): drone = drones.pop(0)
        else:
          drone = None
      continue

  return steps

d = findO2System()
printMap(droneMap)
droneMap = {d.position.y:{d.position.y:2}}
d2 = calculateO2Fill(d)
printMap(droneMap)
print(d.steps)
print(d2)