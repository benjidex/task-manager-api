from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import users

app = FastAPI(title="Task Manager API")

# Routers
app.include_router(users.router)

# Create tables
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Task Manager API running"}

# Register tasks routes
from app.routers import tasks
app.include_router(tasks.router)
