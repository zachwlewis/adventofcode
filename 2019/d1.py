# adventofcode.com
# Day 1
# https://adventofcode.com/2019/day/1

import common, math

# Fuel required to launch a given module is based on its mass.
# Specifically, to find the fuel required for a module, take its mass,
# divide by three, round down, and subtract 2.

def calculateBasicFuel(mass):
  return math.floor(float(mass) / 3) - 2

def calculateTotalFuel(mass):
  fuel = math.floor(float(mass) / 3) - 2
  if fuel <= 0: return 0
  
  return fuel + calculateTotalFuel(fuel)

modules = open(common.getFilePath('input1.txt'), 'r').readlines()

basicFuel = 0
totalFuel = 0

for mass in modules:
  basicFuel += calculateBasicFuel(int(mass))
  totalFuel += calculateTotalFuel(int(mass))

print("Basic Fuel: %d" % basicFuel)
print("Total Fuel: %d" % totalFuel)