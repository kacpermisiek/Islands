import pytest
import os.path
from collections import namedtuple

from database.database import DataError
from grid.grid import Grid

GridSize = namedtuple("GridSize", ['rows', 'cols'])


def file_path(file_name: str) -> str:
    return os.path.join(os.getcwd(), 'tests/utils/grid_files', file_name)


class TestGrid:
    @pytest.fixture
    def sut(self, file_name):
        return Grid(file_path(file_name))

    @pytest.mark.parametrize("file_name, grid_size", [
        ('data_9x8', GridSize(rows=8, cols=9)),
        ('data_1x1', GridSize(rows=1, cols=1)),
        ('data_10x1', GridSize(rows=1, cols=10)),
        ('data_1x10', GridSize(rows=10, cols=1))
    ])
    def test_grid_should_return_num_of_cols_and_rows(
            self, sut: Grid, file_name: str, grid_size: GridSize) -> None:
        assert sut.width == grid_size.cols
        assert sut.height == grid_size.rows

    @pytest.mark.parametrize("file_name, x, y", [
        ('data_9x8', 3, 2),
        ('data_1x1', 0, 0),
        ('data_10x1', 5, 0),
        ('data_1x10', 0, 9),
        ('data_1000x1000', 56, 343)
    ])
    def test_coordinate_should_not_be_visited_when_it_was_not_visited_yet(
            self, sut: Grid, file_name: str, x: int, y: int) -> None:
        assert not sut.is_visited(x, y)
        sut.mark_as_visited(x, y)
        assert sut.is_visited(x, y)

    @pytest.mark.parametrize("file_name, x, y, expected_output", [
        ('data_9x8', 3, 2, True),
        ('data_1x1', 0, 0, True),
        ('data_10x1', 5, 0, True),
        ('data_1x10', 0, 9, True),
        ('data_9x8', -1, 0, False),
        ('data_1x1', 1, 1, False),
        ('data_10x1', 1, 5, False),
        ('data_1x10', 9, 1, False),
    ])
    def test_should_return_are_coordinates_in_matrix(
            self, sut: Grid, file_name: str, x: int, y: int, expected_output) -> None:
        assert sut.is_in_matrix(x, y) == expected_output

    @pytest.mark.parametrize("file_name, x, y, expected_output", [
        ('data_9x8', 1, 1, True),
        ('data_1x1', 0, 0, True),
        ('data_10x1', 4, 0, True),
        ('data_1x10', 0, 9, False),
        ('data_9x8', 8, 0, False),
        ('data_10x1', 5, 0, False),
        ('data_1x10', 0, 9, False),
    ])
    def test_should_return_is_coordinate_is_land(
            self, sut: Grid, file_name: str, x: int, y: int, expected_output) -> None:
        assert sut.is_land(x, y) == expected_output

    def test_should_raise_when_empty_file_is_being_passed(self):
        with pytest.raises(DataError):
            Grid(file_path("data_0x0"))
