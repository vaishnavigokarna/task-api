from fastapi import FastAPI, HTTPException

app = FastAPI()

# In-memory task list
tasks = [
    {"id": 1, "title": "Study Python", "done": False},
    {"id": 2, "title": "Complete Assignment", "done": True},
    {"id": 3, "title": "Go for a Walk", "done": False}
]

@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health():
    return {"status": "ok"}

# Get all tasks
@app.get("/tasks")
def get_tasks():
    return tasks

# Get one task by ID
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )