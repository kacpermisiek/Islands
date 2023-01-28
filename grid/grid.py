from file.file import OriginalFile, VisitedFile


class Grid:
    def __init__(self, file_path: str) -> None:
        self._grid_path = OriginalFile(file_path)
        self._visited_path = VisitedFile(self._grid_path.rows, self._grid_path.cols)

    @property
    def height(self) -> int:
        return self._grid_path.rows

    @property
    def width(self) -> int:
        return self._grid_path.cols

    def is_land(self, x: int, y: int) -> bool:
        return self._grid_path.read(x, y) == 1

    def is_visited(self, x: int, y: int) -> bool:
        return self._visited_path.read(x, y) == 1

    def mark_as_visited(self, x: int, y: int):
        self._visited_path.mark(x, y)

    def is_in_matrix(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def is_in_matrix_and_unvisited_and_land(self, x: int, y: int) -> bool:
        if not self.is_in_matrix(x, y):
            return False
        return not self.is_visited(x, y) and self.is_land(x, y)
