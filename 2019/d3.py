# adventofcode.com
# Day 3
# https://adventofcode.com/2019/day/3

import common

with open(common.getFilePath('input3.txt')) as f:
    inpt = f.read()

path1, path2 = inpt.strip().split('\n')
deltas = {'R': (1, 0), 'L': (-1, 0), 'U': (0, 1), 'D': (0, -1)}

def find_points(directions):
    steps, curr_x, curr_y = 0, 0, 0
    points = set()
    step_counts = {}

    for dir in directions.split(','):
        d, l = dir[:1], int(dir[1:])
        dx, dy = deltas[d]
        for _ in range(l):
            curr_x += dx
            curr_y += dy
            steps += 1
            points.add((curr_x, curr_y))
            step_counts.setdefault((curr_x, curr_y), steps)

    return points, step_counts

p1_points, p1_steps = find_points(path1)
p2_points, p2_steps = find_points(path2)

intersections = p1_points & p2_points

print("Closest Intersection: %d" % min(abs(x) + abs(y) for x, y in intersections))
print("Fewest Steps: %d" % min(p1_steps[point] + p2_steps[point] for point in intersections))
