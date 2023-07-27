import os
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

if not os.environ.get('TESTING', default=True):
    DATABASE_URI = os.environ.get('DATABASE_URI', default='mysql+pymysql://root:test@127.0.0.1:17011/main')
else:
    DATABASE_URI = os.environ.get('DATABASE_URI', default='mysql+pymysql://root:test@127.0.0.1:17011/test')

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()