import os
from fastapi import FastAPI
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

if os.environ.get('TESTING', default=False):
    DATABASE_URI = os.environ.get('TESTING_URI', 'mysql+pymysql://root:test@127.0.0.1:17011/test')
else:
    DATABASE_URI = os.environ.get('MYSQL_URI', 'mysql+pymysql://api:test@127.0.0.1:17011/main')

# print(DATABASE_URI)

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# print(dir(Base), dir(Base.metadata), Base.metadata.tables, Base.metadata.info, sep='\n')
# print(inspect(engine).has_table('users'))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()