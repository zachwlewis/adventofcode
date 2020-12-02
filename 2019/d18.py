# adventofcode.com
# Day 18
# https://adventofcode.com/2019/day/18

from common import getFilePath
from typing import Dict, Tuple, Set, List
from copy import deepcopy
from collections import deque, namedtuple

def part1():
  G = []
  for line in open(getFilePath('input18.txt'),'r').readlines():
    G.append(list(line.strip()))
  R = len(G)
  C = len(G[0])
  DR = [-1,0,1,0]
  DC = [0,1,0,-1]
  Q = deque()
  State = namedtuple('State', ['r', 'c', 'keys', 'd'])
  all_keys = set()
  for r in range(R):
    for c in range(C):
      if G[r][c]=='@':
        #print(r,c,G[r][c])
        Q.append(State(r, c, set(), 0))
      if 'a'<=G[r][c]<='z':
        all_keys.add(G[r][c])
  #print(len(all_keys), all_keys)

  SEEN = set()
  print('Calculating required steps',end='',flush=True)
  while Q:
    S = Q.popleft()
    key = (S.r, S.c, tuple(sorted(S.keys)))
    if key in SEEN:
      continue
    SEEN.add(key)
    if len(SEEN)%250000 == 0:
      print('.',end='',flush=True)
    if not (0<=S.r<R and 0<=S.c<C and G[S.r][S.c]!='#'):
      continue
    if 'A'<=G[S.r][S.c]<='Z' and G[S.r][S.c].lower() not in S.keys:
      continue
    newkeys = set(S.keys)
    if 'a'<=G[S.r][S.c]<='z':
      newkeys.add(G[S.r][S.c])
      if newkeys == all_keys:
        print('\n%d'%S.d)
        return
    for d in range(4):
      rr,cc = S.r+DR[d], S.c+DC[d]
      Q.append(State(rr, cc, newkeys, S.d+1))

def part2():
  G = []
  for line in open(getFilePath('input18_2.txt')).readlines():
    G.append(list(line.strip()))
  R = len(G)
  C = len(G[0])
  DR = [-1,0,1,0]
  DC = [0,1,0,-1]
  Q = deque()
  State = namedtuple('State', ['pos', 'keys', 'd'])
  all_doors = {}
  all_keys = {}
  starts = []
  for r in range(R):
    for c in range(C):
      if G[r][c]=='@':
        starts.append((r,c))
      if 'a'<=G[r][c]<='z':
        all_keys[G[r][c]] = (r,c)
      if 'A'<=G[r][c]<='Z':
        all_doors[G[r][c]] = (r,c)
  print(len(all_keys), all_keys)
  print(len(all_doors), all_doors)
  Q.append(State(starts, set(), 0))
  N = len(starts)

  best = 1e9
  SEEN = {}
  while Q:
    S = Q.popleft()
    key = (tuple(S.pos), tuple(sorted(S.keys)))
    if key in SEEN and S.d>=SEEN[key]:
      continue
    SEEN[key] = S.d
    if len(SEEN)%10000 == 0:
      print(key,S.d)
      print(len(SEEN))
    newkeys = set(S.keys)
    bad = False
    for i in range(N):
      r,c = S.pos[i]
      if not (0<=r<R and 0<=c<C and G[r][c]!='#'):
        bad = True
        break
      if 'A'<=G[r][c]<='Z' and G[r][c].lower() not in S.keys:
        bad = True
        print('B2')
        break
    if bad:
      continue

    D = {}
    Q2 = deque()
    for i in range(N):
      Q2.append((S.pos[i], i, 0))
    while Q2:
      pos,robot,dd = Q2.popleft()
      r,c = pos
      if not (0<=r<R and 0<=c<C and G[r][c]!='#'):
        continue
      if 'A'<=G[r][c]<='Z' and G[r][c].lower() not in S.keys:
        continue
      if pos in D:
        continue
      D[pos] = (dd,robot)
      for d3 in range(4):
        newpos = (r+DR[d3], c+DC[d3])
        Q2.append((newpos, robot,dd+1))

    for k in all_keys:
      if k not in S.keys and all_keys[k] in D:
        distance,robot = D[all_keys[k]]
        newpos = list(S.pos)
        newpos[robot] = all_keys[k]
        newkeys = set(S.keys)
        newkeys.add(k)
        newdist = S.d+distance
        if len(newkeys) == len(all_keys):
          if newdist < best:
            best = newdist
            print(best)
        Q.append(State(newpos, newkeys, newdist))

