from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Database import get_db, Crud, Models
from .Models import TransactionShema
from Security import Hashing

trans_router = APIRouter(
    prefix='/transaction',
    tags=['transaction',]
)

@trans_router.post('/make/')
async def make_transaction(transaction: TransactionShema, db: Session = Depends(get_db)):
    sender = Crud.get_user(db, transaction.sender_id)
    if sender == None:
        raise HTTPException(
            detail=f'No such user {transaction.sender_id}', 
            status_code=404
        )
    receiver = Crud.get_user(db, transaction.receiver_id)
    if receiver == None:
        raise HTTPException(
            detail=f'No such user {transaction.receiver_id}', 
            status_code=404,
        )
    
    if not Hashing.Hasher.verify(transaction.sender_password, sender.password):
        raise HTTPException(
            detail=f"Sender's passwords doesn't match",
            status_code=403,
        )

    if transaction.amount > sender.coins:
        raise HTTPException(
            detail=f'User {sender.id} has not enough coins',
            status_code=400,    
        )
    
    sender.coins -= transaction.amount
    receiver.coins += transaction.amount

    db.commit()

    return Crud.create_transaction(
        db,
        transaction.amount,
        transaction.sender_id,
        transaction.receiver_id,
    )

@trans_router.get('/{transaction_id}')
async def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = Crud.get_transaction(db, transaction_id)
    if transaction == None:
        return {}
    return transaction