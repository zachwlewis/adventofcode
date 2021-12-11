"""
adventofcode.com
Day 11
https://adventofcode.com/2021/day/11
"""

import fr

inputs: list[str] = fr.read_as_list('input11')

def idx(x:int, y:int) -> int:
    return x + y * 10

def valid(x: int, y: int) -> bool:
    return x >= 0 and x < 10 and y >= 0 and y < 10

data: list[int] = []
neighbors: list[list[int]] = []

for row in inputs:
    r_d = list(map(int,list(row)))
    data.extend(r_d)


for y in range(10):
    for x in range(10):
        n: list[int] = []
        if valid(x,y-1): n.append(idx(x,y-1))       # North
        if valid(x+1,y-1): n.append(idx(x+1,y-1))   # Northeast
        if valid(x+1,y): n.append(idx(x+1,y))       # East
        if valid(x+1,y+1): n.append(idx(x+1,y+1))   # Southeast
        if valid(x,y+1): n.append(idx(x,y+1))       # South
        if valid(x-1,y+1): n.append(idx(x-1,y+1))   # Southwest
        if valid(x-1,y): n.append(idx(x-1,y))       # West
        if valid(x-1,y-1): n.append(idx(x-1,y-1))   # Northwest
        neighbors.append(n)


def out():
    for y in range(10):
        for x in range(10):
            print(f'{data[idx(x,y)]}',end='')
        print('')

flashes: list[int] = []
sync: list[int] = []
for step in range(250):
    did_flash: bool = True
    # At the start of each step, increment all values by 1
    for i, v in enumerate(data): data[i] = v + 1

    # Process explosion until no more flashes.
    has_flashed: set[int] = set()
    while did_flash:
        did_flash = False
        for i, v in enumerate(data):
            if v > 9 and not (i in has_flashed):
                did_flash = True
                has_flashed.add(i)
                for n in neighbors[i]:
                    data[n] = data[n] + 1
    
    # Reset all flashes to 0 and count them.
    flashes.append(len(has_flashed))
    if len(has_flashed) == 100: sync.append(step+1)
    for f in has_flashed:
        data[f] = 0

print(sum(flashes[0:100]))
print(sync[0])
