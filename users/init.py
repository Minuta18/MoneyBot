import os
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

if os.environ.get('TESTING', default=True):
    DATABASE_URI = os.environ.get('MYSQL_URI', default='mysql+pymysql://root:test@127.0.0.1:17011/test')
else:
    DATABASE_URI = os.environ.get('TESTING_URI', default='mysql+pymysql://root:test@127.0.0.1:17011/main')

BALANCES_URI = os.environ.get('BALANCES_URL', default='http://localhost:17012/api/v1/balances')

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()