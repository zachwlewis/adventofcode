"""
adventofcode.com
Day 7
https://adventofcode.com/2021/day/7
"""

import fr

inputs: list[str] = fr.read_as_list('input7')
initial_positions: list[int] = list(map(int, inputs[0].split(',')))

def get_required_fuel_basic(target: int, positions: list[int]) -> int:
    """
    Finds the required fuel to move all positions to the target using the basic
    procedure.
    """
    fuel: int = 0
    for position in positions:
        fuel += abs(target - position)
    return fuel

total_fuel = get_required_fuel_basic(0, initial_positions)
for t in range(1,max(initial_positions)):
    fuel_cost = get_required_fuel_basic(t, initial_positions)
    if fuel_cost > total_fuel:
        break
    else:
        total_fuel = fuel_cost

print(total_fuel)

def partial_sum(num: int) -> int:
    """
    The partial sum, `1 + 2 + ... + num`.
    """
    return num * (num + 1) // 2

def get_required_fuel_advanced(target: int, positions: list[int]) -> int:
    """
    Finds the required fuel to move all positions to the target using the
    advanced procedure.
    """
    fuel: int = 0
    for position in positions:
        fuel += partial_sum(abs(target - position))
    return fuel

total_fuel = get_required_fuel_advanced(0, initial_positions)
for t in range(1,max(initial_positions)):
    fuel_cost = get_required_fuel_advanced(t, initial_positions)
    if fuel_cost > total_fuel:
        break
    else:
        total_fuel = fuel_cost

print(total_fuel)