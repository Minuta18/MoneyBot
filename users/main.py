from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import Depends
from passlib.context import CryptContext
import uvicorn, os
from init import engine, Base, get_db
import crud
import models
import shemas

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.on_event('startup')
async def init():
    Base.metadata.create_all(bind=engine)

@app.get('/users/{user_id}')
async def get_user(user_id: int, db: Session = Depends(get_db)):
    '''Returns a user by id'''
    usr = crud.get_user(db, user_id)
    if usr == None:
        return JSONResponse(
            status_code=404,
            content={
                'error': True,
                'message': 'User not found',
                'code': 1,
            }
        )
    return {
        'error': False,
        'id': usr.id,
        'email': usr.email,
        'is_banned': usr.is_banned,
    }

@app.get('/users')
async def users_list(page: int=1, page_size: int=20, db: Session = Depends(get_db)):
    '''Returns a list of users'''
    return {
        'error': False,
        'page': page,
        'page_size': page_size,
        'users': [{
            'id': usr.id,
            'email': usr.email,
            'is_banned': usr.is_banned,
        } for usr in crud.get_users(db, page=page, page_limit=page_size)],
    }

@app.post('/users/create')
async def create(user_create: shemas.UserCreateShema, db: Session = Depends(get_db)):
    '''Creates a user'''
    try:
        usr = crud.create_user(db, user_create.email, pwd_context.hash(user_create.password))
    except IntegrityError:
        return JSONResponse(
            status_code=400,
            content={
                'error': True,
                'message': 'User already exists',
                'code': 2,
            }
        )
    return {
        'error': False,
        'id': usr.id,
        'email': usr.email,
        'hashed_password': usr.hashed_password,
        'is_banned': usr.is_banned,
    }

@app.put('/users/{user_id}/edit')
async def edit(user_id: int, user_edit: shemas.UserEditShema, db: Session = Depends(get_db)):
    try:
        usr = crud.get_user(db, user_id)
        
        if not pwd_context.verify(user_edit.password, usr.hashed_password):
            return JSONResponse(
                status_code=403,
                content={
                    'error': True,
                    'message': 'Invalid password',
                    'code': 4,
                }
            )

        if usr == None:
            return JSONResponse(
                status_code=404,
                content={
                    'error': True,
                    'message': 'User not found',
                    'code': 1,
                }
            )
        
        crud.edit_user(db, usr, user_edit.new_email, pwd_context.hash(user_edit.new_password))
        return {
            'error': False,
        }
    except IntegrityError:
        return JSONResponse(
            status_code=400,
            content={
                'error': True,
                'message': 'User\'s email already exists',
                'code': 2,
            }
        )

if __name__ == '__main__':
    uvicorn.run('main:app', 
        port=int(os.environ.get('PORT', default=17010)), 
        host=os.environ.get('HOST', default='0.0.0.0'), 
        log_level='info'
    ) #