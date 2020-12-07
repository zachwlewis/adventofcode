## adventofcode.com
# Day 7
# https://adventofcode.com/2020/day/7

import fr

from typing import List, Dict

inputs = fr.readAsList('input7-clean')

def parseRules(rules: List[str]) -> Dict[str,Dict[str,int]]:
  _rules = {}
  for line in rules:
    rList = line.split(',')

    # If there is only one item,
    # add an empty dictionary.
    if len(rList) == 1:
      _rules[rList[0]] = {}
      continue

    k = rList[0]
    vList = rList[1:]
    v = {}
    for i in range(0,len(vList), 2):
      v[vList[i+1]] = int(vList[i])
    
    _rules[k] = v

  return _rules

rules = parseRules(inputs)

def canContain(outerBag: str, innerBag: str) -> bool:
  if not outerBag in rules:
    # The outer bag can't contain anything,
    # so it can't contain the inner bag.
    return False

  contents = rules[outerBag]
  for bag in contents.keys():
    if bag == innerBag: return True
    if canContain(bag, innerBag): return True

  return False


answer1 = 0
for bag in rules.keys():
  if canContain(bag, 'shiny gold'): answer1 += 1

# Dynamic Programming 

dp = {}

def debug(iteration):
  print(f'--- ITERATION {iteration} ------')
  for item in dp.keys():
    print(f'{item} -> {dp[item]}')

iCount = 0
while len(dp) != len(rules):
#for i in range(0,2):
  iCount += 1
  for bag in rules.keys():
    if bag in dp:
      # This bag has already been calculated!
      continue

    if len(rules[bag]) == 0:
      # This bag can contain no others.
      # Count as just the one bag.
      dp[bag] = 0
      continue

    totalCount = 0
    allFound = True
    for _bag in rules[bag].keys():
      if not _bag in dp: allFound = False
      else:
        totalCount += rules[bag][_bag] * (dp[_bag] + 1)

    # Save the total bags that can be contained
    if allFound: dp[bag] = totalCount

answer2 = dp['shiny gold']

print(f'Answer 1: {answer1}')
print(f'Answer 2: {answer2}')