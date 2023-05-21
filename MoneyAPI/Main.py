import uvicorn
from fastapi import FastAPI
from Database import Crud
from Users import usr_router
from Transactions import trans_router

app = FastAPI()
app.include_router(usr_router)
app.include_router(trans_router)

@app.get('/')
async def root():
    return {'test': True}

if __name__ == '__main__':
    uvicorn.run('Main:app', host='127.0.0.1', port=8000, reload=True)