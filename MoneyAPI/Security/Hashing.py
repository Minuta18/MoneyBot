from passlib.context import CryptContext
from random import randint

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher():
    @staticmethod
    def verify(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_hash(password):
        return pwd_context.hash(password)