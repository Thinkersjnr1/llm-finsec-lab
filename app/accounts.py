from fastapi import APIRouter, Depends, HTTPException

from .database import SessionLocal
from .models import User
from .security import get_current_user


router = APIRouter(prefix="/api", tags=["Accounts"])


@router.get("/balance/{user_id}")
def get_balance(
    user_id: int,
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access this account"
        )

    db = SessionLocal()

    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return {
            "user_id": user.id,
            "username": user.username,
            "balance": user.balance
        }

    finally:
        db.close()
