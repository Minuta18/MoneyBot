from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    hashed_password = Column(String)
    coins = Column(Integer)
    is_banned = Column(Boolean)

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    sum = Column(Integer)
    sender_id = Column(Integer, ForeignKey('User.id'))
    receiver_id = Column(Integer, ForeignKey('User.id'))

