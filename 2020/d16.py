## adventofcode.com
# Day 16
# https://adventofcode.com/2020/day/16

import fr

answer1 = 'unknown'
answer2 = 'unknown'

# inputs: list[str] = fr.readAsList('input16')

fields_input = fr.readAsList('input16-fields')
nearby_input = fr.readAsList('input16-nearby-tickets')

valid_set: set[int] = set()

def fieldSet(field: str) -> set[int]:
  '''Takes a field definition and returns a set containing
  the valid values of the field.'''

  # Saved as a comma separated list
  # Name is unneeded, so just grab the ranges
  raw_ranges = field.split(',')[1:]
  values: set[int] = set()

  for field_range in raw_ranges:
    range_values = field_range.split('-')
    range_set = set(range(int(range_values[0]), int(range_values[1]) + 1))
    values = values.union(range_set)

  return values

validValues: set[int] = set()
for field in fields_input:
  validValues = validValues.union(fieldSet(field))

validTickets: set[int] = set() # valid ticket indices

answer1 = 0
for ticket_index in range(len(nearby_input)):
  ticketValues = list(map(int, nearby_input[ticket_index].split(',')))
  valid = True
  for value in ticketValues:
    if not value in validValues:
      answer1 += value
      valid = False

  if valid: validTickets.add(ticket_index)

# Use validTickets to find target field.

print(f'Answer 1: {answer1}')
print(f'Answer 2: {answer2}')
