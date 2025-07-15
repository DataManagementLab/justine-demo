"""
Manual test script for the system.

Pass the strategy as an argument when executing the script.
Possible: heuristic_exact, heuristic_fuzzy, heuristic_synonyms, llama3_finetuned, llama3_not_finetuned, gpt
"""
import os

import sys
import traceback
from pathlib import Path

from justine.utils.utils import get_finetuned_model_dir, load_env_variables

load_env_variables()


from justine.databases.sqlite_database import SQLiteDatabase
from justine.strategies.heuristic.heuristic_strategy import (
    HeuristicStrategy,
    MatchingAlgorithm,
)
from justine.strategies.llama3.llama3_strategy import Llama3Strategy
from tabulate import tabulate

from justine.insert_handler import InsertHandler


class Justine:
    def __init__(self):
        justine_path = Path(__file__).resolve().parent
        self.strategy = Llama3Strategy(
            os.path.join(justine_path, 'models', 'missing_tables_12000_1_csv_data_collator'),
            os.path.join(justine_path, 'models', 'missing_columns_12000_1_own_data_collator')
        )
        #self.database = SQLLiteDatabase()
        #self.insert_handler = InsertHandler(self.database, self.strategy)

    def new_batch(self, database_path: str):
        database = SQLiteDatabase(database_path)
        insert_handler = InsertHandler(database, self.strategy)
        return database, insert_handler

    def execute_sql(self, user_input: str, database, insert_handler):
        try:
            if user_input.lower().startswith("insert"):
                result, adjusted_query = insert_handler.handle_insert(user_input)
            elif user_input.lower() == "reset;":
                database.reset_database()
                result = None
                adjust_query = "RESET"
            else:
                result = database.execute(user_input)
                adjusted_query = user_input
            return result, adjusted_query
        except Exception as e:
            print(traceback.format_exc())
            return None, str(e)
