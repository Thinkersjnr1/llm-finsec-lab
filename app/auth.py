from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .database import SessionLocal
from .models import User


router = APIRouter(prefix="/api", tags=["Authentication"])


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(request: LoginRequest):
    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.username == request.username)
            .first()
        )

        if not user or user.password != request.password:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        return {
            "message": "Login successful",
            "user_id": user.id,
            "username": user.username,
            "token": f"user-{user.id}-token"
        }

    finally:
        db.close()

