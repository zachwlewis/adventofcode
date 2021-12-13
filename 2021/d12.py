"""
adventofcode.com
Day 12
https://adventofcode.com/2021/day/12
"""
from __future__ import annotations
from typing import Type
import fr

inputs: list[str] = fr.read_as_list('input12_sample')

class Node:
    name: str = ''
    children: list[Node]

    @classmethod
    def link(self, a: Node, b: Node) -> None:
        a.add(b)
        b.add(a)

    def __init__(self, name:str) -> None:
        self.name = name
        self.children = []

    def add(self, node: Node) -> None:
        self.children.append(node)

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name

    def visit_once(self) -> bool:
        return self.name.lower() == self.name


cave_nodes: dict[str, Node] = dict()

for input in inputs:
    print(input)
    _ = input.split('-')
    start = _[0]
    end = _[1]
    if start not in cave_nodes:
        print(f'Creating node {start}.')
        cave_nodes[start] = Node(start)
    if end not in cave_nodes:
        print(f'Creating node {end}.')
        cave_nodes[end] = Node(end)

    Node.link(cave_nodes[start], cave_nodes[end])

def find_path(start: Node, path:list[Node]) -> list[list[Node]]:
    #if (start.name == 'end'):
