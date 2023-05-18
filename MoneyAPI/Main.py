from fastapi import FastAPI
from MoneyAPI.database import Crud

app = FastAPI()

@app.route('/user/{user_id}')
def get_user(user_id: int):
    return Crud.get_user(user_id)

@app.route('/user/create')
def create_user():
    ...

@app.route('/user/delete/{user_id}')
def delete_user(user_id: int):
    ...

@app.route('/user/edit/{user_id}')
def edit_user(user_id: int):
    ...

@app.route('/transaction/')
def make_transaction():
    ...

@app.route('/transaction/{transaction_id}')
def get_transaction(transaction_id: int):
    ...