"""
adventofcode.com
Day 17
https://adventofcode.com/2021/day/17

target area: x=48..70, y=-189..-148
"""

"""
The probe's x,y position starts at 0,0. Then, it will follow some trajectory by
moving in steps. On each step, these changes occur in the following order:

- The probe's x position increases by its x velocity.
- The probe's y position increases by its y velocity.
- Due to drag, the probe's x velocity changes by 1 toward the value 0; that is,
  it decreases by 1 if it is greater than 0, increases by 1 if it is less than
  0, or does not change if it is already 0.
- Due to gravity, the probe's y velocity decreases by 1.
"""

TOP = -148
LEFT = 48
BOTTOM = -189
RIGHT = 70

def do_step(px:int, py:int, vx:int, vy:int) -> tuple[int, int, int, int]:
    px_n = px + vx
    py_n = py + vy
    vx_n = 0 if vx == 0 else vx - 1
    vy_n = vy - 1

    return (px_n, py_n, vx_n, vy_n)


def in_range(px: int, py: int) -> bool:
    HIT: bool = px >= LEFT and px <= RIGHT and py <= TOP and py >= BOTTOM
    return HIT

def run():
    max_height: int = 0

    for vx_i in range(100):
        for vy_i in range(200):
        #print(f'\n{vx_i}, {vy_i}: ', end='')
            px: int = 0
            py: int = 0
            vx: int = vx_i
            vy: int = vy_i
            step: int = 0
            py_max: int = 0
            hit: bool = False
            while px <= RIGHT and py >= BOTTOM and vx > 0:
                step += 1
                px, py, vx, vy = do_step(px, py, vx, vy)
                py_max = max(py_max, py)
            #print(f'{step}', end='')
                if in_range(px, py): print(f'Hit! {vx_i}, {vy_i}')
            
#  and py_max > max_height
# print(f'New record: {py_max}! v = ({vx_i}, {vy_i})')
# max_height = py_max

# run()

def fire(vx_initial: int, vy_initial: int) -> tuple[bool,int]:
    px:int = 0
    py:int = 0
    vx:int = vx_initial
    vy:int = vy_initial
    max_height = 0
    hit: bool = False
    step: int = 0
    while (vx > 0 and px < LEFT) or px <= RIGHT and py >= BOTTOM:
        step += 1
        px, py, vx, vy = do_step(px, py, vx, vy)
        max_height = max(py, max_height)
        if in_range(px, py):
            hit = True
            break

    # if hit: print(f'{vx_initial}, {vy_initial} hit the target after {step} steps. Max height: {max_height}')

    return (hit, max_height)

max_height: int = 0
hits: int = 0
for x in range(75):
    for y in range(-190,190):
        hit, height = fire(x, y)
        if hit:
            max_height = max(max_height, height)
            hits += 1

print(max_height)
print(hits)
