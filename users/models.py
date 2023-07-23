from sqlalchemy import  Column, Integer, String, Boolean
from . import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True)
    hashed_password = Column(String(255))

    is_banned = Column(Boolean)
