from database.database import Database


class Grid:
    def __init__(self, file_path: str) -> None:
        self._db = Database(file_path)

    @property
    def height(self) -> int:
        return self._db.num_of_rows

    @property
    def width(self) -> int:
        return self._db.num_of_cols

    def is_land(self, x: int, y: int) -> bool:
        return self._db.read('map', x, y) == 1

    def is_visited(self, x: int, y: int) -> bool:
        return self._db.read('visited', x, y) == 1

    def mark_as_visited(self, x: int, y: int):
        self._db.update('visited', x, y, 1)

    def is_in_matrix(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def is_in_matrix_and_unvisited_and_land(self, x: int, y: int) -> bool:
        if not self.is_in_matrix(x, y):
            return False
        return not self.is_visited(x, y) and self.is_land(x, y)
