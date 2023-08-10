import models
from sqlalchemy.orm import Session

def get_user(db: Session, user_id: int):
    return db.get(models.User, user_id)

def get_users(db: Session, page: int=1, page_limit: int=20):
    return db.query(models.User).offset((page - 1) * 20).limit(page_limit).all()

def create_user(db: Session, email: str=None, hashed_password: str=None, commit: bool=True) -> models.User:
    new_user = models.User(
        email=email,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    if commit:
        db.commit()

    return new_user

def edit_user(db: Session, user: models.User, email: str, hashed_password: str):
    user.email = email
    user.hashed_password = hashed_password
    
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def delete_user(db: Session, id: int, commit: bool=True) -> None:
    user = get_user(db, id)
    if user == None:
        raise ValueError('User is not exists')
    
    db.delete(user)
    if commit:
        db.commit()

def commit(db: Session):
    db.commit()

def rollback(db: Session):
    db.rollback()