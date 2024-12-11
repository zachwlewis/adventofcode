# adventofcode.com
# Day 11
# https://adventofcode.com/2024/day/11

from typing import Dict

def blink(stones: list[int]) -> list[int]:
    """
    Every time you blink, the stones each simultaneously change according to the
    first applicable rule in this list:

    1. If the stone is engraved with the number 0, it is replaced by a stone
       engraved with the number 1.
    2. If the stone is engraved with a number that has an even number of digits,
       it is replaced by two stones. The left half of the digits are engraved on
       the new left stone, and the right half of the digits are engraved on the
       new right stone. (The new numbers don't keep extra leading zeroes: 1000
       would become stones 10 and 0.)
    3. If none of the other rules apply, the stone is replaced by a new stone;
       the old stone's number multiplied by 2024 is engraved on the new stone.
    """

    s: list[int] = []

    for stone in stones:
        if stone == 0:
            s.append(1)
        elif len(str(stone)) % 2 == 0:
            half = len(str(stone)) // 2
            s.append(int(str(stone)[:half]))
            s.append(int(str(stone)[half:]))
        else:
            s.append(stone * 2024)
    
    return s

def blinkMap(stones: Dict[int, int]) -> Dict[int, int]:
    """
    Same as blink, but with a map counting the number of stones with a given number.

    Hopefully, this fixes the issue of the array growing too quickly.
    """

    s: Dict[int,int] = {}
    for stone, count in stones.items():
        if stone == 0:
            s[1] = s.get(1, 0) + count
        elif len(str(stone)) % 2 == 0:
            half = len(str(stone)) // 2
            a = int(str(stone)[:half])
            b = int(str(stone)[half:])
            s[a] = s.get(a, 0) + count
            s[b] = s.get(b, 0) + count
        else:
            a = stone * 2024
            s[a] = s.get(a, 0) + count

    return s

def solution1(stones: list[int]) -> int:
    """
    Return the number of stones with the number 1 after 2024 blinks.
    """
    original = stones.copy()
    for _ in range(25):
        stones = blink(stones)

    return len(stones)

def solution2(stones: list[int]) -> int:
    """
    Need another approach, since the array grows too quickly.
    """

    # Convert stones into a map
    stone_map: Dict[int,int] = {}
    for stone in stones:
        if stone in stone_map:
            stone_map[stone] += 1
        else:
            stone_map[stone] = 1

    for _ in range(75):
        stone_map = blinkMap(stone_map)

    total = 0
    for count in stone_map.values():
        total += count

    return total

test = [125,17]
input = [9759, 0, 256219, 60, 1175776, 113, 6, 92833]

print("Test cases:")
print(f"S1: {solution1(test)}")
print(f"S2: {solution2(test)}")

print("Solutions:")
print(f"S1: {solution1(input)}")
print(f"S2: {solution2(input)}")
