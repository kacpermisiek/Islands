import os.path
from abc import abstractmethod
from typing import BinaryIO, Iterable, Callable


BLOCK_SIZE = 16777216
EMPTY_BYTES_VARIABLE_SIZE = 33
BYTE_SIZE = 1


class DataError(Exception):
    pass


def raise_data_error():
    raise DataError


class File:
    def __init__(self, block_size=BLOCK_SIZE):
        self._block_size = block_size
        self.rows = self._num_of_rows()
        self.cols = self._num_of_cols()

    @property
    @abstractmethod
    def path(self):
        pass        # pragma: no cover

    def read(self, x: int, y: int) -> int:
        print("read")
        with open(self.path, "r+b") as file:
            id_of_byte = self._get_id_of_byte(x, y)
            i = 0
            for block in self._read_in_blocks(file):
                if self._byte_is_in_current_block(id_of_byte, i):
                    return self._specific_item_of_block(block, i, id_of_byte)
                i += 1
            raise DataError

    def _num_of_rows(self) -> int:
        result = 0
        with open(self.path, "rb") as file:
            for block in self._read_in_blocks(file):
                result += len([x for x in block if x == 10])
        return result

    def _num_of_cols(self) -> int:
        with open(self.path, "rb") as file:
            result = 0
            for block in self._read_in_blocks(file):
                for char in block:
                    if char == 10:
                        return result
                    result += 1
            raise DataError

    def _read_in_blocks(self, file_object: BinaryIO, emergency_func: Callable = None) -> Iterable:
        while True:
            data = file_object.read(self._block_size)
            if not data:
                if emergency_func:
                    emergency_func()
                break
            yield data

    def _specific_item_of_block(self, block: bytes, i: int, id_of_byte: int) -> int:
        try:
            return int(chr(block[id_of_byte - self._block_size * i]))
        except IndexError:
            raise DataError

    def _get_id_of_byte(self, x: int, y: int) -> int:
        return x + y * (self.cols + 1)

    def _byte_is_in_current_block(self, id_of_byte: int, i: int) -> bool:
        return id_of_byte <= self._block_size * (i + 1) - 1


class VisitedFile(File):
    def __init__(self, x: int, y: int, block_size: int = BLOCK_SIZE) -> None:
        self._path = os.path.join(os.getcwd(), "tmp_file.txt")
        self.prepare(x, y)
        super().__init__(block_size)

    @property
    def path(self):
        return self._path

    def prepare(self, x: int, y: int) -> None:
        with open(self._path, "w+b") as file:
            for _ in range(x):
                for _ in range(y):
                    file.write(b"0")
                file.write(b"\n")

    def mark(self, x: int, y: int) -> None:
        with open(self._path, "r+b") as file:
            self._mark(file, x, y)

    def _mark(self, file: BinaryIO, x: int, y: int) -> None:
        id_of_byte = self._get_id_of_byte(x, y)
        i = 0
        for block in self._read_in_blocks(file, raise_data_error):
            if self._byte_is_in_current_block(id_of_byte, i):
                self._update_block(block, file, id_of_byte, i)
                break
            i += 1

    def _update_block(self, block: bytes, file: BinaryIO, id_of_byte: int, i: int):
        pivot = self._get_pivot(i, id_of_byte, len(block))
        block = block[:pivot] + b"1" + block[pivot + 1:]
        file.seek(-len(block), 1)
        file.write(block)

    def _get_pivot(self, i: int, id_of_byte: int, len_of_block: int) -> int:
        pivot = id_of_byte - self._block_size * i
        self._validate_pivot(pivot, len_of_block)
        return pivot

    @staticmethod
    def _validate_pivot(pivot: int, len_of_block: int) -> None:
        if pivot >= len_of_block:
            raise DataError

    def __del__(self):
        try:
            os.remove(self.path)
        except FileNotFoundError:
            pass


class OriginalFile(File):
    def __init__(self, path, block_size: int = BLOCK_SIZE) -> None:
        self._path = path
        super().__init__(block_size)

    @property
    def path(self) -> str:
        return self._path
