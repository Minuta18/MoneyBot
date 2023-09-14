import sqlalchemy as sql
import init
import asyncio

class User(init.base):
    __tablename__ = 'users'

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    email = sql.Column(sql.String(255), unique=True)
    hashed_password = sql.Column(sql.String(255))

    is_banned = sql.Column(sql.Boolean, default=False)
