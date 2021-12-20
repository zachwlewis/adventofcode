'''
adventofcode.com
Day 18
https://adventofcode.com/2021/day/18
'''

from __future__ import annotations
from typing import Union
import fr


INPUTS: list[str] = fr.read_as_list('input18')

class SFNum:
    '''
    Describes a snailfish number.
    '''
    def __init__(self, x: Union[int, SFNum], y: Union[int, SFNum]) -> None: # pylint: disable=unsubscriptable-object
        self.x_elem = x
        self.y_elem = y

    def __str__(self) -> str:
        return f'[{str(self.x_elem)},{str(self.y_elem)}]'

    def __add__(self, other) -> SFNum:
        reduced = SFNum(self, other)
        print(f'add {reduced}')
        reduced.reduce()
        return reduced

    @classmethod
    def from_split(cls: SFNum, value: int) -> SFNum:
        '''
        Creates a new SFNum by splitting a value.
        '''
        left = value // 2
        right = int(value / 2 + 0.5)
        return SFNum(left, right)

    @classmethod
    def from_str(cls: SFNum, value: str) -> Union[int, SFNum]:
        '''
        Creates a new SFNum by parsing a string.
        '''

        if value.find(',') == -1:
            return int(value)

        c: int = 0
        split: int = 0
        for i, v in enumerate(value):
            if v == '[': c += 1   
            elif v == ']': c -= 1
            elif v == ',' and c == 1:
                split = i
                break
        

        return SFNum(SFNum.from_str(value[1:split]), SFNum.from_str(value[split+1:-1]))


    def reduce(self) -> None:
        while True:
            did_explode, _, _ = self.explode()
            if did_explode:
                print(f'explode: {self}')
                continue
            if self.split():
                print(f'split {self}')
                continue
            return

    def explode(self, level: int = 0) -> tuple[bool, int, int]:
        '''
        Explodes in place.

        Returns if an explode happened.
        '''
        if level < 3:
            if isinstance(self.x_elem, SFNum):
                did_explode, left, right = self.x_elem.explode(level + 1)
                print(f'Left: {level}, {did_explode}, {left}, {right} {self}')
                if did_explode:
                    if isinstance(self.x_elem, int):
                        if left != -1: self.x_elem += left
                        left = -1
                    if (isinstance(self.y_elem, int)):
                        if right != -1: self.y_elem += right
                        right = -1
                    return True, left, right

            if isinstance(self.y_elem, SFNum):
                did_explode, left, right = self.y_elem.explode(level + 1)
                print(f'Right: {level}, {did_explode}, {left}, {right} {self}')
                if did_explode:
                    if isinstance(self.x_elem, int):
                        if left != -1: self.x_elem += left
                        left = -1
                    if (isinstance(self.y_elem, int)):
                        if right != -1: self.y_elem += right
                        right = -1
                    return True, left, right
        else:
            if isinstance(self.x_elem, SFNum):
                left = self.x_elem.x_elem
                right = -1

                self.y_elem += self.x_elem.y_elem
                self.x_elem = 0
                return True, left, right
            if isinstance(self.y_elem, SFNum):
                left = -1
                right = self.y_elem.y_elem
                self.x_elem += self.y_elem.x_elem
                self.y_elem = 0
                return True, left, right

        return (False, -1, -1)

    def split(self) -> bool:
        '''
        Splits in place.

        Returns if a split happened.
        '''
        if isinstance(self.x_elem, SFNum):
            if self.x_elem.split():
                return True
        else:
            if self.x_elem >= 10:
                self.x_elem = SFNum.from_split(self.x_elem)
                return True

        if isinstance(self.y_elem, SFNum):
            if self.y_elem.split():
                return True
        else:
            if self.y_elem >= 10:
                self.y_elem = SFNum.from_split(self.y_elem)
                return True

        return False

"""
This snailfish homework is about addition. To add two snailfish numbers, form a pair from the
left and right parameters of the addition operator.

For example, [1,2] + [[3,4],5] becomes [[1,2],[[3,4],5]].
"""

# ex1 = SFNum(1,2)
# ex2 = SFNum(SFNum(3,4),5)

# print(f'{ex1} + {ex2} = {ex1 + ex2}')


# To explode a pair, the pair's left value is added to the first regular number to the left of the
# exploding pair (if any), and the pair's right value is added to the first regular number to the
# right of the exploding pair (if any). Exploding pairs will always consist of two regular numbers.
# Then, the entire exploding pair is replaced with the regular number 0.

# Here are some examples of a single explode action:

# [[[[[9,8],1],2],3],4] becomes [[[[0,9],2],3],4] (the 9 has no regular number to its left, so it is
# not added to any regular number).

# [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]] becomes [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
# (the pair [3,2] is unaffected because the pair [7,3] is further to the left; [3,2]
# would explode on the next action).

# [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]] becomes [[3,[2,[8,0]]],[9,[5,[7,0]]]].

# ex_explode3 = SFNum.from_str('[[6,[5,[4,[3,2]]]],1]')
# print(ex_explode3)
# ex_explode3.explode()
# print(ex_explode3)

# ex_explode = SFNum(SFNum(SFNum(SFNum(SFNum(9,8),1),2),3),4)
# ex_explode.reduce()
# print(ex_explode)
#print(ex_explode, ex_explode.explode())
#print(ex_explode, ex_explode.explode())

# ex_explode2_left = SFNum(3,SFNum(2,SFNum(1,SFNum(7,3))))
# ex_explode2_right = SFNum(6,SFNum(5,SFNum(4,SFNum(3,2))))
# ex_explode2 = SFNum(ex_explode2_left, ex_explode2_right)

# ex_explode2.reduce()
# print('----------')
# print(ex_explode2)
# print(ex_explode2, ex_explode2.explode())
# print(ex_explode2, ex_explode2.explode())
# print(ex_explode2, ex_explode2.explode())


# To split a regular number, replace it with a pair; the left element of the pair should be the
# regular number divided by two and rounded down, while the right element of the pair should be the
# regular number divided by two and rounded up. For example, 10 becomes [5,5], 11 becomes [5,6], 12
# becomes [6,6], and so on.

# print('------')
# print(SFNum.from_split(10))
# print(SFNum.from_split(11))
# print(SFNum.from_split(12))

# ex_split = SFNum(11,17)
# ex_split.reduce()
# print(ex_split)
# print(ex_split, ex_split.split())
# print(ex_split, ex_split.split())
# print(ex_split, ex_split.split())

# [[[[4,3],4],4],[7,[[8,4],9]]] + [1,1]
a = SFNum.from_str('[[[[4,3],4],4],[7,[[8,4],9]]]')
b = SFNum(1,1)

print(f'{a} + {b} = {a + b}')