from pydantic import BaseModel

class UserCreateShema(BaseModel):
    email: str
    password: str
    

class UserEditShema(BaseModel):
    password: str
    new_password: str
    new_email: str