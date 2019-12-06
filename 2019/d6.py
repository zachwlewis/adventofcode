# adventofcode.com
# Day 6
# https://adventofcode.com/2019/day/6

import common

f = open(common.getFilePath('input6.txt'), 'r')
orbit_data = f.read().splitlines()

orbits = dict()
planets = set()
for orbit in orbit_data:
  link = orbit.split(')')
  planets.add(link[1])
  orbits.setdefault(link[1],link[0])

obc = 0
for planet in planets:
  p = planet
  while p != "COM":
    obc += 1
    p = orbits.get(p,"")


def getPathToCOM(planet, orbit_map):
  path = dict()
  p = orbit_map.get(planet, "")
  step = 0
  while p != "COM":
    step += 1
    p = orbit_map.get(p, "")
    path.setdefault(p, step)
  
  return path

def getRequiredTransfers(start, end, orbit_map):
  start = getPathToCOM(start, orbit_map)
  end = getPathToCOM(end, orbit_map)

  for jump in start:
    if end.get(jump,-1) != -1: return end.get(jump, -1) + start.get(jump,-1)


print(obc)
print(getRequiredTransfers("YOU", "SAN", orbits))
