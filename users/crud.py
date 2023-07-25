import models
from sqlalchemy.orm import Session

def get_user(db: Session, user_id: int):
    return db.query(models.User).get(user_id)

def get_users(db: Session, page: int=1, page_limit: int=20):
    return db.query(models.User).offset((page - 1) * 20).limit(page_limit).all()

def create_user(db: Session, email: str=None, hashed_password: str=None) -> models.User:
    new_user = models.User(
        email=email,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user