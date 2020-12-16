## adventofcode.com
# Day 15
# https://adventofcode.com/2020/day/15

import fr

answer1 = 'unknown'
answer2 = 'unknown'

# inputs: list[str] = fr.readAsList('input15')

puzzleInputs = [0,13,1,8,6,15]

# Save the history of spoken numbers as a dictionary.
# The value of each item contains the number of the
# last two turns it was spoken.

history: dict[int, tuple[int, int]] = {}

def takeTurn(lastNumber: int, turn: int) -> int:
  """Takes a turn of the game.  
  Returns the value spoken."""
  if not lastNumber in history:
    # This is a new number!
    # Add it to the history and say 0.
    history[lastNumber] = (0, turn)
    return 0

  # This number has been spoken before.
  # Update the remembered turns.
  # Say the difference between turns spoken.
  history[lastNumber] = (history[lastNumber][1], turn)
  return history[lastNumber][1] - history[lastNumber][0]

turn = 0
num = 0
for init in puzzleInputs:
  turn += 1
  takeTurn(init, turn)

while turn <= 30000000:
  turn += 1
  if turn == 2020: answer1 = num
  if turn == 30000000: answer2 = num
  num = takeTurn(num, turn)

print(f'Answer 1: {answer1}')
print(f'Answer 2: {answer2}')