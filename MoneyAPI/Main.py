import uvicorn
from fastapi import FastAPI
from Database import Crud
from Users import usr_router
from Transactions import trans_router

app = FastAPI()
app.include_router(usr_router)
app.include_router(trans_router)

HOST = '0.0.0.0'
PORT = 17002

if __name__ == '__main__':
    uvicorn.run('Main:app', host=HOST, port=PORT, reload=True)