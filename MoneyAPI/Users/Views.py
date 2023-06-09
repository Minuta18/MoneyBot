from Database import Crud
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Database import get_db
from .Models import UserShema, UserEditShema
from Security import Hasher

usr_router = APIRouter(
    prefix='/users',
    tags=['users',],
)

@usr_router.get('/', tags=['users', ])
async def get_users(page: int = 1, page_size: int = 20, db: Session = Depends(get_db)):
    '''Gets list of users'''
    usrs = Crud.get_users(db, page_size * (page - 1), page_size)
    result = {'users': []}
    for usr in usrs:
        result['users'].append({
            'id': usr.id,
            'coins_count': usr.coins,
            'is_banned': usr.is_banned,
        })
    return result

@usr_router.get('/{user_id}', tags=['users', ])
async def get_user(user_id: int, db: Session = Depends(get_db)):
    '''Gets user by id'''
    usr = Crud.get_user(db, user_id)
    if usr != None:
        return {
            'id': usr.id,
            'coins_count': usr.coins,
            'is_banned': usr.is_banned,
        }

@usr_router.post('/create', tags=['users', ])
async def create_user(user: UserShema, db: Session = Depends(get_db)):
    '''Creates user'''
    new_password = Hasher.get_hash(user.password)
    new_user = Crud.create_user(db, new_password)
    return new_user

@usr_router.post('/delete/{user_id}', tags=['users', ])
async def delete_user(user: UserShema, user_id: int, db: Session = Depends(get_db)):
    '''Deletes user by id. Need password'''
    usr = Crud.get_user(db, user_id)
    if usr == None:
        raise HTTPException(detail='No such user', status_code=404)
    if Hasher.verify(user.password, usr.hashed_password):
        try:
            return Crud.delete_user(db, user_id)
        except ValueError:
            raise HTTPException(detail=f'No such user {user_id}', status_code=404)
    raise HTTPException(detail="Passwords doesn't match", status_code=403)

@usr_router.post('/edit/{user_id}', tags=['users', ])
async def edit_user(user: UserEditShema, user_id: int, db: Session = Depends(get_db)):
    '''Edit edit user's password. Need password'''
    usr = Crud.get_user(db, user_id)
    if usr == None:
        raise HTTPException(detail='No such user', status_code=404)
    if Hasher.verify(user.old_password, usr.hashed_password):
        try:
            return Crud.edit_user(db, user_id, Hasher.get_hash(user.new_password))
        except ValueError:
            return HTTPException(detail=f'No such user {user_id}', status_code=404)
    raise HTTPException(detail="Passwords doesn't match", status_code=403)