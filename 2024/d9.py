# adventofcode.com
# Day 9
# https://adventofcode.com/2024/day/9

import common
from grid import Grid
from point import IntPoint2

from dataclasses import dataclass

@dataclass
class DataBlock:
    id: int
    length: int

def get_input(s:str) -> list[int]:
    filename = common.getFilePath(s)
    data: list[int] = []
    with open(filename, "r") as file:
        data = [int(x) for x in file.read().strip()]

    return data

def uncompress_data(data: list[int]) -> list[int]:
    id = 0
    ud: list[int] = []
    add: bool = True
    for d in data:
        if add:
            # add d instances of id to ud
            for i in range(d):
                ud.append(id)
            id += 1
        else:
            for i in range(d):
                ud.append(-1)
        add = not add
    return ud

def compact_data(data: list[int]) -> list[int]:
    start, end = 0, len(data) - 1
    while start < end:
        if data[start] >= 0:
            start += 1
        elif data[end] < 0:
            end -= 1
        else:
            data[start], data[end] = data[end], data[start]
            start += 1
            end -= 1
    return data

def calculate_checksum(data: list[int]) -> int:
    checksum = 0
    for i in range(len(data)):
        if data[i] < 0:
            continue
        checksum += i * max(0,data[i])
    return checksum

def solution1(data: list[int]) -> int:
    ud = uncompress_data(data)
    cd = compact_data(ud)
    return calculate_checksum(cd)

# For solution 2, treat data as blocks of data.
def uncompress_blocks(data: list[int]) -> list[DataBlock]:
    blocks: list[DataBlock] = []
    id = 0
    add: bool = True
    for d in data:
        if add:
            blocks.append(DataBlock(id, d))
            id += 1
        else:
            blocks.append(DataBlock(-1, d))
        add = not add
    return blocks

def compact_blocks(blocks: list[DataBlock]) -> list[DataBlock]:
    # find the highest id
    highest_id = 0
    for block in blocks:
        highest_id = max(highest_id, block.id)

    for id in range(highest_id, -1, -1):
        # find the first block with id
        data_index, blank_index = -1, -1
        for i in range(len(blocks)):
            if blocks[i].id == id:
                data_index = i
                break

        # blocks[i] is the current block we are trying to move
        # find the first -1 block with length >= blocks[i].length
        for j in range(i):
            if blocks[j].id == -1 and blocks[j].length >= blocks[data_index].length:
                blank_index = j
                break

        if blank_index == -1:
            # No blank block with enough room found to move.
            continue

        # We have a blank block with enough room.
        blocks[blank_index].length -= blocks[data_index].length
        data: DataBlock = DataBlock(blocks[data_index].id, blocks[data_index].length)
        blocks[data_index].id = -1
        blocks.insert(blank_index, data)

    return blocks

def expand_blocks(blocks: list[DataBlock]) -> list[int]:
    data: list[int] = []
    for block in blocks:
        for i in range(block.length):
            data.append(block.id)
 
    return data

def solution2(data: list[int]) -> int:
    blocks = uncompress_blocks(data)
    compact = compact_blocks(blocks)
    expanded = expand_blocks(compact)
    return calculate_checksum(expanded)

test1 = [1,2,3,4,5]
test2 = [2,3,3,3,1,3,3,1,2,1,4,1,4,1,3,1,4,0,2]
input = get_input("input9.txt")
print("Test cases:")
print(f"S1: {solution1(test2)}")
print(f"S2: {solution2(test2)}")

print("Solutions:")
print(f"S1: {solution1(input)}")
print(f"S2: {solution2(input)}")
