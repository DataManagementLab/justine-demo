import json
import os
import shutil
import sqlite3
from functools import cached_property
from justine.justine import Justine

import minidb

from data import Run, RunStep, Dataset, Interaction


class JustineAdapter:
    runs = {}
    interactions = {}

    def __init__(self):
        # Connect to database
        self.db = minidb.Store("./data.sqlite")
        self.db.register(Dataset)
        self.db.register(Run)
        self.db.register(RunStep)
        self.db.register(Interaction)
        self.justine = None

    def load(self):
        self.justine = Justine()

    def close(self):
        self.db.close()

    def new_run(self, settings: dict):
        dataset = self.databases[settings.dataset]

        run = Run(dataset=settings.dataset,
                  missing_table_names=settings.missingTableNames,
                  missing_column_names=settings.missingColumnNames,
                  num_iterations=dataset["num_inserts"]
                  )
        run.save(self.db)
        self.db.commit()

        self.runs[run.id] = {}
        self.runs[run.id]["settings"] = settings
        self.runs[run.id]["database_name"] = dataset['name']
        self.runs[run.id]["num_inserts"] = dataset["num_inserts"]

        # TODO Replace
        # Copy gold database to run folder
        #shutil.copy(f"data/{dataset['folder']}/{dataset['folder']}.sqlite", f"runs/{run.id}.sqlite")

        database, insert_handler = self.justine.new_batch(f"runs/{run.id}.sqlite")
        self.runs[run.id]["database"] = database
        self.runs[run.id]["insert_handler"] = insert_handler

        workload_file_name = f"data/{dataset['folder']}/inserts_only.sql"
        if settings.missingTableNames > 0 or settings.missingColumnNames > 0:
            # if file exists
            if os.path.exists(f"data/{dataset['folder']}/evaluation_input_0.5_0.5.sql"):
                workload_file_name = f"data/{dataset['folder']}/evaluation_input_0.5_0.5.sql"

        with open(workload_file_name, 'r', encoding="utf8") as file:
            lines = file.readlines()
            self.runs[run.id]["insert_lines"] = [line for line in lines if line.strip()]
        self.runs[run.id]["insert_index"] = -1

        return {
            "id": run.id,
            "dataset": settings.dataset,
            "dataset_name": dataset["name"],
            "missingTableNames": settings.missingTableNames,
            "missingColumnNames": settings.missingColumnNames,
            "tableSynonyms": settings.tableSynonyms,
            "columnsSynonyms": settings.columnsSynonyms,
            "startWithSchema": settings.startWithSchema,
            "fixSchema": settings.fixSchema,
            "num_iterations": dataset["num_inserts"]
        }

    @cached_property
    def databases(self):
        databases = []
        i = 0
        # Loop over subfolders in data folder
        for db_folder in os.listdir("data"):
            if os.path.isdir(f"data/{db_folder}"):
                # Load info json
                with open(f"data/{db_folder}/{db_folder}.json") as f:
                    db_info = json.load(f)
                db_info["folder"] = db_folder
                if not "name" in db_info:
                    db_info["name"] = db_folder.replace("_", " ")
                db_info["id"] = i
                i += 1
                if not "description" in db_info:
                    db_info["description"] = ""
                databases.append(db_info)
        return databases

    def next(self, run_id):
        self.runs[run_id]["insert_index"] += 1
        iteration = self.runs[run_id]["insert_index"]
        query = self.runs[run_id]["insert_lines"][iteration]

        # Perform the insert
        result, adjusted_query = self.justine.execute_sql(query,
                                     self.runs[run_id]["database"],
                                     self.runs[run_id]["insert_handler"]
                                     )

        # Get resulting database
        # Loop over all tables in the database
        tables = self._fetch_tables(f"runs/{run_id}.sqlite")

        more = True if iteration < self.runs[run_id]["num_inserts"] - 1 else False

        result = {
            "run_id": run_id,
            "iteration": iteration + 1,
            "tables": tables,
            "query": query,
            "adjusted_query": adjusted_query,
            "more": more,
            "raw_result": result,
        }
        run_step = RunStep(run=run_id,
                           iteration=iteration + 1,
                           cached_result=json.dumps(result)
                           )
        run_step.save(self.db)
        if not more or iteration % 10 == 0:
            self.db.commit()

        if not more:
            self.runs[run_id]["database"].close()

        return result

    def _fetch_tables(self, path):
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        tables = []
        # Query to get the list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = cursor.fetchall()
        for table_name in table_names:
            table_name = table_name[0]
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = [";".join(str(r) for r in row) for row in cursor.fetchall()]

            tables.append({
                "name": table_name,
                "columns": [description[0] for description in cursor.description],
                "data": rows,
                "row_count": len(rows),
            })
        # Close the connection
        conn.close()
        return tables

    def get_previous_runs(self):
        runs = [r.to_dict() for r in Run.load(self.db)]
        runs.sort(key=lambda x: x["id"], reverse=True)
        return runs

    def get_cached_run_step(self, iter_id, run_id):
        r = RunStep.get(self.db, run=run_id, iteration=iter_id)
        return json.loads(r.cached_result)

    def get_run_details(self, run_id):
        r = Run.get(self.db, id=run_id)
        r_details = r.to_dict()
        r_details["dataset_name"] =  self.databases[r_details['dataset']]["name"]
        return r_details

    def new_interaction(self, database_id=None):
        interaction = Interaction(database=database_id,
                                  num_interactions=0
                                  )
        interaction.save(self.db)
        self.db.commit()

        db_path = f"interactions/{interaction.id}.sqlite"

        if database_id is None:
            db_name = "Empty database"
            conn = sqlite3.connect(db_path)
            conn.close()
        else:
            dataset = self.databases[database_id]
            db_name = dataset["name"]
            shutil.copy(f"data/{dataset['folder']}/{dataset['folder']}.sqlite", db_path)

        database, insert_handler = self.justine.new_batch(db_path)

        self.interactions[interaction.id] = {
            "query_queue": [],
            "query_index": -1,
            "database": database,
            "insert_handler": insert_handler,
        }

        return {
            "id": interaction.id,
            "db": db_name
        }

    def get_interaction_state(self, interaction_id):
        return {
            "tables": self._fetch_tables(f"interactions/{interaction_id}.sqlite")
        }

    def add_queries_to_queue(self, interaction_id, queries):
        interaction_id = int(interaction_id)
        print(self.interactions)
        self.interactions[interaction_id]["query_queue"].extend(queries)
        result, adjusted_query = self.justine.execute_sql(queries[0],
                                     self.interactions[interaction_id]["database"],
                                     self.interactions[interaction_id]["insert_handler"]
                                     )
        return queries[0], adjusted_query


