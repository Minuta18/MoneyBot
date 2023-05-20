from pydantic import BaseModel

class UserShema(BaseModel):
    password: str

class UserEditShema(BaseModel):
    old_password: str
    new_password: str