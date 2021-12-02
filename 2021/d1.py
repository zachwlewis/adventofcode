"""
adventofcode.com
Day 1
https://adventofcode.com/2021/day/1
"""

import fr

inputs: list[int] = list(map(int, fr.read_as_list('input1')))
input_size = len(inputs)

increases: int = 0
for index in range(1,input_size):
    if inputs[index] > inputs[index-1]:
        increases += 1

print(increases)

def get_window_value(data: list[int], end: int) -> int:
    """Gets the window value of 3 items"""
    return data[end] + data[end-1] + data[end-2]

window_increases: int = 0
for index in range(3, input_size):
    if get_window_value(inputs, index) > get_window_value(inputs, index - 1):
        window_increases += 1

print(window_increases)
