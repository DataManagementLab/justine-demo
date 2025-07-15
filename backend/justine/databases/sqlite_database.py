from typing import Any
import sqlite3

from .database import Database


class SQLiteDatabase(Database):
    def __init__(self, path) -> None:
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

    def execute(
        self, statement: str, params: tuple[str, ...] = ()
    ) -> list[tuple[Any, ...]]:
        cursor = self.conn.cursor()
        cursor.execute(statement, params)
        output = cursor.fetchall()
        self.conn.commit()
        # cursor.close()
        return output

    def select_all_data(self, table_name: str) -> list[tuple[Any, ...]]:
        statement = f"SELECT * FROM {table_name};"
        return self.execute(statement)

    def get_all_tables(self) -> list[str]:
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [table_name[0] for table_name in self.cursor.fetchall()]

    def get_all_columns(self, table_name: str) -> list[tuple[str, str]]:
        self.cursor.execute(f"SELECT * FROM {table_name}")
        return [(description[0], description[1]) for description in self.cursor.description]

    def get_example_rows(self, table_name: str) -> list[tuple[Any, ...]]:
        statement = f"SELECT * FROM {table_name} LIMIT 3;"
        return self.execute(statement)

    def get_database_state(self) -> dict[str, tuple[list[str], list[tuple[Any, ...]]]]:
        return {
            table: (
                [column[0] for column in self.get_all_columns(table)],
                self.get_example_rows(table),
            )
            for table in self.get_all_tables()
        }

    def create_table(
        self, table_name: str, column_names: list[str], column_types: list[str]
    ) -> None:
        statement = f"CREATE TABLE {table_name} ({', '.join([f'{column[0]} {column[1]}' for column in zip(column_names, column_types)])});"
        self.execute(statement)

    def create_column(
        self, table_name: str, column_name: str, column_type: str
    ) -> None:
        statement = f"ALTER TABLE {table_name} ADD {column_name} {column_type};"
        self.execute(statement)

    def remove_table(self, table_name: str) -> None:
        statement = f"DROP TABLE {table_name};"
        self.execute(statement)

    def reset_database(self) -> None:
        for table in self.get_all_tables():
            self.remove_table(table)

    def close(self) -> None:
        self.conn.close()
