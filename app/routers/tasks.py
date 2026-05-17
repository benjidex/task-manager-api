from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .. import models, database, schemas, auth

router = APIRouter()

# Database connection
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Task schema
class TaskCreate(BaseModel):
    title: str
    description: str

# Create task
@router.post("/tasks")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(auth.get_current_user)
):
    new_task = models.Task(
        title=task.title,
        description=task.description,
        owner_id=user_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

# Get user's tasks
@router.get("/tasks")
def get_tasks(
    db: Session = Depends(get_db),
    user_id: int = Depends(auth.get_current_user)
):
    tasks = db.query(models.Task).filter(
        models.Task.owner_id == user_id
    ).all()

    return tasks



@router.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    updated_task: TaskCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(auth.get_current_user)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == user_id
    ).first()

    if not task:
        return {"error": "Task not found"}

    task.title = updated_task.title  # type: ignore
    task.description = updated_task.description  # type: ignore

    db.commit()
    db.refresh(task)

    return task



@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(auth.get_current_user)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == user_id
    ).first()

    if not task:
        return {"error": "Task not found"}

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}