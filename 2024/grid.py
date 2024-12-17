from typing import TypeVar, Generic, Any
T = TypeVar('T')
class Grid(Generic[T]):
    """A wrapper class for accessing an array as a 2D grid."""
    def __init__(self, 
                 width_or_data: Any, 
                 height: int | None = None, 
                 default_value: T | None = None):
        # Check if first argument is a list of lists
        if isinstance(width_or_data, list):
            # Assume width_or_data is a 2D list
            data = width_or_data
            # Validate it's a rectangular grid
            if not data:
                raise ValueError("Data for Grid cannot be empty")
            row_length = len(data[0])
            if any(len(row) != row_length for row in data):
                raise ValueError("All rows in data must be of the same length")

            self._height = len(data)
            self._width = row_length
            self._grid = [item for row in data for item in row]

        else:
            # Assume width_or_data is width, and we have height and default_value
            if height is None or default_value is None:
                raise ValueError("If passing width and height, must also provide default_value")
            self._width = width_or_data
            self._height = height
            self._grid = [default_value] * (self._width * self._height)

    @property
    def width(self) -> int:
        """Returns the width of the grid."""
        return self._width
    
    @property
    def height(self) -> int:
        """Returns the height of the grid."""
        return self._height

    def find(self, value:T) -> tuple[int,int]:
        """Returns the index of the first occurrence of the value in the grid."""
        try:
            index = self._grid.index(value)
            x = index % self._width
            y = index // self._width
            return (x, y)
        except ValueError:
            return (-1, -1)
        
    def findAll(self, value:T) -> list[tuple[int,int]]:
        """Returns a list of all occurrences of the value in the grid."""
        return [(x % self._width, x // self._width) for x in range(len(self._grid)) if self._grid[x] == value]
        
    def count(self, value:T) -> int:
        """Returns the number of occurrences of the value in the grid."""
        return self._grid.count(value)
    
    def copy(self) -> 'Grid[T]':
        """Returns a copy of the grid."""
        copy = Grid(0,0,0)
        copy._width = self._width
        copy._height = self._height
        copy._grid = self._grid.copy()
        return copy
    
    def inBounds(self, indices:tuple[int,int]) -> bool:
        """Returns True if the indices are within the bounds of the grid."""
        x, y = indices
        return x >= 0 and x < self._width and y >= 0 and y < self._height
    
    def __len__(self) -> int:
        """Returns the number of elements in the grid."""
        return len(self._grid)
    
    def __getitem__(self, indices:tuple[int,int]) -> T:
        """Returns the element at the given index."""
        x, y = indices
        if x < 0 or x >= self._width or y < 0 or y >= self._height:
            raise IndexError(f"Grid index out of range: {(x, y)}")
        return self._grid[x + y * self._width]
    
    def __setitem__(self, indices:tuple[int,int], value:T) -> None:
        """Sets the element at the given index to the given value."""
        x, y = indices
        if x < 0 or x >= self._width or y < 0 or y >= self._height:
            raise IndexError(f"Grid index out of range: {(x, y)}")
        self._grid[x + y * self._width] = value

    def __repr__(self) -> str:
        """Returns a string representation of the grid."""
        return f'Grid: {self._width}×{self._height} ({len(self)})\n' + '\n'.join([''.join([str(self._grid[x + y * self._width]) for x in range(self._width)]) for y in range(self._height)])