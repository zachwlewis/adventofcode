# adventofcode.com
# Day 10
# https://adventofcode.com/2019/day/10

import common, math

from typing import List, Tuple
Point = Tuple[int, int]
PointList = List[Point]

class Asteroid:
  def __init__(self, location: Point, distance: float):
    self.location = location
    self.distance = distance

  def __repr__(self):
    return "Asteroid()"
  def __str__(self):
    return "%s -> %0.3f" % (self.location, self.distance)

PROGRAM_PATH = common.getFilePath('input10.txt')

def parseMap(path: str) -> PointList:

  f = open(PROGRAM_PATH, 'r')
  rows = f.readlines()
  points = []
  for y in range(len(rows)):
    for x in range(len(rows[y])):
      if rows[y][x] == '#': points.append((x,y))
  
  return points

def checkDistances(p0: Point, map: PointList) -> dict:
  dists = dict()
  for p in map:
    if p != p0:
      dx = p[0] - p0[0]
      dy = p[1] - p0[1]
      r = math.sqrt(dx**2 + dy**2)
      theta = math.atan2(dy, dx)
      if r < dists.get(theta, 1000000):
        dists[theta] = r
      
  return dists

def getAsteroidList(p0: Point, map: PointList) -> dict:
  asteroids = dict()
  for p in map:
    if p == p0: continue
    dx = p[0] - p0[0]
    dy = p[1] - p0[1]
    r = math.sqrt(dx**2 + dy**2)
    theta = calculateAngle(dx, dy)
    if asteroids.get(theta) == None: asteroids[theta] = [Asteroid(p, r)]
    else: asteroids[theta].append(Asteroid(p, r))

  return asteroids

# The laser starts by pointing up and always rotates clockwise, vaporizing any asteroid it hits.
def calculateAngle(x:float, y:float) -> float:
  angle = math.degrees(math.atan2(y, x)) + 90
  if angle < 0 : angle += 360
  return angle

def sortDistance(elem: Asteroid):
  return elem.distance

asteroidMap = parseMap(PROGRAM_PATH)

maxVisible = 0
location = (-1, -1)
for p in asteroidMap:
  numVisible = len(checkDistances(p, asteroidMap))
  if numVisible > maxVisible:
    maxVisible = numVisible
    location = p
  
print(location, maxVisible)

hitlist = getAsteroidList(location,asteroidMap)

# Sort hitlist based on distance
for r in hitlist:
  hitlist[r].sort(key=sortDistance)

hh = []
for d in hitlist:
  hh.append((d, hitlist[d]))

hh.sort()

shot = 1
shotAsteroid = True
#print(hitlist.keys())
while(shotAsteroid):
  shotAsteroid = False
  for r in hh:
    if len(r[1]) == 0: continue
    shotAsteroid = True
    if shot in {1,2,3,10,20,50,100,199,200,201,299}:
      print(shot, r[1][0].location, r[1][0].location[0]*100 + r[1][0].location[1])
    r[1].pop(0)
    shot += 1