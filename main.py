from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, Task

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing tasks",
    version="1.0"
)

# Request Models
class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


# Database Session
def get_db():
    db = SessionLocal()
    return db


# Root Endpoint
@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": [
            "/tasks",
            "/health"
        ]
    }


# Health Endpoint
@app.get("/health")
def health():
    return {"status": "ok"}


# Get All Tasks
@app.get("/tasks")
def get_tasks():
    db = get_db()

    tasks = db.query(Task).all()

    return [
        {
            "id": task.id,
            "title": task.title,
            "done": task.done
        }
        for task in tasks
    ]


# Get Single Task
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    db = get_db()

    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return {
        "id": task.id,
        "title": task.title,
        "done": task.done
    }


# Create Task
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):

    if task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    db = get_db()

    new_task = Task(
        title=task.title,
        done=False
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "id": new_task.id,
        "title": new_task.title,
        "done": new_task.done
    }
# Update Task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate):

    db = get_db()

    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    if updated_task.title is not None:
        if updated_task.title.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="Title cannot be empty"
            )
        task.title = updated_task.title

    if updated_task.done is not None:
        task.done = updated_task.done

    db.commit()
    db.refresh(task)

    return {
        "id": task.id,
        "title": task.title,
        "done": task.done
    }


# Delete Task
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):

    db = get_db()

    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    db.delete(task)
    db.commit()

    return