from fastapi import FastAPI
from .database import Database
import logging
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware import Middleware
from .helper import Helper


logging.basicConfig(level=logging.INFO)
origins = ["*"]
middlewares = [
    Middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]),
    # Middleware(SessionMiddleware, secret_key=Helper().getEnv("SUPABASE_KEY")),
]
app = FastAPI(middleware=middlewares)
# app.include_router(AuthRouter, prefix="/auth", tags=["auth"])
from .api.taskAPI import TaskRouter
app.include_router(TaskRouter, prefix="/api/v1/task", tags=["task"])
from .api.heroAPI import HeroRouter
app.include_router(HeroRouter, prefix="/api/v1/hero", tags=["hero"])


@app.on_event("startup")
def on_startup():
    Database().init_db()
    Database().listAllTables()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
