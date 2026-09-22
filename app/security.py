from fastapi import Header, HTTPException
from .database import SessionLocal
from .models import User


def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header required"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization format"
        )

    token = authorization.replace("Bearer ", "", 1)

    if not token.startswith("user-") or not token.endswith("-token"):
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    try:
        user_id = int(
            token.replace("user-", "", 1).replace("-token", "", 1)
        )
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    db = SessionLocal()

    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        return user

    finally:
        db.close()
