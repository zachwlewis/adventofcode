# adventofcode.com
# Day 4
# https://adventofcode.com/2019/day/4

# How many sequences in [PMIN..PMAX] meet the following criteria:
# - It is a six-digit number.
# - The value is within the range given in your puzzle input.
# - Two adjacent digits are the same (like 22 in 122345).
# - Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

# Puzzle Input: 347312-805915

# Use inspection to determine actual min and max valid sets.
# No need to check below or above these.

# Actual Solution Space: 347777-799999

def calculateIncreasingChains(guess):
  # Split number into sequence of digits
  sequence = []
  for d in str(guess): sequence.append(int(d))

  # Check for valid length
  if len(sequence) != 6: return {0}
  
  # Walk sequence, looking for doubles and increasing values
  prev = -1
  chain = set()
  chainCount = 1
  for d in sequence:
    # Check for bad ordering
    if d < prev: return {0}

    # Build chain list
    if d == prev:
      chainCount += 1
    elif prev >= 0:
      chain.add(chainCount)
      chainCount = 1

    prev = d

  chain.add(chainCount)
  
  return chain


PMIN = 347312
PMAX = 805915

goodPasswords = 0
betterPasswords = 0

GOOD = {2, 3, 4, 5, 6}
BETTER = {2}

for n in range(PMIN, PMAX):
  # For all numbers in the range, calculate a set of
  # increasing chain lengths
  s = calculateIncreasingChains(n)

  # Check the chain lists against the acceptable ones.
  isGood = s & GOOD
  isBetter = s & BETTER
  if len(isGood) > 0:
    goodPasswords += 1
    if len(isBetter) > 0:
      betterPasswords += 1


print("Good passwords found: %d" % goodPasswords)
print("Better passwords found: %d" % betterPasswords)
