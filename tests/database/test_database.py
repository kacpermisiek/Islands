import os

import pytest
from database.database import Database


def file_path(file_name):
    return os.path.join(os.getcwd(), 'tests/utils/grid_files', file_name)


class TestDatabase:
    @pytest.fixture
    def sut(self, file_name):
        return Database(file_path(file_name))

    @pytest.mark.parametrize("file_name, expected_cols, expected_rows", [
        ("data_1x1", 1, 1),
        ("data_1x10", 1, 10),
        ("data_9x8", 9, 8),
        ("data_10x1", 10, 1),
        #("data_100x100", 100, 100),
        #("data_1000x1000", 1000, 1000),
    ])
    def test_database_should_prepare_tables(self, sut, file_name, expected_rows, expected_cols):
        assert sut.num_of_cols == expected_cols
        assert sut.num_of_rows == expected_rows

    @pytest.mark.parametrize("file_name, x, y, expected_val", [
        ("data_1x1", 0, 0, 1),
        ("data_1x10", 0, 9, 0),
        ("data_9x8", 0, 1, 7),
        ("data_10x1", 1, 0, 3),
        ("data_100x100", 89, 37, 0),
    ])
    def test_database_should_read_data_correctly(self, sut, file_name, x, y, expected_val):
        assert sut.read('map', x, y) == expected_val
        assert sut.read('visited', x, y) == 0

    @pytest.mark.parametrize("file_name, x, y", [
        ("data_1x1", 0, 0),
        ("data_1x10", 0, 3),
        ("data_9x8", 3, 4),
        ("data_10x1", 7, 0),
        ("data_100x100", 89, 37),
    ])
    def test_database_should_update_data_correctly(self, sut, file_name, x, y):
        assert sut.read('visited', x, y) == 0
        sut.update('visited', x, y, 1)
        assert sut.read('visited', x, y) == 1
