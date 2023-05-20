from . import Base
from . import Models
from sqlalchemy.orm import Session

def get_user(db: Session, user_id: int):
    return db.query(Models.User).filter(Models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(Models.User).filter(Models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Models.User).offset(skip).limit(limit).all()

def create_user(db: Session, password: str, coins: int = 200):
    new_user = Models.User(
        hashed_password=password,
        coins=coins,
        is_banned=False,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def delete_user(db: Session, id: int):
    user = db.query(Models.User).filter(Models.User.id == id).first()
    if user != None:
        db.delete(user)
        db.commit()
    else:
        raise ValueError(f'No user with id {id}')
    return user

def edit_user(db: Session, id: int, new_password: str):
    user = db.query(Models.User).filter(Models.User.id == id).first()
    if user != None:
        user.hashed_password = new_password
        db.commit()
    else:
        raise ValueError(f'No user with id {id}')
    return user

def get_transaction(db: Session, id: int):
    return db.query(Models.Transaction).filter(Models.Transaction.id == id).first()

def create_transaction(db: Session, sum: int, sender_id: int, receiver_id: int):
    new_transaction = Models.Transaction(
        sum=sum,
        sender_id=sender_id,
        receiver_id=receiver_id,
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction