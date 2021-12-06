"""
adventofcode.com
Day 6
https://adventofcode.com/2021/day/6
"""

import fr

inputs: list[str] = fr.read_as_list('input6')

day: list[int] = [0] * 9

for i in map(int, inputs[0].split(',')):
    day[i] += 1

total_days = 256
for i in range(0, total_days):
    new_fish = day[0]
    day = day[1:]
    day[6] += new_fish
    day.append(new_fish)
    if (i == 79):
        print(sum(day))

print(sum(day))
