from fastapi import APIRouter, HTTPException

from app.schemas.user import UserCreate
from app.schemas.token import Token

from app.database.db import fake_users_db

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(user: UserCreate):

    if user.username in fake_users_db:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    fake_users_db[user.username] = {
        "username": user.username,
        "password": hash_password(user.password)
    }

    return {
        "message": "User created successfully"
    }


@router.post("/login", response_model=Token)
def login(user: UserCreate):

    db_user = fake_users_db.get(user.username)

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        user.password,
        db_user["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        {"sub": user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/users")
def get_users():
    return fake_users_db