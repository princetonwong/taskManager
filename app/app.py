from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from typing import List
from .model import Task, User, TaskRead
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
    addSampleData()


@app.post("/addSampleData/", response_model=List[TaskRead], include_in_schema=False)
def addSampleData():
    db = Database().session
    if db.query(Task).count() > 0:
        logging.info(f"Sample data already added")
        return

    users = [User(id="d0e3d3e0-0b7e-4b1e-8b7a-5b0b6b9b0b6b"),
             User(id="d0e3d3e0-0b7e-4b1e-8b7a-5b0b6b9b0b6c"),
        ]
    for user in users:
        if not db.get(User, user.id):
            db.add(user)
            db.commit()

    taskData = [("Do the dishes", "I should do the dishes today", False, users[0].id),
                ("Do the laundry", "I should do the laundry today", False, users[0].id),
                ("Do the backyard", "I should do the backyard today", True, users[1].id)
                ]
    for task in taskData:
        db.add(Task(name=task[0], description=task[1], done=task[2], created_by=task[3], updated_by=task[3]))
    db.commit()
    logging.info(f"Sample data added")
    return db.query(Task).all()


@app.get("/", tags=["root"])
async def root():
    return RedirectResponse(url="/docs")

