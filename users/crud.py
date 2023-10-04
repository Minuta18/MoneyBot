from sqlalchemy.ext import asyncio
from sqlalchemy import exc
import sqlalchemy as sql
import init
import models

async def get_session() -> asyncio.AsyncSession:
    '''
    This FastApi dependency returns a asynchronous SQL session

    :return: a `asyncio.AsyncSession`
    '''

    async with init.session() as session:
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
        await db.commit()

        return new_user
    except exc.IntegrityError:
        raise ValueError('Email already used')

async def get_user(db: asyncio.AsyncSession, user_id: int = ...):
    '''
    Gets one user by id

    :param db: Database session
    :param user_id: User's id
    :return: User or None if user is not exists
    '''

    return await db.get(models.User, user_id)

async def get_users(
            db: asyncio.AsyncSession,
            start_id: int = ...,
            end_id: int = ...,
        ):
    '''
    Gets multiple users with ids start_id..end_id

    :param db: Database session
    :param start_id: id of first user
    :param end_id: id of last user
    :return: List of users
    '''

    return (await db.execute(sql.select(models.User).offset(start_id).limit(
        abs(end_id - start_id) + 1
    ))).scalars().all()

async def update_user(
            db: asyncio.AsyncSession,
            user: models.User,
            email: str = ...,
            hashed_password: str = ...,
        ) -> models.User:
    '''
    Gets multiple users with ids start_id..end_id

    :param db: Database session
    :param user: User to edit
    :param email: New email
    :param hashed_password: New password
    :return: Edited user
    '''

    user.email = email
    user.hashed_password = hashed_password

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user

async def delete_user(
            db: asyncio.AsyncSession,
            user_id: int = ...,
        ) -> models.User:
    '''
    Deletes user by given id, raises ValueError if user doesn't exists.

    :param db: Database session
    :param user_id: Id user to delete
    :return: Deleted user
    '''

    user = await get_user(db, user_id=user_id)
    if user is None:
        raise ValueError(f'Can\'t found user with id {user_id}')

    await db.delete(user)
    await db.commit()

    return user
