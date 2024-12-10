from fastapi import FastAPI
from contextlib import asynccontextmanager

from .composer import load_models


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/generate")
def generate_midi():
    return {"Hello": "World"}


@app.post("/dummy")
def generate_dummy():

    return {"message": "ok"}