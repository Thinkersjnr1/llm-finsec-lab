import math

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from .database import SessionLocal
from .models import User, Transfer
from .security import get_current_user

router = APIRouter(prefix="/api", tags=["Transfers"])


class TransferRequest(BaseModel):
    from_user: int
    to_user: int
    amount: float = Field(gt=0, allow_inf_nan=False)
    idempotency_key: str = Field(min_length=1, max_length=100)


@router.post("/transfer")
def transfer(
    request: TransferRequest,
    current_user: User = Depends(get_current_user)
):
    # Authorization check
    if current_user.id != request.from_user:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to transfer from this account"
        )

    # Reject NaN and positive/negative Infinity
    if not math.isfinite(request.amount):
        raise HTTPException(
            status_code=400,
            detail="Amount must be a finite number"
        )

    db = SessionLocal()

    try:
        # Replay / duplicate-transfer check
        existing_transfer = (
            db.query(Transfer)
            .filter(
                Transfer.idempotency_key == request.idempotency_key
            )
            .first()
        )

        if existing_transfer:
            raise HTTPException(
                status_code=409,
                detail="Duplicate transfer request"
            )

        sender = (
            db.query(User)
            .filter(User.id == request.from_user)
            .first()
        )

        recipient = (
            db.query(User)
            .filter(User.id == request.to_user)
            .first()
        )

        if not sender or not recipient:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        if request.amount <= 0:
            raise HTTPException(
                status_code=400,
                detail="Amount must be greater than zero"
            )

        if sender.balance < request.amount:
            raise HTTPException(
                status_code=400,
                detail="Insufficient balance"
            )

        sender.balance -= request.amount
        recipient.balance += request.amount

        transfer_record = Transfer(
            idempotency_key=request.idempotency_key,
            from_user=sender.id,
            to_user=recipient.id,
            amount=request.amount
        )

        db.add(transfer_record)
        db.commit()

        return {
            "message": "Transfer successful",
            "from_user": sender.id,
            "to_user": recipient.id,
            "amount": request.amount,
            "idempotency_key": request.idempotency_key
        }
    except Exception:
        db.rollback()
        raise


    finally:
        db.close()
