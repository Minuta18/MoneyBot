import os
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

app = FastAPI()

mysql_uri = os.environ.get('MYSQL_URI', default='noaddr')
engine = create_engine(mysql_uri, echo=True)
session = sessionmaker(autoflush=False, bind=engine)

class Base(DeclarativeBase): pass