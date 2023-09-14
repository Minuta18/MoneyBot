from sqlalchemy.ext import asyncio
from fastapi.responses import JSONResponse
from passlib import context
import fastapi
import init
import models
import crud
import shema
import asyncio as asynciolib

app = fastapi.FastAPI(
    openapi_url=init.OPENAPI_URL,
    docs_url=init.DOCS_URL,
)
router = fastapi.APIRouter(prefix=f'{init.PREFIX}/users')
pwd_context = context.CryptContext(schemes=["bcrypt"], deprecated="auto")

async def init_models():
    async with init.engine.begin() as conn:
        await conn.run_sync(init.base.metadata.create_all)

'''
Error code   meaning
--------------------------------
1            Item not found
2            Item already exists
'''

@app.on_event('startup')
async def startup_event():
    await init_models()

@app.on_event('shutdown')
async def shutdown_event():
    async with init.engine.begin() as conn:
        await conn.close()

@router.get('/health')
async def health_check(request: fastapi.Request):
    '''
    Health check can be used to check if service is available and
    can accept connections
    '''

    init.logging.info('Checked service health by ' +
                      f'{request.client.host}:{request.client.port}')

    return {
        'error': False,
    }

@router.get('/{user_id}')
async def get_user(
            user_id: int,
            db: asyncio.AsyncSession = fastapi.Depends(crud.get_session)
        ):
    '''
    Returns user by id
    '''

    user = await crud.get_user(db, user_id)
    if user is None:
        init.logging.error(f'User not found with id={user_id}')

        return JSONResponse(content={
            'error': True,
            'code': 1,
            'message': 'User not found',
        }, status_code=404)

    init.logging.info(f'Returned user with id={user_id}')
    return {
        'error': False,
        'id': user.id,
        'email': user.email,
        'balance': 0,
    }

@router.get('/')
async def get_users(
            page: int = 1,
            page_size: int = 20,
            db: asyncio.AsyncSession = fastapi.Depends(crud.get_session),
        ):
    '''
    Returns multiple users
    '''

    users = await crud.get_users(
        db, 
        start_id=((page - 1) * page_size), 
        end_id=((page - 1) * page_size)
    )

    return {
        'error': False,
        'page': 1,
        'page_size': 20,
        'users': [{
            'id': user.id,
            'email': user.email,
            'is_banned': user.is_banned,
            'balance': 0,
        } for user in users],
    }

@router.post('/create')
async def create_user(
            create_shema: shema.UserCreateShema,
            db: asyncio.AsyncSession = fastapi.Depends(crud.get_session)
        ):
    '''
    Creates a new user
    '''

    password = pwd_context.hash(create_shema.password)

    try:
        new_user = await crud.create_user(db, create_shema.email, password)
        init.logging.info(f'Created user with id={new_user.id}')

        return {
            'error': False,
            'id': new_user.id,
            'email': new_user.email,
            'balance': 0,
            'is_banned': new_user.is_banned,
        }
    except ValueError:
        init.logging.error('Error while creating user: User with' +
                           f'email={create_shema.email} already created')

        return JSONResponse(content={
            'error': True,
            'code': 2,
            'message': 'User already created',
        }, status_code=400)

app.include_router(router)