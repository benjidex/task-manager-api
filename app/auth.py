from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

# Fake token storage
tokens = {}

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = f"token-{user.username}"

    tokens[token] = user.id

    return {"access_token": token}

from fastapi import Header

def get_current_user(token: str = Header(...)):
    user_id = tokens.get(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user_id