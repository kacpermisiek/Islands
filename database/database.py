import os
import sqlite3


class DataError(Exception):
    pass


class Database:
    def __init__(self, file_path):
        self.num_of_rows = 0
        self._num_of_elements = 0
        self._conn = sqlite3.connect('coordinates.db')
        self._cursor = self._conn.cursor()
        self._prepare_database(file_path)
        self.num_of_cols = self._calculate_num_of_cols()

    def _prepare_database(self, file_path):
        self._create_tables()
        with open(file_path, "r") as file:
            for line in file:
                self.num_of_rows += 1
                for char in line.strip():
                    self._insert_into_table('map', char)
                    self._insert_into_table('visited', 0)
                    self._num_of_elements += 1
        self._conn.commit()

    def _create_tables(self):
        self._create_table('map')
        self._create_table('visited')

    def _insert_into_table(self, table, char):
        self._cursor.execute(f"INSERT INTO {table} (val) VALUES (?)", (char,))

    def _create_table(self, name):
        self._cursor.execute(
            f"CREATE TABLE {name} (id INTEGER PRIMARY KEY AUTOINCREMENT, val INTEGER)")
        self._commit()

    def read(self, table, x, y):
        print("read")
        idx = x + y * self.num_of_cols + 1
        return self._cursor.execute(f"SELECT val FROM {table} WHERE id={idx}").fetchone()[0]

    def update(self, table, x, y, val):
        idx = x + 1 + y * self.num_of_cols
        self._cursor.execute(f"UPDATE {table} SET val=? WHERE id=?", (val, idx))
        self._commit()

    def __del__(self):
        self._conn.close()
        os.remove('coordinates.db')

    def _commit(self):
        self._conn.commit()

    def _calculate_num_of_cols(self):
        if self.num_of_rows == 0:
            raise DataError
        return int(self._num_of_elements / self.num_of_rows)
