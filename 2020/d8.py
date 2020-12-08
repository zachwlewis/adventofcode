## adventofcode.com
# Day 8
# https://adventofcode.com/2020/day/8

from hc import HCI, HanCon

# inputs = fr.readAsList('input8')

console = HanCon('input8')

visited = set()
op_max = 0

while not console.op in visited:
  visited.add(console.op)

  if (console.op > op_max):
    op_max = console.op
    inst = console.currentInstruction()
    if   inst.ins == 'jmp' and inst.val < 0: print(f'[{op_max}] {inst}')
    elif inst.ins == 'nop' and inst.val + op_max >= len(console): print(f'[{op_max}] {inst}')

  console.tick()

answer1 = console.acc
answer2 = 'unknown'
console.loadROM('input8-fixed')

for change in range(0, len(console)):
  console.loadROM('input8-fixed')
  if console.rom[change].ins == 'acc': continue
  console.rom[change].ins = 'jmp' if console.rom[change].ins == 'nop' else 'nop'
  print(f'L{change}')
  v = set()

  while not console.op in v:
    v.add(console.op)
    console.tick()
    if console.status == 'end':
      answer2 = console.acc
      break

  if answer2 != 'unknown': break


print(f'Answer 1: {answer1}')
print(f'Answer 2: {answer2}')