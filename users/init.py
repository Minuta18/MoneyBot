from os import environ
from sqlalchemy.ext import declarative
from sqlalchemy.ext import asyncio
from sqlalchemy import orm

PREFIX = environ.get('PREFIX', default='/api')
TESTING = environ.get('TESTING', default=False)

DATABASE_URL = 'mysql+tormysql://{}:{}@{}:{}/{}'.format(
    environ.get('DB_USER', default='root'),  # Root is always exists
    ':' + environ.get('DB_PASSWORD') if environ.get('DB_PASSWORD') is not \
    None else '',
    environ.get('DB_HOST', default='localhost'),
    environ.get('DB_PORT', default='3306'),  # Standard mysql port
    environ.get('DB_MAIN', default='main') if TESTING
    else environ.get('DB_TEST', default='test'),
)

OPENAPI_URL = '{}/users/openapi.json'.format(PREFIX)
DOCS_URL = '{}/users/docs'.format(PREFIX)

# All database operations should be asynchronous to make service faster
engine = asyncio.create_async_engine(DATABASE_URL, echo=True)
base = declarative.declarative_base()
session = orm.sessionmaker(
    bind=engine, 
    class_=asyncio.AsyncSession, 
    expire_on_commit=False
)
