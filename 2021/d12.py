"""
adventofcode.com
Day 12
https://adventofcode.com/2021/day/12

Got heckin' stuck on this one. Did a cheat.
https://github.com/plan-x64/advent-of-code-2021/blob/main/advent/day12.py
"""

from collections import (defaultdict, deque)
import fr

inputs: list[str] = fr.read_as_list('input12')

def parse_graph(input):
    graph = defaultdict(set)
    for connection in input:
        (v1, v2) = tuple(connection.split('-'))
        graph[v1].add(v2) 
        graph[v2].add(v1)

    return graph

def part1_path_filter(possible_vertex, current_path):
    return possible_vertex.isupper() or possible_vertex not in current_path

def part2_path_filter(possible_vertex, current_path):
    lower = [vertex for vertex in current_path if vertex.islower()]
    is_small_duplicate = len(lower) != len(set(lower))
    return part1_path_filter(possible_vertex, current_path) or (possible_vertex != 'start' and not is_small_duplicate)

def find_all_paths(graph, path_filter):
    paths = deque([['start']])

    valid_paths = []
    while paths:
        current_path = paths.pop()
        current_vertex = current_path[-1]

        if current_vertex == 'end':
            valid_paths.append(current_path)
            continue

        for connected_vertex in graph[current_vertex]:
            if path_filter(connected_vertex, current_path):
                paths.append(current_path + [connected_vertex])

    return valid_paths


graph = parse_graph(inputs)

print(len(find_all_paths(graph, part1_path_filter)))
print(len(find_all_paths(graph, part2_path_filter)))
