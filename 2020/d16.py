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

# -------- Part 2 --------
# Use validTickets to find target field.

field_ranges: dict[str, set[int]] = {}
valid_fields: dict[str, set[int]] = {}

for field in fields_input:
  # Build field lookups.
  field_name = field.split(',')[0]
  field_ranges[field_name] = fieldSet(field)
  valid_fields[field_name] = set(range(20))

for ticket_index in validTickets:
  ticketValues = list(map(int, nearby_input[ticket_index].split(',')))
  
  for field_key in valid_fields.keys():
    valids: set[int] = set()
    for field_index in valid_fields[field_key]:
      if ticketValues[field_index] in field_ranges[field_key]: valids.add(field_index)

    valid_fields[field_key] = valids.intersection(valid_fields[field_key])

# valid_fields now should contain all field indices.
# Do some manual work to filter down to single ids.
for kvp in valid_fields.items():
  print(f'{kvp[0]}: {kvp[1]}')

# departure location: {1}
# departure station: {19}
# departure platform: {2}
# departure track: {4}
# departure date: {14}
# departure time: {6}
# arrival location: {15}
# arrival station: {3}
# arrival platform: {10}
# arrival track: {13}
# class: {5}
# duration: {18}
# price: {16}
# route: {17}
# row: {8}
# seat: {11}
# train: {7}
# type: {0}
# wagon: {12}
# zone: {9}

my_ticket = [109,101,79,127,71,59,67,61,173,157,163,103,83,97,73,167,53,107,89,131]
answer2 = (
  my_ticket[1] *
  my_ticket[19] *
  my_ticket[2] *
  my_ticket[4] *
  my_ticket[14] *
  my_ticket[6]
)

print(f'Answer 1: {answer1}')
print(f'Answer 2: {answer2}')
