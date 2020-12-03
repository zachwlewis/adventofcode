## adventofcode.com
# Day 3
# https://adventofcode.com/2020/day/3

import fr

from typing import List

route = fr.readAsList('input3')

def countTrees(route: List[str], width: int, right: int, down: int) -> int:
  position = 0
  trees = 0
  for row in range(0, len(route), down):
    if route[row][position] == "#": trees += 1
    position = (position + right) % width

  return trees

routeA = countTrees(route, 31, 3, 1)
print(f'Trees along slope (1,3): {routeA}')

routeB = countTrees(route, 31, 1, 1)
routeC = countTrees(route, 31, 5, 1)
routeD = countTrees(route, 31, 7, 1)
routeE = countTrees(route, 31, 1, 2)

treeProduct = routeA * routeB * routeC * routeD * routeE
print(f'Trees product along all routes: {treeProduct}')
