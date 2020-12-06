## adventofcode.com
# Day 2
# https://adventofcode.com/2020/day/2

import fr

from typing import List

passwords = fr.readAsList('input2-clean')

def checkPasswordA(password: str):
  args = password.split(',')
  min = int(args[0])
  max = int(args[1])
  match = args[2]
  pw: str = args[3]

  num = pw.count(match)
  return num <= max and num >= min

def checkPasswordB(password: str):
  args = password.split(',')
  indexA = int(args[0]) - 1
  indexB = int(args[1]) - 1
  match: str = args[2]
  pw: str = args[3]

  validA = 1 if pw[indexA] == match else 0
  validB = 1 if pw[indexB] == match else 0
  return (validA + validB) == 1

validPasswordsA = 0
validPasswordsB = 0
for p in passwords:
  validPasswordsA += 1 if checkPasswordA(p) else 0
  validPasswordsB += 1 if checkPasswordB(p) else 0

print(f'Answer 1: {validPasswordsA}')
print(f'Answer 2: {validPasswordsB}')