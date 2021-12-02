## adventofcode.com
# Day 17
# https://adventofcode.com/2020/day/17

import fr

answer1 = 'unknown'
answer2 = 'unknown'

inputs: list[str] = fr.readAsList('input17-test')

class P3:
  '''Describes the position of a Conway Cube.'''
  def __init__(self,x:int, y:int, z:int):
    self.x = x
    self.y = y
    self.z = z

  def __str__(self):
    return f'({self.x}, {self.y}, {self.z})'

  def __repr__(self):
    return self.__str__()

def addP3(a: P3, b: P3) -> P3:
  '''Adds two P3s together and returns a new P3.'''
  return P3(
    a.x + b.x,
    a.y + b.y,
    a.z + b.z
  )

def adjacentToP3(p: P3) -> list[P3]:
  '''Returns a list of all adjacent locations.'''
  adjs: list[P3] = []
  for x in [-1,0,1]:
    for y in [-1,0,1]:
      for z in [-1,0,1]:
        if x == 0 and y == 0 and z == 0: continue
        offset = P3(x,y,z)
        adjs.append(addP3(p, offset))

  return adjs


def makeCubeMap(inputs: list[str]) -> dict[P3, bool]:
  '''Builds a set of cubes from an input.'''
  height = len(inputs)
  width = len(inputs[0])
  print(f'Building a {width}x{height} cube map.')
  cubes: dict[P3, bool] = {}
  for rIndex in range(height):
    for cIndex in range(width):
      # For each active cube, add it and it's adjacent cubes
      # to the dictionary.
      nCube = P3(cIndex, rIndex, 0)

      # Safe to blindly overwrite this cube, since it is
      # being read from the source of truth (the input).
      cubes[nCube] = True if inputs[rIndex][cIndex] == '#' else False

      for adj in adjacentToP3(nCube):
        # If the adjacent cube isn't in the list, add it as inactive.
        if not adj in cubes: cubes[adj] = False

  return cubes

def activeFilter(p:tuple[P3,bool]) -> bool:
  return p[1]

def transitionState(initialState: dict[P3, bool]) -> dict[P3, bool]:
  """Performs one step of state transitions and returns the new cube state.  
  - If a cube is active and exactly 2 or 3 of its neighbors are also active,
    the cube remains active. Otherwise, the cube becomes inactive.
  - If a cube is inactive but exactly 3 of its neighbors are active, the cube
    becomes active. Otherwise, the cube remains inactive."""

  nextState = initialState.copy()
  for cube in initialState.keys():
    # Determine the active adjacent cubes for each cube.
    adj = adjacentToP3(cube)
    active = 0
    for a in adj:
      # Add inactive cube if not present.
      if not a in initialState:
        nextState[a] = False
        continue

      if initialState[a]: active += 1

    # We now know how many cubes are active adjacent to the current cube.
    # Apply the rules and update the next state.
    if initialState[cube]: nextState[cube] = (active == 2 or active == 3)
    else: nextState[cube] = active == 3

  final: dict[P3, bool] = {}
  for k in nextState:
    if nextState[k]: final[k] = True

  return final

def activeCount(cubes: dict[P3, bool]) -> int:
  active = 0
  for isActive in cubes.values():
    if isActive: active += 1

  return active

cubeState = makeCubeMap(inputs)
for step in range(7):
  print(f'Step {step}: {len(cubeState)} cubes.')
  cubeState = transitionState(cubeState)

answer1 = activeCount(cubeState)

print(f'Answer 1: {answer1}')
print(f'Answer 2: {answer2}')