import os
from fastapi import FastAPI
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

if os.environ.get('TESTING', default=True):
    DATABASE_URI = os.environ.get('TESTING_URI', 'mysql+pymysql://root:test@127.0.0.1:17011/test')
else:
    DATABASE_URI = os.environ.get('MYSQL_URI', 'mysql+pymysql://api:test@127.0.0.1:17011/main')

USERS_SERVICE_URL = os.environ.get('USERS_SERVICE_URL', 'http://localhost:17010/api/v1/users')

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()