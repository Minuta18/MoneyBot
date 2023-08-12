from sqlalchemy.ext import asyncio
import init

async def get_session() -> asyncio.AsyncSession:
    '''
    This FastApi dependency returns a asynchronous SQL session
    
    :return: a :class:`asyncio.AsyncSession`
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