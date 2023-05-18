from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('put_url_there')

Base = declarative_base()

from . import Models

Base.metadata.create_all(bind=engine)

