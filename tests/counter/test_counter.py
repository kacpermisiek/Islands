import os
import pytest
from counter.counter import Counter


def file_path(file_name: str) -> str:
    return os.path.join(os.getcwd(), 'tests/counter/grid_files', file_name)


class TestCounter:
    @pytest.fixture
    def sut(self, file_name) -> Counter:
        return Counter(file_path(file_name))

    @pytest.mark.parametrize("file_name, expected_islands", [
        ("data_1x1", 0),
        ("data_5x1", 1),
        ("data_8x9", 4),
        ("data_3x3", 2),
        ("data_4x4", 1),
        ("data_100x100", 50)
    ])
    def test_counter_should_return_expected_num_of_islands(
            self, sut: Counter, file_name: str, expected_islands: int) -> None:
        assert sut.get_islands_count() == expected_islands
