from database import Crud
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

usr_router = APIRouter(
    prefix='/users',
    tags=['users',],
)

@usr_router.get('/{user_id}', tags=['users', ])
async def get_user(user_id: int, db: Session = Depends(get_db)):
    usr =  Crud.get_user(user_id, db)

    return usr if usr != None else {}

@usr_router.post('/create', tags=['users', ])
async def create_user():
    return {"detail": "in dev"}

@usr_router.get('/delete/{user_id}', tags=['users', ])
async def delete_user(user_id: int):
    ...

@usr_router.get('/edit/{user_id}', tags=['users', ])
async def edit_user(user_id: int):
    ...