from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, database, schemas, auth

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Register
@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing_user:
        return {"error": "Username already exists"}

    new_user = models.User(
        username=user.username,
        password=auth.hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# Login
@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return auth.authenticate_user(
        user.username,
        user.password,
        db
    )