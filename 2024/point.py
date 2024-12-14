from typing import Any
class IntPoint2:
    """A point in 2D space."""
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @property
    def t(self) -> tuple[int, int]:
        return self.x, self.y
    
    @t.setter
    def t(self, value: tuple[int, int]) -> None:
        self.x, self.y = value
    
    def __add__(self, other: 'IntPoint2') -> 'IntPoint2':
        return IntPoint2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'IntPoint2') -> 'IntPoint2':
        return IntPoint2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other: Any) -> 'IntPoint2':
        # If other is an IntPoint2, return an IntPoint2
        if isinstance(other, IntPoint2):
            return IntPoint2(self.x * other.x, self.y * other.y)
        else:
            return IntPoint2(self.x * other, self.y * other)
    
    def __floordiv__(self, other: Any) -> 'IntPoint2':
        if isinstance(other, IntPoint2):
            return IntPoint2(self.x // other.x, self.y // other.y)
        else:
            return IntPoint2(self.x // other, self.y // other)
    
    def __truediv__(self, other: 'IntPoint2') -> 'IntPoint2':
        return IntPoint2(self.x / other.x, self.y / other.y)
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def __copy__(self) -> 'IntPoint2':
        return IntPoint2(self.x, self.y)
    
    def __eq__(self, other: 'IntPoint2') -> bool:
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    