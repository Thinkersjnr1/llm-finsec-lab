from .database import Base, engine, SessionLocal
from .models import User,Transfer


Base.metadata.create_all(bind=engine)


def create_users():
    db = SessionLocal()

    if db.query(User).count() == 0:
        alice = User(
            id=123,
            username="alice",
            password="alice123",
            balance=500000.0
        )

        bob = User(
            id=124,
            username="bob",
            password="bob123",
            balance=750000.0
        )

        db.add(alice)
        db.add(bob)
        db.commit()

        print("Created Alice and Bob.")

    else:
        print("Users already exist.")

    db.close()


if __name__ == "__main__":
    create_users()
