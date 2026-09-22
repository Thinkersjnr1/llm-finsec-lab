from fastapi import HTTPException

from .database import SessionLocal
from .models import User, Transfer


def get_balance(requesting_user_id: int, user_id: int):
    if requesting_user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="AI tool: unauthorized account access"
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


def get_profile(requesting_user_id: int, user_id: int):
    if requesting_user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="AI tool: unauthorized profile access"
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
            "username": user.username
        }

    finally:
        db.close()


def get_transactions(requesting_user_id: int, user_id: int):
    if requesting_user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="AI tool: unauthorized transaction access"
        )

    db = SessionLocal()

    try:
        transactions = (
            db.query(Transfer)
            .filter(
                (Transfer.from_user == user_id) |
                (Transfer.to_user == user_id)
            )
            .all()
        )

        return [
            {
                "id": transaction.id,
                "from_user": transaction.from_user,
                "to_user": transaction.to_user,
                "amount": transaction.amount
            }
            for transaction in transactions
        ]

    finally:
        db.close()
