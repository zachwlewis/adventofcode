# adventofcode.com
# Day 22
# https://adventofcode.com/2019/day/22

import common, math

from collections import deque
from typing import Tuple

INPUT = common.getFilePath('input22.txt')

# Card shuffling
# Deal: Reverse list order
# Cut: Move start of list
#      Positive cuts shift start index forward.
#      Negative cuts shift start index backwards,
#      wrapping around if required.
# Deal w/ Increment:

def cut(d: deque, count: int = 0) -> None:
  if count == 0: return
  d.rotate(-count)

def deal(d: deque, count: int = 0) -> None:
  if count == 0:
    d.reverse()
    return

  _d: deque = d.copy()
  while len(_d):
    d[0] = _d.popleft()
    d.rotate(-count)

def part1() -> None:
  deck = deque(range(0, 10007))
  # Ran regex on input to build function list:
  cut(deck, 8808)
  deal(deck, 59)
  deal(deck)
  deal(deck, 70)
  cut(deck, -5383)
  deal(deck, 4)
  deal(deck)
  cut(deck, 9582)
  deal(deck, 55)
  cut(deck, -355)
  deal(deck, 61)
  deal(deck)
  cut(deck, -6596)
  deal(deck, 8)
  cut(deck, 4034)
  deal(deck, 37)
  cut(deck, -8183)
  deal(deck, 16)
  cut(deck, 9529)
  deal(deck, 24)
  cut(deck, -7751)
  deal(deck, 15)
  cut(deck, -8886)
  deal(deck, 17)
  deal(deck)
  cut(deck, -1157)
  deal(deck, 74)
  cut(deck, -6960)
  deal(deck, 49)
  cut(deck, 9032)
  deal(deck, 47)
  cut(deck, 8101)
  deal(deck, 59)
  cut(deck, -8119)
  deal(deck, 35)
  cut(deck, -2017)
  deal(deck, 10)
  cut(deck, -4431)
  deal(deck, 47)
  cut(deck, 5712)
  deal(deck, 18)
  cut(deck, 4424)
  deal(deck, 69)
  cut(deck, 5382)
  deal(deck, 40)
  cut(deck, -4266)
  deal(deck, 58)
  cut(deck, -8911)
  deal(deck, 24)
  cut(deck, 8231)
  deal(deck, 74)
  cut(deck, -2055)
  deal(deck)
  cut(deck, -1308)
  deal(deck, 31)
  deal(deck)
  deal(deck, 18)
  cut(deck, 4815)
  deal(deck, 5)
  deal(deck)
  cut(deck, 1044)
  deal(deck, 75)
  deal(deck)
  deal(deck, 13)
  cut(deck, 177)
  deal(deck)
  deal(deck, 28)
  cut(deck, 5157)
  deal(deck, 31)
  deal(deck)
  cut(deck, -8934)
  deal(deck, 50)
  cut(deck, 4183)
  deal(deck, 50)
  cut(deck, 1296)
  deal(deck, 5)
  cut(deck, -5162)
  deal(deck, 52)
  deal(deck)
  cut(deck, -5207)
  deal(deck, 30)
  cut(deck, -2767)
  deal(deck, 71)
  deal(deck)
  cut(deck, 5671)
  deal(deck, 67)
  cut(deck, 4818)
  deal(deck, 35)
  cut(deck, 9234)
  deal(deck, 58)
  cut(deck, -8832)
  deal(deck, 72)
  cut(deck, 1289)
  deal(deck, 55)
  cut(deck, -8444)
  deal(deck)
  deal(deck, 19)
  cut(deck, -5512)
  deal(deck, 29)
  cut(deck, 3680)

  print(deck.index(2019))

# convert rules to linear polynomial.
# (g∘f)(x) = g(f(x))
def parse(L, rules):
  a,b = 1,0
  for s in rules[::-1]:
    if s == 'deal into new stack':
      a = -a
      b = L-b-1
      continue
    if s.startswith('cut'):
      n = int(s.split(' ')[1])
      b = (b+n)%L
      continue
    if s.startswith('deal with increment'):
      n = int(s.split(' ')[3])
      z = pow(n,L-2,L) # == modinv(n,L)
      a = a*z % L
      b = b*z % L
      continue
    raise Exception('unknown rule', s)
  return a,b

# modpow the polynomial: (ax+b)^m % n
# f(x) = ax+b
# g(x) = cx+d
# f^2(x) = a(ax+b)+b = aax + ab+b
# f(g(x)) = a(cx+d)+b = acx + ad+b
def polypow(a,b,m,n):
  if m==0:
    return 1,0
  if m%2==0:
    return polypow(a*a%n, (a*b+b)%n, m//2, n)
  else:
    c,d = polypow(a,b,m-1,n)
    return a*c%n, (a*d+b)%n

def shuffle2(L, N, pos, rules):
  a,b = parse(L,rules)
  a,b = polypow(a,b,N,L)
  return (pos*a+b)%L

def part2() -> None:
  rules = open(INPUT, 'r').read().split('\n')
  L = 119315717514047
  N = 101741582076661
  print(shuffle2(L,N,2020,rules))

part1()
part2()
