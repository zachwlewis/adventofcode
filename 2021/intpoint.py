"""This supports easy loading of int points."""

from dataclasses import dataclass

@dataclass
class IntPoint:
    x: int = 0
    y: int = 0

    def __str__(self) -> str:
        return f'{self.x},{self.y}'

    def __repr__(self) -> str:
        return str(self)

    def __add__(self, other):
        return IntPoint(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return IntPoint(self.x - other.x, self.y - other.y)

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y

    def unit(self):
        x = self.x // abs(self.x) if self.x != 0 else 0
        y = self.y // abs(self.y) if self.y != 0 else 0
        return IntPoint(x,y)

    @classmethod
    def from_str(IntPoint, s:str) -> 'IntPoint':
        """Takes a string in the form `x,y` and returns an IntPoint."""
        values = s.split(',')
        return IntPoint(int(values[0]), int(values[1]))