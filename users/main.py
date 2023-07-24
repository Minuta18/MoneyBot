from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import Depends
import uvicorn, os
from init import engine, Base, get_db
import crud
from models import User

app = FastAPI()

@app.on_event('startup')
async def init():
    Base.metadata.create_all(bind=engine)

@app.get('/user/{user_id}')
async def get_user(user_id: int, db: Session = Depends(get_db)):
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

if __name__ == '__main__':
    uvicorn.run('main:app', 
        port=int(os.environ.get('PORT', default=17010)), 
        host=os.environ.get('HOST', default='0.0.0.0'), 
        log_level='info'
    ) #