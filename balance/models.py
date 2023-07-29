from sqlalchemy import  Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
import init

class Balance(init.Base):
    __tablename__ = 'balances'

    id = Column(Integer, primary_key=True, index=True)
    points = Column(Integer)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User')

class User(init.Base):
    __table__ = Table('users', init.Base.metadata, autoload_with=init.engine)