"""
adventofcode.com
Day 14
https://adventofcode.com/2021/day/14
"""

import fr

inputs: list[str] = fr.read_as_list('input14')

polymer: str = inputs[0]

conversion: dict[str,str] = dict()

for input in inputs[2:]:
    (key, value) = tuple(input.split(' -> '))
    conversion[key] = value

def pair_insertion(s: str) -> str:
    start: int = 0
    end: int = 1
    L = len(s)
    out: list[str] = []
    while end < L:
        out.append(s[start])
        out.append(conversion[s[start:end+1]])
        start += 1
        end += 1
    out.append(s[start])

    return ''.join(out)

step = polymer
for i in range(10):
    step = pair_insertion(step)

def score(s:str) -> int:
    LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    min_: int = len(s)
    max_: int = 0

    for letter in LETTERS:
        COUNT = s.count(letter)
        if COUNT == 0: continue
        min_ = min(COUNT, min_)
        max_ = max(COUNT, max_)

    return max_ - min_

print(score(step))

polymer_map: dict[str, int] = dict()
for c in conversion.keys():
    polymer_map[c] = 0

for i in range(len(polymer) - 1):
    s = polymer[i:i+2]
    v = polymer_map.get(s,0) + 1
    polymer_map[s] = v

def print_map(pm: dict[str,int]):
    for k, v in polymer_map.items():
        print(f'{k}: {v}')

def map_insertion(pm: dict[str,int]) -> dict[str,int]:
    out: dict[str,int] = pm.copy()
    for pair, count in pm.items():
        # AB becomes ACB
        A = pair[0]
        B = pair[1]
        C = conversion[pair]
        AC = f'{A}{C}'
        CB = f'{C}{B}'
        out[AC] += count
        out[CB] += count
        out[pair] -= count

    return out


for i in range(40):
    polymer_map = map_insertion(polymer_map)

def map_score(pm: dict[str,int]) -> int:
    s_map: dict[str,float] = {'A': 0,'B': 0,'C': 0,'D': 0,'E': 0,'F': 0,'G': 0,'H': 0,'I': 0,'J': 0,'K': 0,'L': 0,'M': 0,'N': 0,'O': 0,'P': 0,'Q': 0,'R': 0,'S': 0,'T': 0,'U': 0,'V': 0,'W': 0,'X': 0,'Y': 0,'Z': 0}
    for k, v in pm.items():
        s_map[k[0]] += v
        s_map[k[1]] += v

    _min = sum(s_map.values())
    
    for k,v in s_map.items():
        s_map[k] = v/2
        if v > 0:
            _min = min(_min, v/2)

    SCORES = s_map.values()
    return int(max(SCORES) - _min + 0.5)

print(map_score(polymer_map))
