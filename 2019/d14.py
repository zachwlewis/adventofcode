# adventofcode.com
# Day 14
# https://adventofcode.com/2019/day/14

import common, math

from typing import List, Tuple, Dict
Compound = Tuple[str,int]
ReactionTable = Dict[Compound, List[Compound]]

PROGRAM_PATH = common.getFilePath('input14.txt')

def parseLines(lines: List[str]) -> ReactionTable:
    def _parseCompound(numsymbol: str) -> Compound:
        num, symbol = numsymbol.strip().split()
        return symbol, int(num)
    reactions = {}
    for line in lines:
        left, right = line.split('=>')
        left, right = list(map(_parseCompound, left.split(','))), _parseCompound(right)
        reactions[right[0]] = (right[1], left)
    return reactions

def process(reactions: ReactionTable, resources: List[Compound], element: str, consume: str, qty: int) -> bool:
    if resources[element] >= qty:
        return True
    if element == consume:
        return False
    n = math.ceil((qty - resources[element]) / reactions[element][0])
    ensured = True
    for _element, _qty in reactions[element][1]:
        ensured = ensured and process(reactions, resources, _element, consume, n*_qty)
        resources[_element] -= n*_qty
    if ensured:
        resources[element] += n*reactions[element][0]
    return ensured

def calculateOreForFuel(reactions: ReactionTable, fuel: int) -> int:
    low, high = 0, 10**12
    while low < high:
        mid = low + (high - low) // 2
        resources = {element: 0 for element in reactions}
        resources['ORE'] = mid
        if process(reactions, resources, 'FUEL', 'ORE', fuel):
            high = mid
        else:
            low = mid + 1
    return low

def calculateFuelFromOre(reactions: ReactionTable, ore: int) -> int:
    low, high = 0, 10**12
    while low < high-1:
        mid = low + (high - low) // 2
        data = {element: 0 for element in reactions}
        data['ORE'] = ore
        if process(reactions, data, 'FUEL', 'ORE', mid):
            low = mid
        else:
            high = mid - 1
    return high if process(reactions, data, 'FUEL', 'ORE', high) else low

reactions = parseLines(open(PROGRAM_PATH).read().split('\n'))

print(calculateOreForFuel(reactions, 1))
print(calculateFuelFromOre(reactions, 10**12))