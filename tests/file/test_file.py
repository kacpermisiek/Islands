import os
import pytest
from file.file import DataError, VisitedFile, File, OriginalFile
from tests.grid.test_grid import GridSize


def file_path(file_name: str) -> str:
    return os.path.join(os.getcwd(), 'tests/utils/grid_files', file_name)


class TestOriginalFile:
    @pytest.fixture
    def sut(self, file_name: str) -> OriginalFile:
        return OriginalFile(file_path(file_name), 8)

    @pytest.mark.parametrize("file_name, expected_size", [
        ('data_9x8', GridSize(rows=8, cols=9)),
        ('data_1x1', GridSize(rows=1, cols=1)),
        ('data_10x1', GridSize(rows=1, cols=10)),
        ('data_1x10', GridSize(rows=10, cols=1)),
        ('data_1000x1000', GridSize(rows=1000, cols=1000))
    ])
    def test_file_should_return_proper_num_of_rows_and_cols(
            self, sut: OriginalFile, file_name: str, expected_size: GridSize) -> None:
        assert sut.rows == expected_size.rows
        assert sut.cols == expected_size.cols

    @pytest.mark.parametrize("file_name, x, y, expected_value", [
        ("data_9x8", 0, 0, 9),
        ("data_9x8", 1, 0, 8),
        ("data_9x8", 0, 1, 7),
        ("data_9x8", 2, 2, 6),
        ('data_10x1', 0, 0, 2),
        ('data_10x1', 1, 0, 3),
        ('data_10x1', 9, 0, 9),
        ('data_1x10', 0, 0, 1),
        ('data_1x10', 0, 1, 2),
        ('data_1x10', 0, 2, 3),
        ('data_1x10', 0, 8, 9),
        ('data_1x10', 0, 9, 0),
    ])
    def test_file_should_read_value_properly(
            self, sut: File, file_name: str, x: int, y: int, expected_value: chr) -> None:
        assert sut.read(x, y) == expected_value

    @pytest.mark.parametrize("file_name, x, y", [
        ("data_9x8", 100, 33),
        ("data_10x1", 1, 1),
    ])
    def test_file_should_raise_error_when_not_proper_coordinates_have_been_passed(
            self, sut: File, file_name: str, x: int, y: int) -> None:
        with pytest.raises(DataError):
            sut.read(x, y)


class TestVisitedGrid:
    @pytest.fixture
    def sut(self, x, y) -> VisitedFile:
        return VisitedFile(x, y, 8)

    @staticmethod
    def assert_file_is_prepared(expected_x: int, expected_y: int) -> None:
        with open("tmp_file.txt") as file:
            output = file.readlines()
            assert len(output) == expected_x
            if len(output) > 0:
                assert len(output[0]) == expected_y + 1

    @pytest.mark.parametrize("x, y", [
        (1, 1),
        (3, 3),
        (34, 23),
        (1000, 997),
        (1, 656),
        (656, 1),
    ])
    def test_should_prepare_visited_file(self, sut, x, y) -> None:
        self.assert_file_is_prepared(x, y)

    @pytest.mark.parametrize("file_name, x, y", [
        ("data_10x1", 1, 1),
    ])
    def test_file_should_raise_error_when_not_proper_coordinates_have_been_passed(
            self, sut: VisitedFile, file_name: str, x: int, y: int) -> None:
        with pytest.raises(DataError):
            sut.mark(x, y)
