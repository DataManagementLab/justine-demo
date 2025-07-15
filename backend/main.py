import os
import re

import uvicorn

from typing import Union
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from adapter import JustineAdapter

current_working_directory = os.getcwd()

justine_adapter = JustineAdapter()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # No need for startup functionality here yet
    justine_adapter.load()
    # Wait for the lifespan to finish
    yield
    # Commit changed values and close database
    justine_adapter.close()

app = FastAPI(lifespan=lifespan)
origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Access-Control-Allow-Origin"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/datasets/")
def get_datasets():
    return justine_adapter.databases

@app.get("/datasets/{id}")
def read_dataset(id: int):
    return justine_adapter.databases[id]

run_info = {
    "last_run_id": -1,
}
run_per_id_counter = {}

class RunSettings(BaseModel):
    dataset: int
    missingTableNames: int
    missingColumnNames: int
    tableSynonyms: int
    columnsSynonyms: int
    startWithSchema: str
    fixSchema: str


class QueriesBody(BaseModel):
    queries: str

@app.post("/batch/")
def new_batch(settings: RunSettings):
    info = justine_adapter.new_run(settings)
    return info

@app.get("/batch/{run_id}/next/")
def batch_next(run_id: int):
    return justine_adapter.next(run_id)

@app.get("/runs/")
def get_runs():
    return justine_adapter.get_previous_runs()

@app.get("/runs/{run_id}/")
def get_run(run_id: int):
    return justine_adapter.get_run_details(run_id)

@app.get("/runs/{run_id}/iteration/{iter_id}/")
def get_run_step(run_id: int, iter_id: int):
    return justine_adapter.get_cached_run_step(iter_id, run_id)

@app.post("/interaction/")
def new_interaction(database_id: str | None = None):
    if database_id is not None:
        database_id = int(database_id)
    return justine_adapter.new_interaction(database_id)

@app.get("/interaction/{interaction_id}/state/")
def get_interaction_state(interaction_id: int):
    return justine_adapter.get_interaction_state(interaction_id)

@app.post("/interaction/{interaction_id}/add-queries/")
def add_queries(interaction_id: int, body: QueriesBody):
    queries = [cleaned for q in re.split(";\n", body.queries) if (cleaned := q.strip()) != ""]
    query, adjusted_query = justine_adapter.add_queries_to_queue(interaction_id, queries)
    return {"query": query, "adjusted_query": adjusted_query}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)