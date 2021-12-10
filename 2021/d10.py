"""
adventofcode.com
Day 10
https://adventofcode.com/2021/day/10
"""

import fr

inputs: list[str] = fr.read_as_list('input10')

ERROR_SCORE = { ')': 3, ']': 57, '}': 1197, '>': 25137 }
CLOSING_SCORE = { ')': 1, ']': 2, '}': 3, '>': 4 }
PAIRS = { '(': ')', '{': '}', '[': ']', '<': '>' }

error_score: int = 0
closing_scores: list[int] = []
for index, line in enumerate(inputs, 1):
    LINE = list(line)
    brace_stack: list[str] = []
    valid_line: bool = True
    for character in LINE:
        if character in PAIRS:
            brace_stack.append(PAIRS[character])
        else:
            CLOSE = brace_stack.pop()
            if character != CLOSE:
                # print(f'{index}: Expected {CLOSE}, but found {character} instead.')
                error_score += ERROR_SCORE[character]
                valid_line = False
                break

    if not valid_line: continue
    brace_stack.reverse()

    closing_score: int = 0
    for character in brace_stack:
        closing_score = closing_score * 5 + CLOSING_SCORE[character]
    
    closing_scores.append(closing_score)
    #print(f'{index}: {"".join(brace_stack)} - {closing_score}')

print(error_score)
closing_scores.sort()
print(closing_scores[(len(closing_scores))//2])
