import os
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager

from .composer import load_models

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/generate")
def generate_midi():
    return {"Hello": "World"}


@app.post("/dummy")
def generate_dummy():
    dummy_path = os.path.join(ROOT_DIR, "data/dummy.mid")
    #print(dummy_path)

    def iterfile():
        with open(dummy_path, mode="rb") as file_like:
            yield from file_like
    return StreamingResponse(iterfile(), media_type="audio/midi")