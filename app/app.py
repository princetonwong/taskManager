from fastapi import FastAPI
from .db import Database
import logging

logging.basicConfig(level=logging.INFO)
app = FastAPI()
Database().init_db()
Database().listAllTables()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

