from fastapi import APIRouter, Depends, HTTPException, Query, status
from ..model.taskModel import Task, TaskCreate, TaskRead, TaskUpdate
from typing import List
from sqlmodel import Session, select
from ..database import Database
from uuid import UUID
import logging

TaskRouter = APIRouter()


@TaskRouter.post("/addSampleData/", response_model=List[TaskRead], include_in_schema=False)
def addSampleData():
    db = Database().session
    if db.query(Task).count() > 0:
        logging.info(f"Sample data already added")
        return
    db.add(Task(name="Do the dishes", description="I should do the dishes today", done=False))
    db.add(Task(name="Do the laundry", description="I should do the laundry today", done=False))
    db.add(Task(name="Do the backyard", description="I should do the backyard today", done=True))
    db.commit()
    logging.info(f"Sample data added")
    return db.query(Task).all()

@TaskRouter.post("/tasks/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate,
                      db: Session = Depends(Database().getSession)):
    db_task = Task.from_orm(task)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@TaskRouter.get("/tasks/", response_model=List[TaskRead], status_code=status.HTTP_200_OK)
async def read_tasks(offset: int = 0,
                     limit: int = Query(default=100, lte=100),
                     db: Session = Depends(Database().getSession)):
    tasks = db.exec(select(Task).offset(offset).limit(limit)).all()
    return tasks


@TaskRouter.get("/tasks/{task_id}", response_model=TaskRead, status_code=status.HTTP_200_OK)
async def read_task(task_id: UUID,
                    db: Session = Depends(Database().getSession)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@TaskRouter.patch("/tasks/{task_id}", response_model=TaskRead, status_code=status.HTTP_202_ACCEPTED)
async def update_task(task_id: UUID,
                      task: TaskUpdate,
                      db: Session = Depends(Database().getSession)):
    db_task = db.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = task.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@TaskRouter.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task(task_id: UUID,
                      db: Session = Depends(Database().getSession)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"Message": "Task deleted successfully"}
