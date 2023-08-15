from sqlalchemy.ext import asyncio
from sqlalchemy import exc
import init
import models

async def get_session() -> asyncio.AsyncSession:
    '''
    This FastApi dependency returns a asynchronous SQL session

    :return: a `asyncio.AsyncSession`
    '''

    async with init.session as session:
        yield session

async def init_models():
    '''
    This function drop and create all tables
    '''

    async with init.engine.begin() as conn:
        await conn.run_sync(init.base.metadata.drop_all)
        await conn.run_sync(init.base.metadata.create_all)

async def create_user(
            db: asyncio.AsyncSession,
            email: str = '',
            hashed_password: str = '',
            log: bool = True,
        ) -> models.User:
    '''
    Creates a new user

    :param db: Database session
    :param email: Email of new user
    :param hashed_password: Password of new user, must be hashed
    :return: New user
    '''
    try:
        new_user = models.User(
            email=email,
            hashed_password=hashed_password,
        )

        db.add(new_user)
        db.commit()

        if log:
            init.logger.info('users.crud.create_user:' +
                             'created new user with id' +
                             f'{new_user.id}')
    except exc.IntegrityError:
        raise ValueError('Email already used')

async def get_user():
    ...

async def update_user():
    ...

async def delete_user():
    ...
