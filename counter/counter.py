from grid.grid import Grid

NEIGHBOUR_COMBINATIONS = [
    (-1, 1),
    (0, 1),
    (1, 1),
    (-1, 0),
    (1, 0),
    (-1, -1),
    (0, -1),
    (1, -1),
]


class Counter:
    def __init__(self, file_path: str) -> None:
        self.grid = Grid(file_path)

    def _get_neighbour_unmarked_island_tiles(self, x: int, y: int) -> list:
        neighbours = []
        for a, b in NEIGHBOUR_COMBINATIONS:
            new_x, new_y = x + a, y + b
            if self.grid.is_in_matrix_and_unvisited_and_land(new_x, new_y):
                neighbours.append((x + a, y + b))
        return neighbours

    def _find_and_mark_whole_island(self, initial_x: int, initial_y: int) -> None:
        island_tiles_to_check = [(initial_x, initial_y)]
        while island_tiles_to_check:
            x, y = island_tiles_to_check.pop()
            island_tiles_to_check.extend(self._get_neighbour_unmarked_island_tiles(x, y))
            self.grid.mark_as_visited(x, y)

    def get_islands_count(self) -> int:
        islands_count = 0
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                if not self.grid.is_visited(x, y) and self.grid.is_land(x, y):
                    islands_count += 1
                    self._find_and_mark_whole_island(x, y)
                else:
                    self.grid.mark_as_visited(x, y)
        return islands_count
