from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse

from .helper import Helper
from .api import TaskRouter
from .auth import AuthRouter
from .database import Database
import logging

logging.basicConfig(level=logging.INFO)
origins = ["*"]
middlewares = [
    Middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]),
    Middleware(SessionMiddleware, secret_key=Helper().getEnv("SUPABASE_KEY")),
]
app = FastAPI(middleware=middlewares)
app.include_router(AuthRouter, prefix="/auth", tags=["auth"])
app.include_router(TaskRouter, prefix="/api/v1", tags=["task"])


@app.on_event("startup")
def on_startup():
    Database().init_db()
    Database().listAllTables()


@app.get("/", tags=["root"])
async def root():
    return RedirectResponse(url="/docs")

