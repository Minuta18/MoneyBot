import init
import uvicorn
import fastapi
from shared_components import requests
from fastapi import responses
from sqlalchemy import exc

import models
import shemas
import crud

app = fastapi.FastAPI(openapi_url='/api/v1/balances/openapi.json', docs_url='/api/v1/balances/docs')
router = fastapi.APIRouter(prefix='/api/v1/balances')

@app.on_event('startup')
async def init_():
    init.Base.metadata.create_all(bind=init.engine)

@router.post('/create')
async def create(create_shema: shemas.BalanceCreateShema, db = fastapi.Depends(init.get_db)):
    maker = requests.RequestMaker()
    user = maker.get(f'{init.USERS_SERVICE_URL}/{create_shema.user_id}')
    if user.status_code != 200:
        return responses.JSONResponse(
            status_code=404,
            content={
                'error': True,
                'message': 'User not found',
                'code': 1,
            }
        )
    
    try:
        new_balance = crud.create_balance(db, create_shema.user_id)
    except exc.IntegrityError:
        return responses.JSONResponse({
                'error': True,
                'message': 'Balance already created',
                'code': 2,     
            },
            status_code=400,
        ) 

    return {
        'error': False,
        'points': new_balance.points,
    }

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run('main:app', 
        port=int(init.os.environ.get('PORT', default=17013)), 
        host=init.os.environ.get('HOST', default='0.0.0.0'), 
        log_level='info'
    ) #