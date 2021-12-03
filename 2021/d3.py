"""
adventofcode.com
Day 3
https://adventofcode.com/2021/day/3
"""

import fr

inputs: list[str] = fr.read_as_list('input3')


def part1(data):
    """Solves part 1."""
    
    input_size = len(data)
    bit_count = len(data[0])

    # Just add all the individual bits to get the
    # number of 1s and compare it to half the size
    # of the original list.

    bits = [0] * bit_count
    for input in data:
        for bit_index in range(0, bit_count):
            bits[bit_index] += int(input[bit_index])

    # Now we can calcluate our values.
    half_size = int(input_size / 2)
    gamma_bits = [0] * bit_count
    epsilon_bits = [0] * bit_count

    for bit_index in range(0, bit_count):
        gamma_bits[bit_index] = str(int(int(bits[bit_index]) / half_size))
        epsilon_bits[bit_index] = str(int(half_size / int(bits[bit_index])))

    gamma_rate = int(''.join(gamma_bits),2)
    epsilon_rate = int(''.join(epsilon_bits),2)
    print(gamma_rate * epsilon_rate)

def split_data(data, bit: int = 0) -> tuple[list[int], list[int]]:
    """Returns a set containing the most-common and least-common values
    for a given bit."""
    input_size = len(data)
    divisor = input_size / 2

    zeros = []
    ones = []

    bit_value = 0
    for input in data:
        bit_value += int(input[bit])
        if input[bit] == "1":
            ones.append(input)
        else:
            zeros.append(input)
    
    if divisor / bit_value > 1:
        return ones, zeros

    return zeros, ones

def part2(data):
    """Solves part 2."""
    o2, co2 = split_data(data, 0)
    bit = 1
    while len(o2) > 1:
        o2, _ = split_data(o2, bit)
        bit += 1

    bit = 1
    while len(co2) > 1:
        _, co2 = split_data(co2, bit)
        bit += 1

    o2_rating = int(''.join(o2[0]), 2)
    co2_rating = int(''.join(co2[0]), 2)

    print(o2_rating * co2_rating)


part1(inputs)
part2(inputs)
