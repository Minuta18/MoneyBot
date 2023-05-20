import uvicorn
from fastapi import FastAPI
from Database import Crud
from Users import usr_router

app = FastAPI()
app.include_router(usr_router)

@app.get('/')
async def root():
    return {'test': True}

@app.get('/transaction/')
async def make_transaction():
    ...

@app.get('/transaction/{transaction_id}')
async def get_transaction(transaction_id: int):
    ...

if __name__ == '__main__':
    uvicorn.run('Main:app', host='127.0.0.1', port=8000, reload=True)