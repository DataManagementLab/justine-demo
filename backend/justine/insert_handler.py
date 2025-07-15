from typing import Any

from .data.insert_data import InsertData
from .databases.database import Database
from .insert_parser import parse_insert
from .strategies.strategy import Strategy


class InsertHandler:
    def __init__(self, database: Database, strategy: Strategy) -> None:
        self.database = database
        self.strategy = strategy

    def handle_insert(self, insert: str) -> list[tuple[Any, ...]]:
        """Collects all required information for the execution of the insert and executes it on the database"""

        # Parse the insert of the user and collect information needed for execution
        insert_data = InsertData(insert, self.database.get_database_state())
        parse_insert(insert_data)

        # clean the insert data
        insert_data.clean()

        # If insert contains all information needed for execution, try to run it
        if insert_data.is_valid():
            try:
                adjusted_query = insert_data.get_insert()
                #print(f"{insert} -> {adjusted_query}")
                result = self.database.execute(adjusted_query)
                #print(result)
                return result, adjusted_query
            except Exception as e:
                print("Error while executing the query:", e)
                print("Trying to adjust the query...")

        insert_data.table = self.strategy.predict_table_name(insert_data).lower()
        insert_data.columns = [c.lower() for c in self.strategy.predict_column_mapping(insert_data)]

        if insert_data.table not in insert_data.database_state.keys():
            # Create database table if it does not already exist
            #print(f"Creating table {insert_data.table} with columns {', '.join(f'{c} ({t})' for (c,t) in zip(insert_data.columns, insert_data.column_types))}")
            self.database.create_table(
                insert_data.table,
                insert_data.columns,
                insert_data.column_types,
            )
        else:
            # Create not-existing columns
            for index, column in enumerate(insert_data.columns):
                if not column in insert_data.database_state[insert_data.table][0]:
                    self.database.create_column(
                        insert_data.table,
                        column,
                        insert_data.column_types[index],
                    )

        adjusted_query = insert_data.get_insert()

        # Execute constructed insert
        return self.database.execute(adjusted_query), adjusted_query
