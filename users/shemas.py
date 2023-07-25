from pydantic import BaseModel

class UserCreateShema(BaseModel):
    email: str
    password: str
    