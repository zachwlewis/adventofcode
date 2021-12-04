"""
adventofcode.com
Day 4
https://adventofcode.com/2021/day/4
"""

import fr
import re

inputs: list[str] = fr.read_as_list('input4')
board_size = 5
numbers: list[int] = list(map(int, inputs[0].split(',')))

n_map = {}
for i in range(0, len(numbers)):
    n_map[numbers[i]] = i

def map_board_to_turn(board: list[int]) -> list[int]:
    for index in range(0, len(board)):
        board[index] = n_map[board[index]]
    return board

def parse_boards(data: list[str]) -> list[list[int]]:
    boards = []
    current_board: list[int] = []
    for row_index in range(0,len(data)):
        if row_index > 0 and row_index % 6 == 0:
            boards.append(map_board_to_turn(current_board))
            current_board = []
        elif row_index > 0:
            split_row = re.split(r'\s\s?', data[row_index])
            row_numbers = list(map(int, split_row))
            current_board.extend(row_numbers)

    boards.append(map_board_to_turn(current_board))
    return boards

boards = parse_boards(inputs[1:])

board_lines = [
    # Rows
    [ 0,  1,  2,  3,  4],
    [ 5,  6,  7,  8,  9],
    [10, 11, 12, 13, 14],
    [15, 16, 17, 18, 19],
    [20, 21, 22, 23, 24],
    # Columns
    [ 0,  5, 10, 15, 20],
    [ 1,  6, 11, 16, 21],
    [ 2,  7, 12, 17, 22],
    [ 3,  8, 13, 18, 23],
    [ 4,  9, 14, 19, 24],
    # Diagonals don't count
    #[ 0,  6, 12, 18, 24],
    #[ 4,  8, 12, 16, 20]
]

def get_winning_turn(board: list[int]) -> int:
    '''Takes a board and finds the turn at which it will win.'''
    min_turn = 100
    for line in board_lines:
        values = [100] * 5
        for i in range(0, 5):
            values[i] = board[line[i]]

        turn = max(values)
        min_turn = min(turn, min_turn)
    
    return min_turn

winning_turn = 100
winning_board = []
losing_turn = 0
losing_board = []
for board in boards:
    turn = get_winning_turn(board)
    if turn < winning_turn:
        winning_turn = turn
        winning_board = board
    if turn > losing_turn:
        losing_turn = turn
        losing_board = board

def get_board_score(board: list[int], turn: int) -> int:
    '''Scores a board by summing all the numbers that were not marked.'''
    score = 0
    for n in board:
        if n > turn:
            score += numbers[n]

    return score

print(get_board_score(winning_board, winning_turn) * numbers[winning_turn])
print(get_board_score(losing_board, losing_turn) * numbers[losing_turn])
