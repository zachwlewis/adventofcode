"""
adventofcode.com
Day 8
https://adventofcode.com/2021/day/8
"""

import fr

inputs: list[str] = fr.read_as_list('input8')

def part1():
    count: int = 0
    for input in inputs:
        for output in input.split(' ')[-4:]:
            if len(output) == 2 or len(output) == 3 or len(output) == 4 or len(output) == 7:
                count += 1
    print(count)

part1()

def parse_line(line: str):
    _ = line.split(' ')
    encoded_digits = list(map(set, _[0:10]))
    encoded_output = list(map(set, _[-4:]))

    return encoded_digits, encoded_output

def decode(encoded_digits: list[set[str]]):
    cipher = [set()] * 10
    fives: list[set] = []
    sixes: list[set] = []

    for digit in encoded_digits:
        size = len(digit)
        if size == 2: cipher[1] = digit
        elif size == 3: cipher[7] = digit
        elif size == 4: cipher[4] = digit
        elif size == 5: fives.append(digit)
        elif size == 6: sixes.append(digit)
        elif size == 7: cipher[8] = digit
        else: print(f'bad input: {digit}')

    a = cipher[7] ^ cipher[1]
    bd = cipher[4] ^ cipher[1]
    abfg = sixes[0] & sixes[1] & sixes[2]
    cde = cipher[8] ^ abfg
    d = cde & bd
    fg = cipher[8] - (cde | a | bd)
    f = fg & cipher[1]
    g = fg ^ f
    c = cipher[1] - f
    b = bd - d
    e = cde - (c | d)

    cipher[0] = cipher[8] - d
    cipher[2] = cipher[8] - (b | f)
    cipher[3] = cipher[8] - (b | e)
    cipher[5] = cipher[8] - (c | e)
    cipher[6] = cipher[8] - c
    cipher[9] = cipher[8] - e

    return cipher


def part2():
    total = 0
    for input in inputs:
        digits, output = parse_line(input)
        cipher = decode(digits)
        out = list(map(cipher.index, output))
        total += 1000*out[0]+100*out[1]+10*out[2]+out[3]

    print(total)

part2()