#part1()
#part2()

import sys
from copy import deepcopy
from collections import deque, namedtuple

import heapq
def main(path):
  with open(path) as infile:
    lines = infile.read().split('\n')
  
  grid = list(map(list, lines))
  
  doors = dict()
  keys = dict()
  start = None

  for y in range(len(grid)):
    for x in range(len(grid[y])):
      char = grid[y][x]
      if(char.isalpha()):
        if(char.isupper()):
          doors[char] = (x,y)
        else:
          keys[char] = (x,y)
      elif(char == '@'):
        start = (x,y)
  
  keyNames = sorted(keys.keys())
  keyIntDict = dict()
  
  for i in range(len(keyNames)):
    keyIntDict[keyNames[i]] = 1<<i;
  
  nodes = ['@', *doors.keys(), *keys.keys()]
  nodesLoc = dict()
  nodesLoc['@'] = start
  for key in keys:
    nodesLoc[key] = keys[key]
  for door in doors:
    nodesLoc[door] = doors[door]
  
  nodeDist = dict()
  for node in nodes:
    nodeDist[node] = dict()
  
  visited = [[False for x in range(len(grid[y]))] for y in range(len(grid))]
  toExplore = deque();
  
  dy = [-1, 0, 1, 0]
  dx = [0, 1, 0, -1]
  
  def inRange(x,y):
    return x>=0 and x<len(grid[0]) and y>= 0 and y<len(grid)

  for node in nodes:
    visited = [[False for x in range(len(grid[y]))] for y in range(len(grid))]
    
    startPos = nodesLoc[node]
    toExplore.append((startPos, 0))
    visited[startPos[1]][startPos[0]] = True
    while(len(toExplore) != 0):
      curPos, curDis = toExplore.popleft()
      curX, curY = curPos
      gridChar = grid[curY][curX]
      if(gridChar in nodes and gridChar != node):
        nodeDist[node][gridChar] = curDis
      else:
        for i in range(4):
          newX = curX + dx[i]
          newY = curY + dy[i]
          if(inRange(newX, newY)):
            if(grid[newY][newX]!='#'):
              if(not visited[newY][newX]):
                visited[newY][newX] = True
                toExplore.append(((newX, newY), curDis+1))

  bfDist = dict()
  for node in nodes:
    bfDist[node] = dict()
   
  pq = [(0, 0, '@')]
  heapq.heapify(pq)
  bfDist['@'][0] = 0
  
  def isSmaller(newDist, node, intKeyMap):
    if(intKeyMap not in bfDist[node]):
      return True
    else:
      return newDist < bfDist[node][intKeyMap] 
  fullKeys = (1<<len(keys))-1
  
  while(len(pq)!=0):
    curDist, curKeyMap, curNode = heapq.heappop(pq)
    if(curKeyMap == fullKeys):   
      print(curDist)
      break
    else:       
      for nextNode in nodeDist[curNode]:
        newDist = curDist + nodeDist[curNode][nextNode]
        nextKeyMap = curKeyMap
        if(nextNode.isupper()):
          if(keyIntDict[nextNode.lower()] & nextKeyMap == 0):
            #No key
            continue
        elif(nextNode.islower()):
          #Add key
          nextKeyMap |= keyIntDict[nextNode]
        if(isSmaller(newDist, nextNode, nextKeyMap)):
            bfDist[nextNode][nextKeyMap] = newDist
            heapq.heappush(pq, (newDist, nextKeyMap, nextNode))
        
  

  #----------------------------------PART 2-----------------------------------------#
  
  
  grid2 = [ grid[y][:] for y in range(len(grid))]
  grid2[start[1]][start[0]] = '#'
  for i in range(4):
    grid2[start[1]+dy[i]][start[0]+dx[i]] = '#'
    
  grid2[start[1]-1][start[0]-1] = '@'
  grid2[start[1]-1][start[0]+1] = '$'
  grid2[start[1]+1][start[0]+1] = '%'
  grid2[start[1]+1][start[0]-1] = '&'
  
  newNodes = ['@', '$', '%', '&', *doors.keys(), *keys.keys()]
  
  nodesLoc = dict()
  nodesLoc['@'] = (start[0]-1, start[1]-1)
  nodesLoc['$'] = (start[0]+1, start[1]-1)
  nodesLoc['%'] = (start[0]+1, start[1]+1)
  nodesLoc['&'] = (start[0]-1, start[1]+1)
  
  for key in keys:
    nodesLoc[key] = keys[key]
  for door in doors:
    nodesLoc[door] = doors[door]
  
  
  newNodeDist = dict()
  for node in newNodes:
    newNodeDist[node] = dict()
  
  visited = [[False for x in range(len(grid2[y]))] for y in range(len(grid2))]
  toExplore = deque();
  
  for node in newNodes:
    visited = [[False for x in range(len(grid2[y]))] for y in range(len(grid2))]
    startPos = nodesLoc[node]
    toExplore.append((startPos, 0))
    visited[startPos[1]][startPos[0]] = True
    while(len(toExplore) != 0):
      curPos, curDis = toExplore.popleft()
      curX, curY = curPos
      gridChar = grid2[curY][curX]
      if(gridChar in newNodes and gridChar != node):
        newNodeDist[node][gridChar] = curDis
      else:
        for i in range(4):
          newX = curX + dx[i]
          newY = curY + dy[i]
          if(inRange(newX, newY)):
            if(grid2[newY][newX]!='#'):
              if(not visited[newY][newX]):
                visited[newY][newX] = True
                toExplore.append(((newX, newY), curDis+1))
         
  startNodes = "@$%&"    
  
  reachableKeys = dict()
  reachableVisited = set()
  for i in range(len(startNodes)):
    startNode = startNodes[i]
    reachableVisited.add(startNode)
    reachableKeys[startNode] = 0
    toExplore = deque([startNode])
    while(len(toExplore) != 0):
      curNode = toExplore.popleft()
      for nxtNode in newNodeDist[curNode]:
        if(nxtNode not in reachableVisited):
          reachableVisited.add(nxtNode)
          if(nxtNode.islower()):
            reachableKeys[startNode]|=keyIntDict[nxtNode]
          toExplore.append(nxtNode)
    
  
  bfDist = dict()
  pq = [(0, 0, startNodes)]
  heapq.heapify(pq)
  bfDist[startNodes] = dict()
  bfDist[startNodes][0] = 0

  def newIsSmaller(newDist, newNodes, intKeyMap):
    if(newNodes not in bfDist):
      bfDist[newNodes] = dict()
      return True
    elif(intKeyMap not in bfDist[newNodes]):
      return True
    else:
      return newDist < bfDist[newNodes][intKeyMap] 
  
  while(len(pq)!=0):
    curDist, curKeyMap, curNodes = heapq.heappop(pq)
    if(curKeyMap == fullKeys):   
      print(curDist)
      break
    else:
      for bot in range(4):
        if(reachableKeys[startNodes[bot]]&curKeyMap == reachableKeys[startNodes[bot]]):
          continue
        curNode = curNodes[bot]
        for newNode in newNodeDist[curNode]:
          newDist = curDist + newNodeDist[curNode][newNode]
          newNodesList = list(curNodes)
          newNodesList[bot] = newNode
          newNodes = "".join(newNodesList)
          newKeyMap = curKeyMap
          if(newNode.isupper()):
            if(keyIntDict[newNode.lower()]&curKeyMap == 0):
              continue
          elif(newNode.islower()):
            newKeyMap |= keyIntDict[newNode]
          if(newIsSmaller(newDist, newNodes, newKeyMap)):
            bfDist[newNodes][newKeyMap] = newDist
            heapq.heappush(pq, (newDist, newKeyMap, newNodes))
          
main(getFilePath('input18.txt'))
  