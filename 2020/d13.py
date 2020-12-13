## adventofcode.com
# Day 13
# https://adventofcode.com/2020/day/13

import fr
import math
from typing import List, Dict, Tuple

answer1 = 'unknown'
answer2 = 'unknown'

inputs = fr.readAsList('input13')

timestamp = int(inputs[0])
busses = inputs[1].split(',')
minDeparture = math.inf
minBus = math.inf
maxBus = 0

for bus in busses:
  if bus != 'x':
    busID = int(bus)
    busDeparture = math.ceil(timestamp / busID) * busID
    if busDeparture < minDeparture:
      minDeparture = busDeparture
      minBus = busID

    maxBus = max(maxBus, busID)

answer1 = minBus * (minDeparture - timestamp)

# PART 2 ----------------------

bus_list = inputs[1].strip().split(',')
buses = []
for n in range(len(bus_list)):
	if bus_list[n] != 'x':
		buses.append((int(bus_list[n]), n))

def do_it3a(base_magnitude, next_bus, next_bus_offset):
	base = base_magnitude[0]
	magnitude = base_magnitude[1]
	done = False
	while not done:
		modulo = (base + next_bus_offset) % next_bus
		if modulo == 0:
			done = True
			magnitude *= next_bus
		else:
			base += magnitude
	return (base, magnitude)

base_magnitude = (buses[0][0], buses[0][0])
for n in range(1, len(buses)):
	base_magnitude = do_it3a(base_magnitude, buses[n][0], buses[n][1])

answer2 = base_magnitude[0]

print(f'Answer 1: {answer1}')
print(f'Answer 2: {answer2}')