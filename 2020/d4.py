## adventofcode.com
# Day 4
# https://adventofcode.com/2020/day/4

import fr
import re

from typing import List

passports = fr.readAsList('input4-clean')

requiredFields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}

def validatePassportFields(passport: str) -> (bool, dict):
  data = passport.split(',')
  # build set of keys
  keys = set()
  passportDict = {}
  for key in range(0, len(data), 2):
    keys.add(data[key])
    passportDict[data[key]] = data[key+1].strip()

  fields = requiredFields.intersection(passportDict.keys())

  return len(fields) == len(requiredFields), passportDict

def validatePassportData(passport: dict) -> bool:
  return ( validateBirthYear(passport['byr'])
       and validateIssueYear(passport['iyr'])
       and validateExpirationYear(passport['eyr'])
       and validateHeight(passport['hgt'])
       and validateHairColor(passport['hcl'])
       and validateEyeColor(passport['ecl'])
       and validatePassportID(passport['pid'])
       and validateCountryID(passport.get('cid', ''))
  )

def validateBirthYear(byr: str) -> bool:
  '''byr (Birth Year) - four digits; at least 1920 and at most 2002.'''
  if len(byr) != 4: return False
  if int(byr) < 1920: return False
  if int(byr) > 2002: return False

  return True

def validateIssueYear(iyr: str) -> bool:
  '''iyr (Issue Year) - four digits; at least 2010 and at most 2020.'''
  if len(iyr) != 4:
    print(f'Issue Year: Invalid length. ({iyr})')
    return False
  if int(iyr) < 2010 or int(iyr) > 2020: 
    print(f'Issue Year: Invalid value. ({iyr})')
    return False

  return True

def validateExpirationYear(eyr: str) -> bool:
  '''eyr (Expiration Year) - four digits; at least 2020 and at most 2030.'''
  if len(eyr) != 4:
    print(f'Expiration Year: Invalid length. ({eyr})')
    return False
  if int(eyr) < 2020 or int(eyr) > 2030:
    print(f'Expiration Year: Invalid value. ({eyr})')
    return False

  return True

def validateHeight(hgt: str) -> bool:
  '''hgt (Height) - a number followed by either cm or in:
     - If cm, the number must be at least 150 and at most 193.
     - If in, the number must be at least 59 and at most 76.'''
  m = re.match('\A(\d{2,3})(in|cm)\Z', hgt)
  if m == None:
    print(f'Height: Invalid format. ({hgt})')
    return False

  value = int(m.group(1))
  unit = m.group(2)
  if unit == 'cm':
    if value < 150 or value > 193:
      print(f'Height: Invalid value. ({hgt})')
      return False
  if unit == 'in':
    if value < 59 or value > 76:
      print(f'Height: Invalid value. ({hgt})')
      return False

  return True

def validateHairColor(hcl: str) -> bool:
  '''hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.'''
  if re.match('\A#[0-9a-f]{6}\Z', hcl) == None:
      print(f'Hair Color: Invalid format. ({hcl})')
      return False

  return True


def validateEyeColor(ecl: str) -> bool:
  '''ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.'''
  if not ecl in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}:
    print(f'Eye Color: Invalid value. ({ecl})')
    return False

  return True


def validatePassportID(pid: str) -> bool:
  '''pid (Passport ID) - a nine-digit number, including leading zeroes.'''
  if re.match('\A\d{9}\Z', pid) == None:
    print(f'Passport ID: Invalid format. ({pid})')
    return False

  return True


def validateCountryID(cid: str) -> bool:
  '''cid (Country ID) - ignored, missing or not.'''
  return True

validPassports = 0
correctPassports = 0

for passport in passports:
  isValid, data = validatePassportFields(passport)
  if isValid:
    validPassports += 1
    if validatePassportData(data): correctPassports += 1


print(f'Answer 1:   {validPassports}')
print(f'Answer 2: {correctPassports}')